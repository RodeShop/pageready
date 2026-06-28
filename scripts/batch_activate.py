#!/usr/bin/env python3
"""
batch_activate.py — Reads PENDING_ACTIVATION.md and activates all ready products.

For each row where notion_template_url is filled:
  1. Runs set_template_url.py <slug> <url>
  2. Runs promote.py <slug>
  3. Marks row as done in PENDING_ACTIVATION.md

Usage: python scripts/batch_activate.py
"""

import os
import re
import subprocess
import sys

PENDING_FILE = 'PENDING_ACTIVATION.md'


def parse_pending(text):
    """Parse the activation table, return list of (slug, notion_page_url, notion_template_url)."""
    rows = []
    in_table = False
    for line in text.splitlines():
        if '| slug |' in line:
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and line.startswith('|'):
            cols = [c.strip() for c in line.strip('|').split('|')]
            if len(cols) >= 4:
                slug, page_url, template_url, status = cols[0], cols[1], cols[2], cols[3]
                if slug and slug != '_пусто — МиМо добавляет сюда_' and template_url:
                    rows.append({'slug': slug, 'page_url': page_url,
                                 'template_url': template_url, 'status': status})
        elif in_table and line.startswith('##'):
            break
    return rows


def mark_done(text, slug, gumroad_url):
    """Remove slug from pending table, add to activated table."""
    lines = text.splitlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.startswith('|') and f'| {slug} |' in line and 'notion-' in line:
            skip = True
        else:
            new_lines.append(line)
            if '## Активированы' in line:
                skip = False

    result = '\n'.join(new_lines)

    from datetime import date
    entry = f'| {slug} | {gumroad_url} | {date.today()} |'
    result = result.replace(
        '| notion-freelance-client-tracker |',
        f'| notion-freelance-client-tracker |'
    )
    lines2 = result.splitlines()
    for i, line in enumerate(lines2):
        if '## Активированы' in line:
            j = i + 1
            while j < len(lines2) and (lines2[j].startswith('|') or lines2[j].strip() == ''):
                j += 1
            lines2.insert(j, entry)
            break
    return '\n'.join(lines2)


def main():
    if not os.path.exists(PENDING_FILE):
        print(f'Not found: {PENDING_FILE}')
        sys.exit(1)

    with open(PENDING_FILE, encoding='utf-8') as f:
        text = f.read()

    pending = parse_pending(text)

    if not pending:
        print('No products ready for activation.')
        print(f'Fill in notion_template_url column in {PENDING_FILE} first.')
        return

    print(f'Found {len(pending)} product(s) to activate.\n')
    py = sys.executable

    for item in pending:
        slug = item['slug']
        url = item['template_url']
        print(f'{"=" * 60}')
        print(f'Activating: {slug}')
        print(f'Template URL: {url}')
        print(f'{"=" * 60}')

        r1 = subprocess.run([py, 'scripts/set_template_url.py', slug, url])
        if r1.returncode != 0:
            print(f'set_template_url.py failed for {slug} — skipping promote')
            continue

        r2 = subprocess.run([py, 'scripts/promote.py', slug])
        if r2.returncode != 0:
            print(f'promote.py failed for {slug} (non-fatal)')

        gumroad_result_path = f'products/ready/{slug}/gumroad_result.json'
        gumroad_url = ''
        if os.path.exists(gumroad_result_path):
            import json
            with open(gumroad_result_path, encoding='utf-8') as f:
                gr = json.load(f)
            gumroad_url = gr.get('gumroad_short_url', '')

        text = mark_done(text, slug, gumroad_url)
        with open(PENDING_FILE, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f'\nDone: {slug}')

    print(f'\n{"=" * 60}')
    print(f'Batch activation complete.')


if __name__ == '__main__':
    main()
