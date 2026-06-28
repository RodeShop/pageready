#!/usr/bin/env python3
"""
playwright_notion.py — Automates Notion template setup via Chrome CDP.

What it does:
  1. Opens the template root page (via Quick Find to avoid login popup)
  2. Clicks Share → enables "Allow template duplication"
  3. Extracts the template URL
  4. Adds Board/Calendar views to each database
  5. Saves template URL to gumroad_result.json

Usage:
  python scripts/playwright_notion.py <slug>
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print('Playwright not installed. Run: pip install playwright && playwright install chromium')
    sys.exit(1)

DEBUG_DIR = Path('debug_screenshots')
DEBUG_DIR.mkdir(exist_ok=True)

# Notion email for popup auth (popup uses curly apostrophe so plain text match fails)
NOTION_EMAIL = 'sparklechuba@onet.pl'

VIEW_MAP = {
    'Client':  ['Board', 'Timeline'],
    'Project': ['Board', 'Timeline', 'Calendar'],
    'Task':    ['Board', 'Calendar'],
    'Content': ['Board', 'Calendar', 'Gallery'],
    'Idea':    ['Gallery', 'Board'],
    'Job':     ['Board', 'Calendar'],
    'Course':  ['Board', 'Calendar'],
    'default': ['Board', 'Calendar'],
}


def screenshot(page, name):
    try:
        page.screenshot(path=str(DEBUG_DIR / f'notion_{name}.png'), timeout=8000)
    except Exception as e:
        print(f'  [screenshot:{name}] {type(e).__name__}: {e}')


def slug_to_title(slug):
    """notion-content-creator-dashboard -> Content Creator Dashboard"""
    return slug.replace('notion-', '').replace('-', ' ').title()


def grant_notion_permissions(context):
    """Pre-grant clipboard so Publish → Copy link does not block on OS prompt."""
    for origin in ('https://app.notion.com', 'https://www.notion.so', 'https://notion.so'):
        try:
            context.grant_permissions(['clipboard-read', 'clipboard-write'], origin=origin)
        except Exception:
            pass


def normalize_template_url(raw, page_id_clean, title_slug):
    """Return https://…notion.site/… or None. Rejects label text without scheme."""
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith('https://') and 'notion.site' in raw:
        return raw.split('?')[0].rstrip('/')
    m = re.search(r'([\w-]+\.notion\.site)', raw)
    if m:
        host = m.group(1)
        path = f'{title_slug}-{page_id_clean}'
        return f'https://{host}/{path}'
    return None


def _hover_cover_strip(page):
    """Reveal cover toolbar (Change / Reposition) via hover."""
    page.evaluate("""() => {
        const repo = document.querySelector('[aria-label="Reposition the cover image"]');
        if (repo) {
            let p = repo;
            for (let i = 0; i < 5 && p; i++) {
                p.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                p.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                p = p.parentElement;
            }
        }
        for (const sel of ['.notion-page-cover-image', '.notion-page-cover', '[class*="pagecover"]', '[class*="page-cover"]']) {
            const el = document.querySelector(sel);
            if (el) {
                el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                el.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
            }
        }
    }""")


def _click_cover_change(page):
    """Click Change on cover strip — span.milana-unmask inside top toolbar."""
    _hover_cover_strip(page)
    page.wait_for_timeout(600)
    vp = page.viewport_size or {'width': 1400, 'height': 900}
    for x, y in [(vp['width'] // 2, 55), (vp['width'] // 2, 85), (vp['width'] - 180, 55)]:
        page.mouse.move(x, y)
        page.wait_for_timeout(400)

    clicked = page.evaluate("""() => {
        const isChange = el => (el.textContent || '').trim() === 'Change';
        const pick = els => els.find(el => {
            const r = el.getBoundingClientRect();
            return r.top >= 0 && r.top < 200 && r.width > 0 && r.height > 0;
        });
        let target = pick([...document.querySelectorAll('span.milana-unmask')].filter(isChange));
        if (!target) target = pick([...document.querySelectorAll('span, [role="button"], button')].filter(isChange));
        if (!target) return false;
        const clickEl = target.closest('[role="button"]') || target.parentElement || target;
        clickEl.click();
        return true;
    }""")
    if clicked:
        page.wait_for_timeout(1200)
        print('  Clicked Change cover button (cover strip)')
    return bool(clicked)


def _click_upload_tab(page):
    clicked = page.evaluate("""() => {
        const tab = [...document.querySelectorAll('[role="tab"]')]
            .find(el => (el.textContent || '').trim().includes('Upload'));
        if (tab) { tab.click(); return true; }
        return false;
    }""")
    if clicked:
        page.wait_for_timeout(800)
        print('  Clicked Upload tab')
        return True
    for sel in ['[role="tab"]:has-text("Upload")', 'div[role="tab"]:has-text("Upload")']:
        try:
            tab = page.locator(sel).first
            if tab.is_visible(timeout=1500):
                tab.click()
                page.wait_for_timeout(800)
                print('  Clicked Upload tab')
                return True
        except Exception:
            continue
    return False


def _upload_cover_file(page, cover_path):
    """Upload via file chooser (Upload file btn) or hidden input — no native OS dialog."""
    if _click_upload_tab(page):
        pass
    else:
        print('  Upload tab not found — trying file input anyway')

    try:
        for inp in page.locator('input[type="file"]').all():
            inp.set_input_files(cover_path, timeout=3000)
            page.wait_for_timeout(4000)
            print('  Cover uploaded via input[type="file"]')
            return True
    except Exception:
        pass

    try:
        with page.expect_file_chooser(timeout=12000) as fc_info:
            page.evaluate("""() => {
                const btn = [...document.querySelectorAll('[role="button"], button')]
                    .find(el => (el.textContent || '').trim() === 'Upload file');
                if (btn) btn.click();
            }""")
        fc_info.value.set_files(cover_path)
        page.wait_for_timeout(4000)
        print('  Cover uploaded via file chooser')
        return True
    except Exception as e:
        print(f'  File chooser failed: {e}')

    try:
        cdp = page.context.new_cdp_session(page)
        doc = cdp.send('DOM.getDocument')
        res = cdp.send('DOM.querySelectorAll', {
            'nodeId': doc['root']['nodeId'],
            'selector': 'input[type="file"]',
        })
        if res.get('nodeIds'):
            cdp.send('DOM.setFileInputFiles', {
                'nodeId': res['nodeIds'][0],
                'files': [cover_path],
            })
            page.wait_for_timeout(4000)
            print('  Cover uploaded via CDP')
            return True
    except Exception as e:
        print(f'  CDP fallback failed: {e}')
    return False


def is_popup_visible(page):
    """
    Detect Notion 'You're almost there!' popup.
    Notion uses curly apostrophe (U+2019) so we match a safe substring.
    """
    try:
        # Use partial text match — avoids curly vs straight apostrophe issue
        return page.get_by_text('almost there', exact=False).is_visible(timeout=1500)
    except Exception:
        pass
    try:
        return page.get_by_text('Sign in to see this page', exact=False).is_visible(timeout=1000)
    except Exception:
        return False


def click_google_continue_as(context):
    """Click Google account picker: 'Continue as RODE51' / 'Continue as ...'."""
    for p in context.pages:
        for sel in [
            'button:has-text("Continue as")',
            '[role="button"]:has-text("Continue as")',
            'div[role="button"]:has-text("Continue as")',
            'text=Continue as RODE51',
        ]:
            try:
                btn = p.locator(sel).first
                if btn.is_visible(timeout=2000):
                    btn.click(timeout=5000)
                    p.wait_for_timeout(3000)
                    print('  Clicked Google "Continue as" button')
                    return True
            except Exception:
                continue
    return False


def click_notion_google_signin(page):
    """On Notion login modal, click Continue with Google."""
    for sel in [
        'button[aria-label="Continue with Google"]',
        'div[aria-label="Continue with Google"]',
        '[data-provider="google"]',
        'button:has-text("Google")',
        'div[role="button"]:has-text("Google")',
        'img[alt="Google"]',
    ]:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1500):
                el.click(timeout=3000)
                page.wait_for_timeout(2000)
                print('  Clicked Notion Google sign-in')
                return True
        except Exception:
            continue
    return False


def handle_notion_auth(page, context):
    """
    Complete Notion login: Google 'Continue as RODE51' or Notion modal flow.
    Returns True if authenticated (popup gone).
    """
    if not is_popup_visible(page):
        return True

    print('  Auth popup — signing in...')

    # Google account picker may already be visible (top-right overlay)
    if click_google_continue_as(context):
        page.wait_for_timeout(4000)
        if not is_popup_visible(page):
            return True

    # Otherwise start Google flow from Notion modal
    if click_notion_google_signin(page):
        page.wait_for_timeout(2000)
        click_google_continue_as(context)
        page.wait_for_timeout(4000)
        if not is_popup_visible(page):
            return True

    # Retry Continue as (popup can appear with delay)
    for _ in range(3):
        if click_google_continue_as(context):
            page.wait_for_timeout(3000)
            if not is_popup_visible(page):
                return True
        page.wait_for_timeout(1500)

    return not is_popup_visible(page)


def dismiss_popup(page, context=None):
    """Legacy name — delegates to handle_notion_auth when context available."""
    if context is not None:
        return handle_notion_auth(page, context)

    page.keyboard.press('Escape')
    page.wait_for_timeout(800)
    return not is_popup_visible(page)


def ensure_notion_loaded(page, context=None):
    """
    Only navigate to notion.so root if the current page isn't already
    inside the workspace (avoids overwriting an authenticated tab).
    """
    url = page.url
    is_workspace = (
        ('notion.so' in url and len(url) > len('https://www.notion.so/')) or
        'app.notion.com' in url
    )
    if is_workspace:
        print('  Already on a Notion workspace page.')
        if context and is_popup_visible(page):
            handle_notion_auth(page, context)
        return True

    print('  Loading Notion workspace...')
    page.goto('https://www.notion.so', wait_until='domcontentloaded', timeout=30000)
    page.wait_for_timeout(5000)  # let SPA redirect to workspace

    if context:
        handle_notion_auth(page, context)

    screenshot(page, 'app_loaded')
    print('  Notion ready.')
    return True


def quick_find_navigate(page, context, search_term):
    """
    Use Notion Quick Find (Ctrl+K) to navigate to a page by name.
    Returns True if navigation likely succeeded.
    """
    print(f'  Quick Find: searching for "{search_term}"...')

    # Open Quick Find
    page.keyboard.press('Control+k')
    page.wait_for_timeout(800)

    screenshot(page, f'qf_open')

    # Clear any existing text and type search
    page.keyboard.press('Control+a')
    page.keyboard.type(search_term)
    page.wait_for_timeout(1500)

    screenshot(page, f'qf_results')

    # Press Enter to select first result
    page.keyboard.press('Enter')
    page.wait_for_timeout(3000)

    # Check if popup appeared (use robust detection — curly apostrophe safe)
    if is_popup_visible(page):
        print('  Popup after Quick Find — trying to dismiss...')
        dismiss_popup(page, context)
        if is_popup_visible(page):
            return False

    screenshot(page, f'qf_navigated')
    return True


def navigate_to_notion_page(page, context, url, search_term):
    """
    Navigate to a Notion page.
    Waits for notion.so -> app.notion.com redirect to complete.
    Handles auth popup if it appears.
    """
    page.goto(url, wait_until='domcontentloaded', timeout=30000)

    # Wait for redirect: notion.so redirects to app.notion.com
    try:
        page.wait_for_url(
            lambda u: 'app.notion.com' in u or ('notion.so' in u and len(u) > 35),
            timeout=8000
        )
    except Exception:
        pass

    # Let the SPA fully render
    page.wait_for_timeout(4000)

    if is_popup_visible(page):
        print('  Auth popup detected — trying to dismiss...')
        dismissed = dismiss_popup(page, context)
        if not dismissed:
            print('  Popup persists — Notion auth needed.')
            print('  TIP: Open notion.so in Chrome and log in via Google.')
            screenshot(page, 'popup_auth_needed')
            return False

    return True


def upload_notion_cover(page, context, page_id, slug):
    """Upload notion-cover.png to root page cover. Skips with warning if file not found."""
    cover_path = None
    for base in [f'products/draft/{slug}', f'products/ready/{slug}']:
        candidate = Path(base) / 'notion-cover.png'
        if candidate.exists():
            cover_path = str(candidate.resolve())
            break

    if not cover_path:
        print('  [0] notion-cover.png not found — skipping cover upload')
        return False

    print(f'  Cover file: {cover_path}')

    page_id_clean = page_id.replace('-', '')
    title_slug = slug_to_title(slug).replace(' ', '-')
    app_url = f'https://app.notion.com/p/{title_slug}-{page_id_clean}'
    fallback_url = f'https://www.notion.so/{page_id_clean}'

    ok = navigate_to_notion_page(page, context, app_url, slug)
    if not ok:
        ok = navigate_to_notion_page(page, context, fallback_url, slug)
    if not ok:
        print('  [0] Navigation failed — skipping cover upload')
        return False

    # Assert we landed on the correct page
    landed_url = page.url
    if page_id_clean not in landed_url.replace('-', ''):
        print(f'  [0] Wrong page after navigation (expected {page_id_clean} in URL, got {landed_url}) — skipping')
        screenshot(page, '0_wrong_page')
        return False

    # Ensure cover strip is fully visible
    page.set_viewport_size({'width': 1400, 'height': 900})
    page.wait_for_timeout(3000)
    handle_notion_auth(page, context)
    page.wait_for_timeout(1000)
    # NOTE: no screenshot here — page.screenshot() can block 8s, Notion redraws cover strip during that time

    # Scroll to top so cover strip is at y≈0
    try:
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(800)
    except Exception:
        pass

    # Hover + click Change (milana-unmask toolbar — see docs/problems/notion-cover-upload)
    cover_clicked = _click_cover_change(page)

    if not cover_clicked:
        for sel in [
            'button:has-text("Change")',
            '[role="button"]:has-text("Change")',
            'button:has-text("Add cover")',
            '[role="button"]:has-text("Add cover")',
        ]:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=1500):
                    el.click()
                    page.wait_for_timeout(1500)
                    cover_clicked = True
                    print(f'  Clicked cover button via {sel}')
                    break
            except Exception:
                continue

    if not cover_clicked:
        print('  [0] Cover button not found — skipping (pipeline continues)')
        screenshot(page, '0_cover_btn_missing')
        return False

    screenshot(page, '0_cover_modal')
    uploaded = _upload_cover_file(page, cover_path)

    if not uploaded:
        print('  [0] Upload failed — skipping (pipeline continues)')
        screenshot(page, '0_cover_upload_failed')
        return False

    page.wait_for_timeout(1000)
    screenshot(page, '0_cover_done')

    try:
        page.keyboard.press('Escape')
        page.wait_for_timeout(500)
    except Exception:
        pass

    print('  Notion cover uploaded.')
    return True


def publish_as_template(page, context, page_id, product_slug):
    """
    Opens the Notion page, clicks Share, enables template duplication,
    and returns the template URL.
    """
    page_id_clean = page_id.replace('-', '')
    search_term = slug_to_title(product_slug)
    title_slug = search_term.replace(' ', '-')
    app_url = f'https://app.notion.com/p/{title_slug}-{page_id_clean}'
    fallback_url = f'https://www.notion.so/{page_id_clean}'

    print('\n  Ensuring Notion app is loaded...')
    ensure_notion_loaded(page, context)

    print(f'\n  Navigating to page: {search_term}')
    ok = navigate_to_notion_page(page, context, app_url, search_term)
    if not ok:
        ok = navigate_to_notion_page(page, context, fallback_url, search_term)
    if not ok:
        ok = quick_find_navigate(page, context, search_term)

    if not ok:
        print('  Could not navigate to page. Taking screenshot...')
        screenshot(page, 'nav_failed')
        return None

    page.wait_for_timeout(3000)
    handle_notion_auth(page, context)
    page.wait_for_timeout(2000)

    screenshot(page, 'root_page')

    # Click Share button
    share_clicked = False
    for sel in [
        '[data-testid="topbar-share-menu-button"]',
        'button:has-text("Share")',
        'div[role="button"]:has-text("Share")',
        'span:has-text("Share")',
        '[aria-label="Share"]',
    ]:
        try:
            btn = page.locator(sel).first
            btn.wait_for(state='visible', timeout=8000)
            btn.click()
            page.wait_for_timeout(1500)
            share_clicked = True
            print('    Clicked Share button')
            break
        except Exception:
            continue

    if not share_clicked:
        print('    Could not find Share button — skipping template publish')
        screenshot(page, 'share_not_found')
        return None

    screenshot(page, 'share_dialog')

    # In new Notion (app.notion.com), template options are under the "Publish" tab.
    # Only use [role="tab"] selectors here — "button:has-text('Publish')" would match
    # the action button inside the tab panel and skip the tab click entirely.
    for tab_sel in [
        '[role="tab"]:has-text("Publish")',
        'div[role="tab"]:has-text("Publish")',
    ]:
        try:
            tab = page.locator(tab_sel).first
            if tab.is_visible(timeout=2000):
                tab.click()
                page.wait_for_timeout(1000)
                print('    Switched to Publish tab')
                screenshot(page, 'publish_tab')
                break
        except Exception:
            continue

    # Click the blue "Publish" CTA inside the Publish tabpanel.
    # Scope to [role="tabpanel"] so we don't hit the tab itself or other page buttons.
    # Use JS .click() to bypass overlay/stale-element issues that fool Playwright .click().
    publish_clicked = False
    screenshot(page, 'pre_publish_cta')

    # JS: find the CTA inside the active tabpanel (exact text "Publish", not a tab)
    publish_clicked = page.evaluate("""() => {
        const panel = document.querySelector('[role="tabpanel"]');
        const root = panel || document.body;
        const btn = [...root.querySelectorAll('button, [role="button"]')]
            .find(el => {
                const t = (el.textContent || '').trim();
                const role = (el.getAttribute('role') || '');
                return t === 'Publish' && role !== 'tab';
            });
        if (btn) { btn.click(); return true; }
        return false;
    }""")

    if publish_clicked:
        page.wait_for_timeout(1500)
        print('    Clicked blue Publish CTA (JS, tabpanel scope)')
    else:
        # Playwright fallback — scoped to tabpanel, then unscoped with :not([role="tab"])
        for pub_sel in [
            '[role="tabpanel"] button:has-text("Publish")',
            '[role="tabpanel"] [role="button"]:has-text("Publish")',
            'button:has-text("Publish"):not([role="tab"])',
            '[role="button"]:has-text("Publish"):not([role="tab"])',
        ]:
            try:
                btn = page.locator(pub_sel).first
                if btn.is_visible(timeout=2000):
                    btn.evaluate('el => el.click()')
                    page.wait_for_timeout(1500)
                    publish_clicked = True
                    print(f'    Clicked Publish CTA via {pub_sel}')
                    break
            except Exception:
                continue

    # Verify publish took effect: wait for "Unpublish" button or "Published" badge (up to 8 s)
    if publish_clicked:
        for _w in range(8):
            try:
                if page.locator(
                    'button:has-text("Unpublish"), [role="button"]:has-text("Unpublish")'
                ).first.is_visible(timeout=800):
                    print('    Confirmed: Published (Unpublish button visible)')
                    break
                if page.get_by_text('Published', exact=True).first.is_visible(timeout=400):
                    print('    Confirmed: Published badge visible')
                    break
            except Exception:
                pass
            page.wait_for_timeout(1000)

    screenshot(page, 'after_publish_btn')

    # Also try old-style "Allow template duplication" toggle (older Notion UI)
    if not publish_clicked:
        for sel in [
            'text="Allow template duplication"',
            'text="Publish as template"',
            '[role="switch"][aria-label*="template"]',
            'div:has-text("Allow template duplication") [role="switch"]',
        ]:
            try:
                el = page.locator(sel).first
                el.wait_for(state='visible', timeout=2000)
                el.click()
                page.wait_for_timeout(1000)
                publish_clicked = True
                print('    Enabled template duplication (old UI)')
                break
            except Exception:
                continue

    # Enable "Allow duplicate as template" toggle (required for buyers)
    page.wait_for_timeout(1500)
    try:
        toggle = page.locator('div:has-text("duplicate as template") >> [role="switch"]').first
        if toggle.is_visible(timeout=3000):
            if toggle.get_attribute('aria-checked') != 'true':
                toggle.click()
                page.wait_for_timeout(1000)
                print('    Enabled "Allow duplicate as template"')
            else:
                print('    "Allow duplicate as template" already ON')
    except Exception:
        # Try alternate label
        try:
            toggle = page.locator('[role="switch"][aria-label*="template"]').first
            if toggle.is_visible(timeout=2000):
                if toggle.get_attribute('aria-checked') != 'true':
                    toggle.click()
                    page.wait_for_timeout(1000)
                    print('    Enabled template toggle (alt selector)')
        except Exception:
            print('    WARNING: "Allow duplicate as template" toggle not found')

    screenshot(page, 'after_publish')

    # Extract notion.site public URL — ONLY notion.site is a valid public/template URL.
    # app.notion.com/p/... is a private workspace URL — must NOT be saved as template_url.
    #
    # Strategy:
    #   1. Click "Copy link" button first — makes URL visible in input and copies to clipboard.
    #   2. Poll DOM broadly for up to 20 s (inputs, links, text nodes, data-testid).
    #   3. Fallback: read clipboard via navigator.clipboard.readText().

    # Step 1: try "Copy link" to activate the URL input and populate clipboard
    for copy_sel in [
        'button:has-text("Copy link")',
        '[role="button"]:has-text("Copy link")',
        'button:has-text("Copy")',
        '[role="button"]:has-text("Copy")',
    ]:
        try:
            btn = page.locator(copy_sel).first
            if btn.is_visible(timeout=1500):
                btn.click()
                page.wait_for_timeout(800)
                print('    Clicked Copy link button')
                break
        except Exception:
            continue

    _url_js = '''() => {
        const ns = v => v && String(v).includes('notion.site');
        // All inputs
        for (const inp of document.querySelectorAll('input')) {
            if (ns(inp.value)) return inp.value.trim();
        }
        // Links (href and text)
        for (const a of document.querySelectorAll('a')) {
            if (ns(a.href)) return a.href;
            const t = (a.textContent || '').trim();
            if (ns(t) && t.length < 200) return t;
        }
        // Text nodes anywhere in the page
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while ((node = walker.nextNode())) {
            const t = (node.nodeValue || '').trim();
            if (ns(t) && t.length < 200) return t;
        }
        // data-value / textContent on [data-testid] elements
        for (const el of document.querySelectorAll('[data-testid]')) {
            const v = el.getAttribute('data-value') || '';
            if (ns(v)) return v.trim();
            const t = (el.textContent || '').trim();
            if (ns(t) && t.length < 200) return t;
        }
        return null;
    }'''

    template_url = None
    for _attempt in range(20):
        try:
            href = page.evaluate(_url_js)
        except Exception:
            href = None
        if href:
            template_url = normalize_template_url(href, page_id_clean, title_slug) or href
            if template_url and template_url.startswith('https://'):
                print(f'    Got public URL: {template_url}')
                break
            template_url = None
        if _attempt == 4:
            screenshot(page, 'publish_url_poll')
        page.wait_for_timeout(1000)

    # Step 3: clipboard fallback (works if "Copy link" was clicked above)
    if not template_url:
        try:
            clip = page.evaluate("() => navigator.clipboard.readText()")
            if clip and 'notion.site' in clip:
                template_url = clip.strip()
                print(f'    Got public URL via clipboard: {template_url}')
        except Exception as e:
            print(f'    Clipboard read failed: {e}')

    template_url = normalize_template_url(template_url, page_id_clean, title_slug)

    if not template_url:
        print('    ERROR: No valid https notion.site URL — page not published or toggle missing')
        print(f'    Current URL: {page.url}')
        screenshot(page, 'publish_no_public_url')
    else:
        print(f'    Template URL: {template_url}')

    try:
        page.keyboard.press('Escape')
        page.wait_for_timeout(500)
    except Exception:
        pass

    return template_url


def get_existing_views(page):
    """Returns set of view tab names already in the database (lowercase)."""
    try:
        result = page.evaluate("""() => {
            return [...document.querySelectorAll('[role="tab"]')]
                .filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.top > 80 && r.top < 220 && r.width > 15 && r.height > 10;
                })
                .map(el => (el.textContent || '').trim().toLowerCase())
                .filter(t => t.length > 0);
        }""")
        return set(result) if result else set()
    except Exception:
        return set()


def reveal_add_view_button(page):
    """
    Hover the rightmost view tab to reveal the '+' (Add view) button.
    Returns bounding box dict of rightmost tab, or None.
    No x-range restriction — only filters by y so it works for any number of tabs.
    """
    box = page.evaluate("""() => {
        const tabs = [...document.querySelectorAll('[role="tab"]')]
            .filter(el => {
                const r = el.getBoundingClientRect();
                // Only filter by y: must be in the view tabs row
                return r.top > 80 && r.top < 220 && r.width > 15 && r.height > 10;
            });
        if (!tabs.length) return null;
        // Find the rightmost tab
        let best = null;
        for (const el of tabs) {
            const r = el.getBoundingClientRect();
            if (!best || r.right > best.right) {
                best = { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right };
            }
        }
        return best;
    }""")

    if box:
        tab_cx = box['x'] + box['width'] / 2
        tab_cy = box['y'] + box['height'] / 2
        page.mouse.move(tab_cx, tab_cy)
        page.wait_for_timeout(300)
        # Move past the tab's right edge to reveal "+"
        page.mouse.move(box['right'] + 25, tab_cy)
        page.wait_for_timeout(800)
        return box

    # Fallback via Playwright locators
    try:
        tabs = page.locator('[role="tab"]').all()
        positioned = []
        for tab in tabs:
            b = tab.bounding_box()
            if b and b['y'] > 80 and b['y'] < 220:
                positioned.append((b['x'] + b['width'], tab, b))
        if positioned:
            positioned.sort(key=lambda t: t[0])
            rightmost_edge, last_tab, last_box = positioned[-1]
            last_tab.hover()
            page.wait_for_timeout(400)
            page.mouse.move(rightmost_edge + 25, last_box['y'] + last_box['height'] / 2)
            page.wait_for_timeout(800)
            return last_box
    except Exception:
        pass
    return None


def click_view_type(page, view_name):
    """Pick a view type from the Add view dialog."""
    try:
        page.locator('[role="dialog"]:has-text("Loading")').wait_for(state='hidden', timeout=5000)
    except Exception:
        pass
    page.wait_for_timeout(500)

    for sel in [
        f'[role="dialog"] >> text="{view_name}"',
        f'[role="dialog"] [role="option"]:has-text("{view_name}")',
        f'div[role="option"]:has-text("{view_name}")',
        f'div[role="menuitem"]:has-text("{view_name}")',
        f'li:has-text("{view_name}")',
    ]:
        try:
            el = page.locator(sel).first
            el.wait_for(state='visible', timeout=3000)
            el.click()
            page.wait_for_timeout(1500)
            return True
        except Exception:
            continue
    raise TimeoutError(f'View type {view_name!r} not found in dialog')


def try_add_view(page, view_name):
    """Attempts to add a view to the currently open database."""
    # Skip if view already exists (avoids double-add on reruns)
    existing = get_existing_views(page)
    if view_name.lower() in existing:
        print(f'    Skipping {view_name} (already exists)')
        return True

    try:
        box = reveal_add_view_button(page)

        add_view_btn = None
        for sel in [
            '[role="button"][aria-label="Add view"]',
            'div[aria-label="Add view"]',
            'button[aria-label="Add view"]',
            'button[aria-label="Add a view"]',
            '[data-testid="views-tabs-add-view"]',
            '[data-testid*="add-view"]',
        ]:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=1500):
                    add_view_btn = el
                    break
            except Exception:
                continue

        if not add_view_btn:
            # JS: find by aria-label (button may now be in DOM after hover)
            found = page.evaluate("""() => {
                const btn = [...document.querySelectorAll('[role="button"], button, div')]
                    .find(b => {
                        const a = (b.getAttribute('aria-label') || '').toLowerCase();
                        return a === 'add view' || a === 'add a view';
                    });
                if (btn) { btn.click(); return true; }
                return false;
            }""")
            if found:
                page.wait_for_timeout(800)
            elif box:
                # Coordinate fallback: click right of rightmost tab
                click_x = box.get('right', box['x'] + box['width']) + 15
                click_y = box['y'] + box['height'] / 2
                page.mouse.click(click_x, click_y)
                page.wait_for_timeout(800)
                # Verify dialog appeared
                try:
                    page.locator('[role="dialog"]').first.wait_for(state='visible', timeout=2000)
                except Exception:
                    raise TimeoutError('No dialog after coordinate click')
            else:
                raise TimeoutError('Add view button not found')

        else:
            add_view_btn.click()
            page.wait_for_timeout(800)

        screenshot(page, f'addview_menu_{view_name}')

        click_view_type(page, view_name)

        for btn_text in ['Create view', 'Done', 'Add']:
            try:
                btn = page.locator(f'button:has-text("{btn_text}")').first
                if btn.is_visible(timeout=2000):
                    btn.click()
                    page.wait_for_timeout(1000)
                    break
            except Exception:
                pass

        print(f'    Added: {view_name} view')
        return True
    except Exception as e:
        print(f'    Could not auto-add {view_name}: {type(e).__name__}')
        return False


def setup_database_views(page, context, db_name, db_id, views_to_add):
    print(f'\n  Database: {db_name}')
    db_url = f'https://notion.so/{db_id.replace("-", "")}'

    ok = navigate_to_notion_page(page, context, db_url, db_name)
    if not ok:
        print(f'  Could not navigate to database: {db_name}')
        screenshot(page, f'db_nav_failed_{db_name[:20]}')
        return

    page.wait_for_timeout(2000)
    screenshot(page, f'db_{db_name}_before')

    for view_name in views_to_add:
        try_add_view(page, view_name)

    screenshot(page, f'db_{db_name}_after')
    print(f'  {db_name} done.')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/playwright_notion.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]

    for base in [f'products/draft/{slug}', f'products/ready/{slug}']:
        notion_path = f'{base}/notion_result.json'
        gumroad_path = f'{base}/gumroad_result.json'
        if os.path.exists(notion_path):
            product_dir = base
            break
    else:
        print(f'Error: notion_result.json not found for "{slug}"')
        sys.exit(1)

    with open(notion_path, encoding='utf-8') as f:
        notion = json.load(f)
    with open(gumroad_path, encoding='utf-8') as f:
        gumroad = json.load(f)

    page_id   = notion['notion_page_id'].replace('-', '')
    databases = notion.get('databases', {})

    print(f'\n{"=" * 55}')
    print(f'NOTION SETUP: {slug}')
    print(f'{"=" * 55}')

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp('http://localhost:9222')
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            # Use existing Notion tab — notion.so or app.notion.com
            existing_notion = None
            for p in context.pages:
                if 'notion.so' in p.url or 'app.notion.com' in p.url:
                    existing_notion = p
                    break
            page = existing_notion if existing_notion else context.new_page()
            print(f'  Connected to Chrome ({"existing Notion tab" if existing_notion else "new tab"}).')
            grant_notion_permissions(context)
        except Exception as e:
            print(f'\n  ERROR: Chrome not on port 9222.')
            print(f'  Open Chrome via RODE51-Chrome shortcut first.')
            sys.exit(1)

        # Step 0: Upload Notion cover
        print('\n[0] Uploading Notion cover...')
        cover_ok = upload_notion_cover(page, context, page_id, slug)

        # Step 1: Publish as template
        print('\n[1] Publishing as template...')
        template_url = publish_as_template(page, context, page_id, slug)
        if not template_url:
            print('\n  FATAL: No notion.site URL obtained — page not published.')
            screenshot(page, 'fatal_no_template_url')
            sys.exit(1)

        # Step 2: Add views to databases
        print(f'\n[2] Adding views to {len(databases)} database(s)...')
        for db_name, db_id in databases.items():
            views = VIEW_MAP.get('default', ['Board', 'Calendar'])
            for key in VIEW_MAP:
                if key.lower() in db_name.lower():
                    views = VIEW_MAP[key]
                    break
            setup_database_views(page, context, db_name, db_id, views)

        # Step 3: Save template URL
        gumroad['notion_template_url'] = template_url
        with open(gumroad_path, 'w', encoding='utf-8') as f:
            json.dump(gumroad, f, indent=2, ensure_ascii=False)
        notion['notion_template_url'] = template_url
        with open(notion_path, 'w', encoding='utf-8') as f:
            json.dump(notion, f, indent=2, ensure_ascii=False)
        print(f'\n  Template URL saved: {template_url}')

        print(f'\n{"=" * 55}')
        print('SUMMARY:')
        print(f'  Cover upload : {"OK" if cover_ok else "FAIL"}')
        print(f'  Publish      : OK  ({template_url})')
        print(f'  Views        : queued for {len(databases)} database(s)')
        print('Notion setup complete.')
        print(f'{"=" * 55}')

    return template_url


if __name__ == '__main__':
    main()
