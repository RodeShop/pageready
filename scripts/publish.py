#!/usr/bin/env python3
"""
publish.py — Runs notion_create + gumroad_create for a product slug.
Usage: python scripts/publish.py <slug>
"""

import subprocess
import sys
import os


def run(cmd):
    print(f'\n$ {" ".join(cmd)}')
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f'Error: command failed with code {result.returncode}')
        sys.exit(result.returncode)


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/publish.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]

    print(f'\n{"=" * 50}')
    print(f'PUBLISH: {slug}')
    print(f'{"=" * 50}')

    run([sys.executable, 'scripts/notion_create.py', slug])
    run([sys.executable, 'scripts/gumroad_create.py', slug])

    print(f'\n{"=" * 50}')
    print('DONE. Manual step required:')
    print(f'  1. Open Notion → find "{slug}" page')
    print(f'  2. Click Share → enable "Allow template duplication"')
    print(f'  3. Copy the template link')
    print(f'  4. Run: python scripts/set_template_url.py {slug} <notion_template_url>')
    print(f'{"=" * 50}')


if __name__ == '__main__':
    main()
