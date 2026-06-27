#!/usr/bin/env python3
"""
gumroad_create.py — Creates a Gumroad product draft from spec.json + listing.md
Usage: python scripts/gumroad_create.py <slug>
"""

import json
import os
import re
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

GUMROAD_TOKEN = os.getenv('GUMROAD_ACCESS_TOKEN')
BASE_URL = 'https://api.gumroad.com/v2'


def api_post(path, data=None, files=None):
    data = dict(data or {})
    data['access_token'] = GUMROAD_TOKEN
    r = requests.post(f'{BASE_URL}{path}', data=data, files=files)
    result = r.json()
    if not result.get('success'):
        print(f'  API error: {result.get("message", r.text[:300])}')
        r.raise_for_status()
    return result


def api_put(path, data=None):
    data = dict(data or {})
    data['access_token'] = GUMROAD_TOKEN
    r = requests.put(f'{BASE_URL}{path}', data=data)
    result = r.json()
    if not result.get('success'):
        print(f'  API error: {result.get("message", r.text[:300])}')
        r.raise_for_status()
    return result


def md_to_html(md):
    """Convert simple Markdown to Gumroad-compatible HTML."""
    lines = md.strip().split('\n')
    out = []
    in_ul = False

    for line in lines:
        line = line.rstrip()

        # Close list before non-list content
        def close_list():
            nonlocal in_ul
            if in_ul:
                out.append('</ul>')
                in_ul = False

        if line.startswith('### '):
            close_list()
            out.append(f'<h3>{_inline(line[4:])}</h3>')
        elif line.startswith('## '):
            close_list()
            out.append(f'<h2>{_inline(line[3:])}</h2>')
        elif line.startswith('# '):
            close_list()
            out.append(f'<h1>{_inline(line[2:])}</h1>')
        elif line.startswith('- ') or line.startswith('* '):
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{_inline(line[2:])}</li>')
        elif line == '':
            close_list()
            out.append('')
        else:
            close_list()
            out.append(f'<p>{_inline(line)}</p>')

    if in_ul:
        out.append('</ul>')

    return '\n'.join(out)


def _inline(text):
    """Apply inline markdown: bold, italic."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def create_product(spec, listing_md):
    price_cents = int(float(spec.get('price', 29)) * 100)
    description = md_to_html(listing_md)
    permalink = spec.get('slug', re.sub(r'[^a-z0-9-]', '-', spec['title'].lower()))

    data = {
        'name': spec['title'],
        'description': description,
        'price': price_cents,
        'currency_code': 'usd',
        'published': 'false',
        'custom_permalink': permalink,
    }

    result = api_post('/products', data)
    product = result['product']
    print(f'  Created: {product["id"]}')
    print(f'  Short URL: {product.get("short_url", "—")}')
    return product


def upload_user_guide(product_id, guide_path):
    with open(guide_path, 'rb') as f:
        files = {'file': ('user-guide.md', f, 'text/markdown')}
        data = {'name': 'User Guide & Template Instructions'}
        api_post(f'/products/{product_id}/product_files', data=data, files=files)
    print(f'  User guide uploaded')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/gumroad_create.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]
    draft_dir = f'products/draft/{slug}'
    spec_path    = f'{draft_dir}/spec.json'
    listing_path = f'{draft_dir}/listing.md'
    guide_path   = f'{draft_dir}/user-guide.md'

    missing = [p for p in [spec_path, listing_path, guide_path] if not os.path.exists(p)]
    if missing:
        for p in missing:
            print(f'Error: {p} not found')
        sys.exit(1)

    with open(spec_path, encoding='utf-8') as f:
        spec = json.load(f)
    with open(listing_path, encoding='utf-8') as f:
        listing_md = f.read()

    print(f'\nCreating Gumroad product: {spec["title"]}')
    print('=' * 50)

    print('\n[1/2] Creating product draft...')
    product = create_product(spec, listing_md)

    print('\n[2/2] Uploading user guide...')
    upload_user_guide(product['id'], guide_path)

    result = {
        'gumroad_product_id': product['id'],
        'gumroad_short_url':  product.get('short_url', ''),
        'gumroad_edit_url':   f'https://app.gumroad.com/products/{product["id"]}/edit',
        'price':   spec.get('price', 29),
        'slug':    slug,
        'published': False,
    }

    result_path = f'{draft_dir}/gumroad_result.json'
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print('\n' + '=' * 50)
    print(f'DONE (draft, not published)')
    print(f'Edit: {result["gumroad_edit_url"]}')
    print(f'Result saved: {result_path}')
    print(f'\nNext steps:')
    print(f'  1. Share Notion page → get template URL')
    print(f'  2. python scripts/set_template_url.py {slug} <notion_url>')
    print(f'  3. python scripts/publish.py {slug}')


if __name__ == '__main__':
    main()
