#!/usr/bin/env python3
"""
promote.py — Full promotion pipeline: images → Pinterest → blog
Usage: python scripts/promote.py <slug>

Pinterest rate limit: max 2-3 pins/day on new accounts.
Script enforces 30-60 min sleep between pins automatically.
"""

import os
import random
import subprocess
import sys
import time
from dotenv import load_dotenv

load_dotenv()

PINTEREST_TOKEN = os.getenv('PINTEREST_ACCESS_TOKEN')


def run(cmd, label):
    print(f'\n[{label}]')
    print(f'$ {" ".join(cmd)}')
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f'Warning: {label} failed (code {result.returncode}). Continuing...')
        return False
    return True


def pinterest_sleep():
    """Enforce 30-60 min rate limit between Pinterest pins."""
    delay = random.randint(1800, 3600)
    minutes = delay // 60
    print(f'\n  Pinterest rate limit: sleeping {minutes} min before posting pin...')
    print(f'  (This prevents spam ban on new accounts)')

    # Show countdown every 5 minutes
    elapsed = 0
    interval = 300
    while elapsed < delay:
        wait = min(interval, delay - elapsed)
        time.sleep(wait)
        elapsed += wait
        remaining = (delay - elapsed) // 60
        if remaining > 0:
            print(f'  {remaining} min remaining...')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/promote.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]
    py = sys.executable

    print(f'\n{"=" * 50}')
    print(f'PROMOTE: {slug}')
    print(f'{"=" * 50}')

    # 1. Generate images (always, no API needed)
    run([py, 'scripts/pillow_pin.py', slug], '1/3  Images (Pillow)')

    # 2. Pinterest pin (only if token available)
    if PINTEREST_TOKEN:
        pinterest_sleep()
        run([py, 'scripts/pinterest_publish.py', slug], '2/3  Pinterest pin')
    else:
        print('\n[2/3  Pinterest pin]')
        print('  PINTEREST_ACCESS_TOKEN not set — skipping.')
        print('  Add token to .env once Pinterest app is approved.')

    # 3. Blog post
    run([py, 'scripts/blog_publish.py', slug], '3/3  Blog post → GitHub Pages')

    print(f'\n{"=" * 50}')
    print(f'PROMOTE DONE: {slug}')
    print(f'{"=" * 50}')


if __name__ == '__main__':
    main()
