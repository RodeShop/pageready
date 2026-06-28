#!/usr/bin/env python3
"""One-shot: connect to Chrome CDP and dump add-view button selectors."""
import json
import sys
from playwright.sync_api import sync_playwright

DB_URL = sys.argv[1] if len(sys.argv) > 1 else 'https://app.notion.com/p/38c8515aba6581cca445ea2a76185014'

with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = None
    for p in ctx.pages:
        if 'app.notion.com/p/' in p.url and 'notion.so' not in p.url:
            page = p
            break
    if not page:
        page = ctx.new_page()

    print(f'Using tab: {page.url[:80]}')
    page.goto(DB_URL, wait_until='domcontentloaded', timeout=30000)
    page.wait_for_timeout(5000)

    # Hover view tabs area
    for sel in ['[role="tab"]', 'button:has-text("Default view")', '[role="tab"]:has-text("Default")']:
        try:
            tab = page.locator(sel).first
            if tab.is_visible(timeout=2000):
                box = tab.bounding_box()
                print(f'Found tab via {sel!r}, box={box}')
                tab.hover()
                page.wait_for_timeout(1000)
                break
        except Exception as e:
            print(f'  tab {sel!r}: {e}')

    # Also hover to the right of tabs
    try:
        tabs = page.locator('[role="tab"]').all()
        if tabs:
            last = tabs[-1]
            box = last.bounding_box()
            if box:
                x = box['x'] + box['width'] + 20
                y = box['y'] + box['height'] / 2
                print(f'Hovering at ({x}, {y}) right of last tab')
                page.mouse.move(x, y)
                page.wait_for_timeout(1000)
    except Exception as e:
        print(f'  mouse hover: {e}')

    # Dump all buttons with aria-label or text containing view/add/+
    buttons = page.evaluate("""() => {
        const out = [];
        for (const el of document.querySelectorAll('button, [role="button"], div[tabindex="0"]')) {
            const aria = el.getAttribute('aria-label') || '';
            const text = (el.textContent || '').trim().slice(0, 40);
            const testid = el.getAttribute('data-testid') || '';
            const cls = (el.className || '').toString().slice(0, 60);
            const vis = el.offsetParent !== null && getComputedStyle(el).visibility !== 'hidden';
            const low = (aria + text + testid).toLowerCase();
            if (vis && (low.includes('view') || low.includes('add') || text === '+' || aria === '+' ||
                testid.includes('view') || aria.includes('New'))) {
                out.push({tag: el.tagName, aria, text, testid, cls, rect: el.getBoundingClientRect().toJSON()});
            }
        }
        return out;
    }""")
    print('\n=== Relevant buttons ===')
    print(json.dumps(buttons, indent=2))

    # All aria-labels on page with "view"
    labels = page.evaluate("""() => {
        return [...document.querySelectorAll('[aria-label]')]
            .filter(el => (el.getAttribute('aria-label')||'').toLowerCase().includes('view'))
            .map(el => ({
                aria: el.getAttribute('aria-label'),
                tag: el.tagName,
                testid: el.getAttribute('data-testid'),
                visible: el.offsetParent !== null,
            }));
    }""")
    print('\n=== aria-label contains view ===')
    print(json.dumps(labels, indent=2))
