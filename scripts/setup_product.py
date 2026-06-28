#!/usr/bin/env python3
"""
setup_product.py — Full automation for one product. Zero manual steps required.

What it does:
  1. Notion: publishes as template + adds Board/Calendar/Timeline views
  2. Gumroad: uploads thumbnail + publishes
  3. Promote: blog post + Pinterest

Requirement: Chrome must be open via RODE51-Chrome shortcut (debug port 9222).

Usage:
  python scripts/setup_product.py <slug>
"""

import datetime
import json
import subprocess
import sys
import os
import shutil
from pathlib import Path

# Windows console: avoid UnicodeEncodeError on arrows/emojis in child output
if sys.platform == 'win32':
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')


def run(cmd, label):
    print(f'\n{"-" * 55}')
    print(f'[{label}]')
    print(f'{"-" * 55}')
    result = subprocess.run(cmd)
    return result.returncode == 0


def ensure_images(slug, py):
    """Generate or copy all cover images before Playwright steps."""
    draft = Path(f'products/draft/{slug}')
    ready = Path(f'products/ready/{slug}')

    for fname in ['gumroad-thumb.png', 'notion-cover.png']:
        if not (draft / fname).exists() and (ready / fname).exists():
            shutil.copy(ready / fname, draft / fname)
            print(f'  Copied {fname} from ready/')

    if not (draft / 'gumroad-thumb.png').exists() or not (draft / 'notion-cover.png').exists():
        run([py, 'scripts/pillow_pin.py', slug], 'Generate images')


def get_template_url(slug):
    """Read template URL saved by playwright_notion.py"""
    for base in [f'products/draft/{slug}', f'products/ready/{slug}']:
        for fname in ['notion_result.json', 'gumroad_result.json']:
            path = f'{base}/{fname}'
            if os.path.exists(path):
                with open(path, encoding='utf-8') as f:
                    data = json.load(f)
                url = data.get('notion_template_url')
                if url:
                    return url
    return None


def log_step(slug, msg):
    log_path = Path(f'products/draft/{slug}/setup.log')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/setup_product.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]
    py   = sys.executable

    print(f'\n{"=" * 55}')
    print(f'SETUP PRODUCT: {slug}')
    print(f'{"=" * 55}')

    # 0. Create Notion page + Gumroad draft (if not yet done)
    # For upgrades: if notion_result.json is missing (Notion page was deleted),
    # re-run publish even if gumroad_result.json exists (product stays on Gumroad).
    gumroad_exists = any(
        os.path.exists(f'{base}/gumroad_result.json')
        for base in [f'products/ready/{slug}', f'products/draft/{slug}']
    )
    notion_exists = any(
        os.path.exists(f'{base}/notion_result.json')
        for base in [f'products/ready/{slug}', f'products/draft/{slug}']
    )

    if gumroad_exists and notion_exists:
        print(f'\n  Draft found — skipping publish step')
    elif gumroad_exists and not notion_exists:
        print('\n  Notion page missing (deleted?) — re-creating Notion only...')
        ok = run([py, 'scripts/notion_create.py', slug], '0/3  Notion — recreate')
    elif notion_exists and not gumroad_exists:
        print('\n  Gumroad draft missing — creating Gumroad only (idempotent)...')
        ok = run([py, 'scripts/gumroad_create.py', slug], '0/3  Gumroad — create draft')
        if not ok:
            print('  Gumroad create failed. Check output above.')
            sys.exit(1)
    else:
        print('\n[0/3  Notion + Gumroad — create draft]')
        ok = run([py, 'scripts/publish.py', slug], '0/3  Notion + Gumroad — create draft')
        if not ok:
            print('  Publish step failed. Check output above.')
            sys.exit(1)

    # 1. Notion: publish as template + add views + upload cover
    ensure_images(slug, py)
    log_step(slug, 'STEP playwright_notion START')
    ok = run([py, 'scripts/playwright_notion.py', slug],
             '1/3  Notion — publish template + add views + cover')
    if not ok:
        log_step(slug, 'STEP playwright_notion FAIL')
        log_step(slug, 'ABORT exit=1')
        print('  Notion step failed — check debug_screenshots/ and setup.log')
        sys.exit(1)
    log_step(slug, 'STEP playwright_notion OK')

    # 2. Use template URL saved by playwright_notion.py
    template_url = get_template_url(slug)
    if template_url:
        print(f'\n  Template URL: {template_url}')
        subprocess.run([py, 'scripts/set_template_url.py', slug, template_url])
    else:
        print('\n  WARNING: Template URL not found in result files.')

    # 3. Gumroad: upload thumbnail + publish
    log_step(slug, 'STEP playwright_gumroad START')
    ok = run([py, 'scripts/playwright_gumroad.py', slug],
             '2/3  Gumroad - upload thumbnail + publish')
    if not ok:
        log_step(slug, 'STEP playwright_gumroad FAIL')
        log_step(slug, 'ABORT exit=1')
        print('  Gumroad step failed — check debug_screenshots/ and setup.log')
        sys.exit(1)
    log_step(slug, 'STEP playwright_gumroad OK')

    # 4. Promote
    log_step(slug, 'STEP promote START')
    ok = run([py, 'scripts/promote.py', slug], '3/3  Blog post -> GitHub Pages')
    log_step(slug, f'STEP promote {"OK" if ok else "FAIL"}')

    print(f'\n{"=" * 55}')
    print(f'SETUP COMPLETE: {slug}')
    print(f'{"=" * 55}')
    log_step(slug, 'SETUP COMPLETE')
    print('\nCheck: https://rodeshop.gumroad.com')


if __name__ == '__main__':
    main()
