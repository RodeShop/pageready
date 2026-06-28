#!/usr/bin/env python3
"""
check_notion_auth.py — Checks if Notion workspace is accessible in Chrome.
Exits with code 0 (OK) or 1 (needs auth).
"""
import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    try:
        browser = pw.chromium.connect_over_cdp('http://localhost:9222')
    except Exception:
        print('ERROR: Chrome not on port 9222')
        sys.exit(2)

    ctx = browser.contexts[0]

    # Reuse existing notion tab or create a new one
    notion_tab = None
    for p in ctx.pages:
        if 'notion.so' in p.url:
            notion_tab = p
            break
    if not notion_tab:
        notion_tab = ctx.new_page()

    # Navigate to notion root — if logged in it redirects to workspace
    notion_tab.goto('https://www.notion.so', wait_until='domcontentloaded', timeout=20000)
    notion_tab.wait_for_timeout(5000)

    url = notion_tab.url
    title = notion_tab.title()

    # Notion redirects logged-in users to workspace URL (contains workspace slug)
    on_workspace = (
        'notion.so' in url and
        url not in ('https://www.notion.so/', 'https://www.notion.so')
    )

    # Also check: not showing marketing page
    is_marketing = any(text in title for text in ['Notion – The all-in-one', 'Notion - The', 'Where teams'])

    # Check for popup
    try:
        popup = notion_tab.get_by_text('almost there', exact=False).is_visible(timeout=1000)
    except Exception:
        popup = False

    if on_workspace and not is_marketing and not popup:
        print('AUTH_OK')
        sys.exit(0)
    else:
        print(f'AUTH_NEEDED (url={url[:60]}, title={title[:40]}, popup={popup})')
        sys.exit(1)
