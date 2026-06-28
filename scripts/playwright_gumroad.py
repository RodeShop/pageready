#!/usr/bin/env python3
"""
playwright_gumroad.py — Automates Gumroad product setup via browser.

What it does:
  1. Opens the product edit page (already logged in via Chrome profile)
  2. Uploads gumroad-thumb.png as cover image
  3. Uploads user-guide.md as product file
  4. Publishes the product

Usage:
  python scripts/playwright_gumroad.py <slug>

First time setup:
  pip install playwright
  playwright install chromium
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print('Playwright not installed. Run: pip install playwright && playwright install chromium')
    sys.exit(1)


DEBUG_DIR = Path('debug_screenshots')
DEBUG_DIR.mkdir(exist_ok=True)


def screenshot(page, name):
    try:
        path = DEBUG_DIR / f'{name}.png'
        page.screenshot(path=str(path), full_page=False, timeout=10000)
        print(f'  Screenshot: {path}')
    except Exception:
        pass


def wait_and_find(page, selectors, timeout=10000):
    """Try multiple selectors, return first match."""
    for sel in selectors:
        try:
            el = page.locator(sel).first
            el.wait_for(state='visible', timeout=timeout)
            return el
        except Exception:
            continue
    return None


def switch_to_tab(page, tab_name):
    """
    Switch to a tab on the Gumroad product edit page.
    Uses exact text match to avoid clicking sidebar "Products" link when targeting "Product" tab.
    """
    # Exact match selectors — scoped to likely tab areas, not sidebar
    for sel in [
        f'[role="tab"]:text-is("{tab_name}")',
        f'nav a:text-is("{tab_name}")',
    ]:
        try:
            tab = page.locator(sel).first
            if tab.is_visible(timeout=2000):
                tab.click()
                page.wait_for_timeout(1500)
                return True
        except Exception:
            continue

    # JS fallback: find links/buttons at the top of the page with exact text
    found = page.evaluate(f"""() => {{
        const exact = Array.from(document.querySelectorAll('a, button, [role="tab"]'))
            .find(el => {{
                const t = el.textContent.trim();
                const r = el.getBoundingClientRect();
                // Must be near top of page (tab bar), exact text match
                return t === '{tab_name}' && r.top < 200 && r.top > 0;
            }});
        if (exact) {{ exact.click(); return true; }}
        return false;
    }}""")
    if found:
        page.wait_for_timeout(1500)
    return bool(found)


def _scroll_to_section(page, heading):
    page.evaluate(f"""() => {{
        const el = [...document.querySelectorAll('h2, h3, label, div, span')]
            .find(e => e.textContent.trim() === '{heading}');
        if (el) el.scrollIntoView({{ block: 'center' }});
    }}""")
    page.wait_for_timeout(800)


def _cover_has_image(page):
    try:
        return page.evaluate("""() => {
            return [...document.querySelectorAll('img, video')].some(el => {
                const r = el.getBoundingClientRect();
                return r.width > 120 && r.height > 80 && r.top > 80 && r.top < 900;
            });
        }""")
    except Exception:
        return False


def _set_files_on_input(page, thumb_path, accept_match):
    """Set files on first input[type=file] whose accept attribute matches."""
    for inp in page.locator('input[type="file"]').all():
        accept = (inp.get_attribute('accept') or '').lower()
        if accept_match(accept):
            inp.set_input_files(str(thumb_path))
            return True
    return False


def upload_thumbnail(page, thumb_path):
    print('\n  [1/3] Uploading Cover + Thumbnail images...')
    print(f'  File: {thumb_path} (1600×900 Direction D)')

    switch_to_tab(page, 'Product')
    try:
        page.wait_for_load_state('networkidle', timeout=12000)
    except Exception:
        pass
    page.wait_for_timeout(2000)

    cover_ok = False
    _scroll_to_section(page, 'Cover')
    try:
        tab = page.locator('[role="tab"]:has-text("Computer files")').first
        if tab.is_visible(timeout=1500):
            tab.click()
            page.wait_for_timeout(500)
    except Exception:
        pass

    try:
        btn = page.get_by_role('button', name='Upload images or videos')
        btn.scroll_into_view_if_needed()
        btn.click()
        page.wait_for_timeout(800)
        # Gumroad: no native filechooser — hidden input appears after click
        cover_ok = _set_files_on_input(
            page, thumb_path,
            lambda a: 'mov' in a or 'mp4' in a or 'mpeg' in a,
        )
        if cover_ok:
            print('  Cover uploaded (input after button click).')
        page.wait_for_timeout(6000)
    except Exception as e:
        print(f'  Cover upload failed: {e}')

    screenshot(page, '1_cover_attempt')

    thumb_ok = False
    _scroll_to_section(page, 'Thumbnail')
    try:
        thumb_trigger = page.locator('label').filter(has_text='Upload').last
        if not thumb_trigger.is_visible(timeout=2000):
            thumb_trigger = page.get_by_role('button', name='+ Upload')
        thumb_trigger.scroll_into_view_if_needed()
        thumb_trigger.click()
        page.wait_for_timeout(800)
        thumb_ok = _set_files_on_input(
            page, thumb_path,
            lambda a: a in ('.jpeg,.jpg,.png,.gif,.webp',) or (
                'webp' in a and 'mov' not in a and 'mp4' not in a
            ),
        )
        if thumb_ok:
            print('  Thumbnail uploaded (input after label click).')
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f'  Thumbnail upload failed: {e}')

    screenshot(page, '1_thumb_attempt')

    try:
        save = page.locator('button:has-text("Save changes")').first
        if save.is_visible(timeout=2000):
            save.click()
            page.wait_for_timeout(3000)
            print('  Saved changes on Product tab.')
    except Exception:
        pass

    if cover_ok or _cover_has_image(page):
        return True

    screenshot(page, '1_cover_upload_failed')
    print('  WARNING: Cover upload failed — UI still empty.')
    return False


def upload_file(page, guide_path, edit_url=''):
    import re as _re
    print('\n  [2/3] Uploading user guide...')

    # Content tab is at /edit/content — navigate there directly
    if edit_url:
        content_url = _re.sub(r'/edit(/.*)?$', '/edit/content', edit_url)
        page.goto(content_url, wait_until='domcontentloaded', timeout=20000)
        try:
            page.wait_for_load_state('networkidle', timeout=8000)
        except Exception:
            pass
        page.wait_for_timeout(2000)
        print(f'  Content URL: {page.url}')

    # Try file chooser via "Upload files" button in the Content tab toolbar
    try:
        with page.expect_file_chooser(timeout=6000) as fc_info:
            upload_btn = wait_and_find(page, [
                'button:has-text("Upload files")',
                'button:has-text("Upload your files")',
                'a:has-text("Upload your files")',
            ], timeout=4000)
            if upload_btn:
                upload_btn.click()
            else:
                raise Exception('No upload button found on Content tab')
        fc_info.value.set_files(str(guide_path))
        page.wait_for_timeout(5000)
        print('  User guide uploaded.')
        return True
    except Exception:
        pass

    # Fallback: set files on any non-image/audio file input
    try:
        for inp in page.locator('input[type="file"]').all():
            accept = inp.get_attribute('accept') or ''
            if accept in ['.jpeg,.jpg,.png,.gif,.webp', '.mp3,.wav,.flac,.wma,.aac,.m4a']:
                continue
            if 'mov' in accept or 'mp4' in accept:
                continue  # Skip Cover input
            inp.set_input_files(str(guide_path))
            page.wait_for_timeout(4000)
            print(f'  User guide uploaded (direct, accept={accept[:40]}).')
            return True
    except Exception as e:
        print(f'  WARNING: File upload fallback failed: {e}')

    print('  WARNING: Could not upload user guide — skipping.')
    return False


def publish_product(page):
    print('\n  [3/3] Publishing product...')

    # Gumroad publish flow:
    # Product tab → "Save and continue" → Content tab → "Publish and continue" or top-right "Publish"
    # OR: Share tab → "Publish" toggle

    # Step 1: save Product tab (if still there) → moves to Content tab
    switch_to_tab(page, 'Product')
    page.wait_for_timeout(500)
    try:
        save_btn = page.locator('button:has-text("Save and continue")').first
        if save_btn.is_visible(timeout=3000):
            save_btn.click()
            page.wait_for_timeout(2500)
            print('  Saved Product tab → Content tab.')
    except Exception:
        pass

    screenshot(page, '5_before_publish')
    published = False

    # Step 2: Try top-right Publish button (visible on all tabs)
    for sel in [
        'button:has-text("Publish and continue")',
        'button:has-text("Publish")',
        'button:has-text("Go live")',
        '[data-testid="publish-button"]',
    ]:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                el.click()
                page.wait_for_timeout(2500)
                published = True
                print(f'  Published via: {sel}')
                break
        except Exception:
            continue

    # Step 3: Try Share tab if not yet published
    if not published:
        switch_to_tab(page, 'Share')
        page.wait_for_timeout(1000)
        for sel in ['button:has-text("Publish")', 'button:has-text("Go live")', 'text=Unpublished']:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=2000):
                    el.click()
                    page.wait_for_timeout(2000)
                    published = True
                    print(f'  Published via Share tab: {sel}')
                    break
            except Exception:
                continue

    # Final save
    try:
        save_btn = page.locator('button:has-text("Save changes"), button:has-text("Save and continue")').first
        if save_btn.is_visible(timeout=2000):
            save_btn.click()
            page.wait_for_timeout(2000)
    except Exception:
        pass

    screenshot(page, '6_after_publish')

    if published:
        print('  Product published.')
    else:
        print('  WARNING: Could not auto-publish.')
        print('  Go to gumroad.com/products and publish manually.')

    return published


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/playwright_gumroad.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]

    # Find product files
    for base in [f'products/ready/{slug}', f'products/draft/{slug}']:
        if os.path.exists(f'{base}/gumroad_result.json'):
            product_dir = base
            break
    else:
        print(f'Error: gumroad_result.json not found for "{slug}"')
        sys.exit(1)

    with open(f'{product_dir}/gumroad_result.json', encoding='utf-8') as f:
        result = json.load(f)

    product_name = result.get('title', '')

    # Find thumb and guide in ready/ or draft/ — whichever has the file
    search_dirs = [f'products/ready/{slug}', f'products/draft/{slug}']
    def find_file(filename):
        for d in search_dirs:
            p = Path(d) / filename
            if p.exists():
                return p.resolve()
        return (Path(product_dir) / filename).resolve()

    thumb_path = find_file('gumroad-thumb.png')
    guide_path = find_file('user-guide.md')

    print(f'\n{"=" * 55}')
    print(f'GUMROAD SETUP: {slug}')
    print(f'{"=" * 55}')

    # Check files exist
    for p in [thumb_path, guide_path]:
        if not p.exists():
            print(f'Error: file not found: {p}')
            sys.exit(1)

    with sync_playwright() as pw:
        CDP_URL = 'http://localhost:9222'
        try:
            browser = pw.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.pages[0] if context.pages else context.new_page()
            print('  Connected to Chrome (using your existing session)')
        except Exception as e:
            print(f'\n  ERROR: Could not connect to Chrome on port 9222.')
            print(f'  Details: {e}')
            sys.exit(1)

        def find_edit_url_from_products(product_slug, product_title, product_id=None):
            """Navigate to gumroad.com/products and find edit link from the product list.
            Gumroad UI uses short slugs (e.g. pamwqu), not API product_id — never guess URL."""
            page.goto('https://gumroad.com/products', wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(3000)
            name_fragment = (product_title or product_slug).replace('notion-', '').replace('-', ' ').lower()
            slug_fragment = product_slug.lower()
            return page.evaluate(f"""() => {{
                const links = [...document.querySelectorAll('a[href*="/edit"]')];
                const byName = links.find(a =>
                    (a.textContent || '').toLowerCase().includes('{name_fragment}')
                );
                if (byName) return byName.href;
                const bySlug = links.find(a =>
                    a.href.toLowerCase().includes('{slug_fragment}')
                );
                if (bySlug) return bySlug.href;
                const byId = links.find(a =>
                    '{product_id or ""}' && a.href.includes('{product_id or ""}')
                );
                return byId ? byId.href : null;
            }}""")

        product_id = result.get('gumroad_product_id', '')

        # Resolve edit URL — prefer product_id-based URL (immune to stale app.gumroad.com URLs)
        edit_url = result.get('gumroad_edit_url', '')
        if edit_url:
            edit_url = edit_url.replace('app.gumroad.com', 'gumroad.com')

        # Navigate and check for "Page not found" — re-discover via product ID if stale
        if edit_url:
            page.goto(edit_url, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(2000)
            try:
                if page.locator('text=Page not found').is_visible(timeout=1500):
                    print('  Stored edit URL invalid — re-discovering via product ID...')
                    edit_url = None
            except Exception:
                pass

        if not edit_url:
            print('  Finding product edit URL from products list...')
            edit_url = find_edit_url_from_products(slug, product_name, product_id)

        if not edit_url:
            print('  ERROR: Could not resolve edit URL. Open gumroad.com/products in Chrome factory.')
            sys.exit(1)

        # Navigate to edit page (might already be there if URL was valid)
        if page.url != edit_url:
            page.goto(edit_url, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(2000)
        try:
            if page.locator('text=Page not found').is_visible(timeout=1500):
                print('  Edit URL still invalid — re-scanning products list...')
                edit_url = find_edit_url_from_products(slug, product_name, product_id)
                if not edit_url:
                    sys.exit(1)
                page.goto(edit_url, wait_until='domcontentloaded', timeout=20000)
                page.wait_for_timeout(2000)
        except Exception:
            pass
        print(f'  Edit page: {page.url}')

        # Persist UI edit URL (short slug) — API product_id alone is not enough for /edit
        ui_edit = page.url.split('?')[0]
        if '/edit' in ui_edit and ui_edit != result.get('gumroad_edit_url'):
            result['gumroad_edit_url'] = ui_edit
            result_path = Path(product_dir) / 'gumroad_result.json'
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f'  Saved edit URL: {ui_edit}')

        thumb_ok = upload_thumbnail(page, thumb_path)
        if not thumb_ok:
            print('  FATAL: Thumbnail upload failed. Exiting.')
            screenshot(page, 'fatal_thumb_failed')
            sys.exit(1)

        guide_ok = upload_file(page, guide_path, edit_url)
        pub_ok = publish_product(page)

        print(f'\n{"=" * 55}')
        print('SUMMARY:')
        print(f'  Cover/Thumb  : {"OK" if thumb_ok else "FAIL"}')
        print(f'  Guide upload : {"OK" if guide_ok else "FAIL"}  ({guide_path.name})')
        print(f'  Published    : {"OK" if pub_ok else "FAIL"}')
        print(f'Done. Check: {result.get("gumroad_short_url", edit_url)}')
        print(f'Screenshots saved to: {DEBUG_DIR}/')
        print(f'{"=" * 55}')

        # Don't close Chrome — user opened it, user closes it


if __name__ == '__main__':
    main()
