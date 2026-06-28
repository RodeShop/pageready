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


def api_get(path, params=None):
    params = dict(params or {})
    params['access_token'] = GUMROAD_TOKEN
    r = requests.get(f'{BASE_URL}{path}', params=params)
    try:
        return r.json()
    except Exception:
        return {}


def find_product_by_permalink(permalink):
    result = api_get('/products')
    if result.get('success'):
        for p in result.get('products', []):
            if p.get('custom_permalink') == permalink:
                return p
    return None


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


def extract_description(listing_md):
    """Extract only the Description section from listing.md (skip Title/Price/Tags/etc.)"""
    sections = re.split(r'^## ', listing_md, flags=re.MULTILINE)
    desc = ''
    template_block = ''
    for section in sections:
        name = section.split('\n', 1)[0].strip().lower()
        body = section.split('\n', 1)[1].strip() if '\n' in section else ''
        if name == 'description':
            desc = body
        elif name == 'get the template':
            template_block = '\n\n## Get the Template\n\n' + body
    return (desc + template_block).strip()


def create_product(spec, listing_md, slug):
    price_cents = int(float(spec.get('price', 29)) * 100)
    clean_md = extract_description(listing_md)
    description = md_to_html(clean_md if clean_md else listing_md)
    permalink = spec.get('slug', re.sub(r'[^a-z0-9-]', '-', spec['title'].lower()))

    # 1. Local check: reuse if gumroad_result.json already exists
    for base in [f'products/draft/{slug}', f'products/ready/{slug}']:
        result_path = f'{base}/gumroad_result.json'
        if os.path.exists(result_path):
            with open(result_path, encoding='utf-8') as f:
                saved = json.load(f)
            if saved.get('gumroad_product_id'):
                print(f'  Found local result — reusing: {saved["gumroad_product_id"]}')
                return {'id': saved['gumroad_product_id'],
                        'short_url': saved.get('gumroad_short_url', '')}

    # 2. API check by permalink (prevents duplicate if local file was lost)
    print(f'  Checking Gumroad for existing permalink: {permalink}')
    existing = find_product_by_permalink(permalink)
    if existing:
        print(f'  Found existing product: {existing["id"]} — skip create')
        return existing

    # 3. Create new product
    data = {
        'name': spec['title'],
        'description': description,
        'price': price_cents,
        'currency_code': 'usd',
        'published': 'false',
        'custom_permalink': permalink,
    }

    try:
        result = api_post('/products', data)
        product = result.get('product')
        if not product:
            raise RuntimeError(result.get('message', 'No product in response'))
    except Exception as e:
        if any(kw in str(e).lower() for kw in ('permalink', 'taken', 'already')):
            print('  Permalink conflict — falling back to list search...')
            existing = find_product_by_permalink(permalink)
            if existing:
                print(f'  Found existing product: {existing["id"]}')
                return existing
        raise
    print(f'  Created: {product["id"]}')
    print(f'  Short URL: {product.get("short_url", "-")}')
    return product


def upload_user_guide(product_id, guide_path):
    """File upload via API is not supported by Gumroad v2 — skip gracefully."""
    print(f'  NOTE: Upload user-guide.md manually in Gumroad dashboard.')
    print(f'  Edit URL: https://app.gumroad.com/products/{product_id}/edit')


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
    product = create_product(spec, listing_md, slug)

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
    print(f'  1. Share Notion page -> get template URL')
    print(f'  2. python scripts/set_template_url.py {slug} <notion_url>')
    print(f'  3. python scripts/publish.py {slug}')


if __name__ == '__main__':
    main()
