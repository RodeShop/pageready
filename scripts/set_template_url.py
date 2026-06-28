#!/usr/bin/env python3
"""
set_template_url.py — Adds Notion template URL to Gumroad description and publishes.
Usage: python scripts/set_template_url.py <slug> <notion_template_url>
"""

import json
import os
import shutil
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

GUMROAD_TOKEN = os.getenv('GUMROAD_ACCESS_TOKEN')
BASE_URL = 'https://api.gumroad.com/v2'


def api_put(path, data):
    data = dict(data)
    data['access_token'] = GUMROAD_TOKEN
    r = requests.put(f'{BASE_URL}{path}', data=data)
    result = r.json()
    if not result.get('success'):
        print(f'  API error: {result.get("message", r.text[:300])}')
        r.raise_for_status()
    return result


def load_spec_price(slug):
    for path in [f'products/ready/{slug}/spec.json', f'products/draft/{slug}/spec.json']:
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return int(float(json.load(f).get('price', 19)) * 100)
    return 1900


def main():
    if len(sys.argv) < 3:
        print('Usage: python scripts/set_template_url.py <slug> <notion_template_url>')
        sys.exit(1)

    slug = sys.argv[1]
    notion_url = sys.argv[2]

    draft_dir = f'products/draft/{slug}'
    gumroad_result_path = f'{draft_dir}/gumroad_result.json'
    listing_path = f'{draft_dir}/listing.md'

    if not os.path.exists(gumroad_result_path):
        print(f'Error: {gumroad_result_path} not found. Run publish.py first.')
        sys.exit(1)

    with open(gumroad_result_path, encoding='utf-8') as f:
        gumroad_result = json.load(f)

    product_id = gumroad_result['gumroad_product_id']

    with open(listing_path, encoding='utf-8') as f:
        listing_md = f.read()

    sys.path.insert(0, os.path.dirname(__file__))
    from gumroad_create import md_to_html, extract_description

    desc_only = extract_description(listing_md) or listing_md

    notion_block = f"""

## Get the Template

**[Click here to duplicate the Notion template ->]({notion_url})**

After clicking, select **Duplicate** in the top-right corner of the Notion page.
"""

    description_html = md_to_html(desc_only + notion_block)
    price_cents = load_spec_price(slug)

    print(f'\nUpdating Gumroad product {product_id}...')
    api_put(f'/products/{product_id}', {
        'description': description_html,
        'price': price_cents,
    })
    print('  Description + price updated.')

    print('  Enabling product (publish)...')
    enable_result = api_put(f'/products/{product_id}/enable', {})
    product = enable_result['product']
    published = product.get('published', False)
    print(f'  Published: {published} — {product.get("short_url")}')

    gumroad_result['notion_template_url'] = notion_url
    gumroad_result['published'] = published
    gumroad_result['price'] = price_cents // 100
    gumroad_result['gumroad_short_url'] = product.get('short_url', gumroad_result.get('gumroad_short_url', ''))

    with open(gumroad_result_path, 'w', encoding='utf-8') as f:
        json.dump(gumroad_result, f, indent=2, ensure_ascii=False)

    ready_dir = f'products/ready/{slug}'
    os.makedirs(ready_dir, exist_ok=True)
    for fname in os.listdir(draft_dir):
        shutil.copy2(f'{draft_dir}/{fname}', f'{ready_dir}/{fname}')

    print(f'\n{"=" * 50}')
    print(f'LIVE: {gumroad_result["gumroad_short_url"]}')
    print(f'Notion: {notion_url}')
    print(f'{"=" * 50}')


if __name__ == '__main__':
    main()
