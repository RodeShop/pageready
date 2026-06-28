#!/usr/bin/env python3
"""
debug_selectors.py — Connects to Chrome, takes screenshots + saves HTML
so we can find the right selectors for Gumroad and Notion.

Usage:
  1. Run start_chrome_debug.bat first
  2. Log in to Gumroad and Notion in that Chrome
  3. python scripts/debug_selectors.py <slug>
"""

import json, os, sys
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

DEBUG = Path('debug_screenshots')
DEBUG.mkdir(exist_ok=True)


def save(page, name):
    png = DEBUG / f'{name}.png'
    html = DEBUG / f'{name}.html'
    try:
        page.screenshot(path=str(png), full_page=False, timeout=15000)
    except Exception as e:
        print(f'  Screenshot failed ({e.__class__.__name__}), trying viewport only...')
        try:
            page.screenshot(path=str(png), full_page=False, timeout=30000)
        except Exception as e2:
            print(f'  Screenshot skipped: {e2}')
    try:
        html.write_text(page.content(), encoding='utf-8')
    except Exception as e:
        print(f'  HTML save failed: {e}')
    print(f'  Saved: {png}  +  {name}.html')


def inspect_inputs(page, label):
    inputs = page.locator('input[type="file"]').all()
    print(f'\n  [{label}] File inputs found: {len(inputs)}')
    for i, inp in enumerate(inputs):
        accept = inp.get_attribute('accept') or '(any)'
        name   = inp.get_attribute('name') or '-'
        pid    = inp.get_attribute('id') or '-'
        print(f'    [{i}] accept={accept}  name={name}  id={pid}')


def inspect_buttons(page, label, keyword=None):
    btns = page.locator('button').all()
    print(f'\n  [{label}] Buttons{" matching "+repr(keyword) if keyword else ""}:')
    for btn in btns:
        try:
            txt = (btn.inner_text() or '').strip()[:60]
            if not txt:
                continue
            if keyword and keyword.lower() not in txt.lower():
                continue
            aria = btn.get_attribute('aria-label') or ''
            pid  = btn.get_attribute('id') or ''
            cls  = (btn.get_attribute('class') or '')[:40]
            print(f'    "{txt}"  aria={aria!r}  id={pid!r}  class={cls!r}')
        except Exception:
            pass


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/debug_selectors.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]

    # Load IDs
    for base in [f'products/ready/{slug}', f'products/draft/{slug}']:
        gr = f'{base}/gumroad_result.json'
        nr = f'{base}/notion_result.json'
        if os.path.exists(gr):
            with open(gr) as f: gumroad = json.load(f)
            with open(nr) as f: notion  = json.load(f)
            break
    else:
        print('Error: result JSONs not found'); sys.exit(1)

    product_id = gumroad['gumroad_product_id']
    page_id    = notion['notion_page_id'].replace('-', '')
    databases  = notion.get('databases', {})

    gumroad_url = f'https://app.gumroad.com/products/{quote(product_id, safe="")}/edit'
    notion_url  = f'https://notion.so/{page_id}'

    print('\nConnecting to Chrome on port 9222...')
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp('http://localhost:9222')
            ctx  = browser.contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            print('Connected.')
        except Exception as e:
            print(f'ERROR: {e}\nRun start_chrome_debug.bat first.'); sys.exit(1)

        # ── GUMROAD ────────────────────────────────────────────
        print(f'\n{"="*50}')
        print(f'GUMROAD: {gumroad_url}')
        print(f'{"="*50}')
        page.goto(gumroad_url, wait_until='domcontentloaded', timeout=30000)
        page.wait_for_timeout(3000)

        # Если открылась страница логина — ждём
        if 'Log in' in page.title() or page.locator('text=Login').count() > 0:
            print('\n  *** Gumroad: нужен вход! ***')
            print('  Войди в Gumroad в открытом окне Chrome.')
            print('  Нажми Enter здесь после входа...')
            input()
            page.wait_for_timeout(3000)

        save(page, 'gumroad_edit')
        inspect_inputs(page, 'gumroad')
        inspect_buttons(page, 'gumroad', keyword=None)

        # Look for cover/thumbnail area
        cover_sels = [
            '[data-testid*="cover"]', '[data-testid*="thumbnail"]',
            '[class*="cover"]', '[class*="thumbnail"]',
            'label[for*="cover"]', 'label[for*="image"]',
        ]
        print('\n  Cover/thumbnail elements:')
        for sel in cover_sels:
            els = page.locator(sel).all()
            if els:
                for el in els[:2]:
                    try:
                        tag = el.evaluate('e => e.tagName')
                        cls = (el.get_attribute('class') or '')[:50]
                        print(f'    {sel}  tag={tag}  class={cls!r}')
                    except Exception:
                        pass

        # ── NOTION DATABASES ───────────────────────────────────
        for db_name, db_id in list(databases.items())[:2]:
            db_id_clean = db_id.replace('-', '')
            db_url = f'https://notion.so/{db_id_clean}'

            print(f'\n{"="*50}')
            print(f'NOTION DB: {db_name}  ->  {db_url}')
            print(f'{"="*50}')
            page.goto(db_url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(5000)

            save(page, f'notion_{db_name}')

            # Look for "add view" button
            view_sels = [
                '[role="button"][aria-label="Add view"]',
                'div[aria-label="Add view"]',
                'button[aria-label*="view"]',
                '[data-testid*="add-view"]',
            ]
            print(f'\n  View-related elements in {db_name}:')
            for sel in view_sels:
                els = page.locator(sel).all()
                if els:
                    for el in els[:3]:
                        try:
                            txt = (el.inner_text() or '').strip()[:40]
                            aria = el.get_attribute('aria-label') or ''
                            print(f'    sel={sel!r}  text={txt!r}  aria={aria!r}')
                        except Exception:
                            pass

            inspect_buttons(page, db_name, keyword='view')
            inspect_buttons(page, db_name, keyword='add')

        print(f'\n{"="*50}')
        print(f'Done. Open debug_screenshots/ to see results.')
        print(f'Share the screenshots with Claude to get correct selectors.')
        print(f'{"="*50}')
        input('\nPress Enter to close...')


if __name__ == '__main__':
    main()
