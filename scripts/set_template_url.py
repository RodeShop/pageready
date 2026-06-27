#!/usr/bin/env python3
"""
set_template_url.py — Adds the Notion template URL to Gumroad product description
                       and publishes the product.
Usage: python scripts/set_template_url.py <slug> <notion_template_url>
"""

import json
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

GUMROAD_TOKEN = os.getenv('GUMROAD_ACCESS_TOKEN')
BASE_URL = 'https://api.gumroad.com/v2'


def api_put(path, data):
    data['access_token'] = GUMROAD_TOKEN
    r = requests.put(f'{BASE_URL}{path}', data=data)
    result = r.json()
    if not result.get('success'):
        print(f'  API error: {result.get("message", r.text[:300])}')
        r.raise_for_status()
    return result


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

    # Read existing listing and append Notion URL section
    with open(listing_path, encoding='utf-8') as f:
        listing_md = f.read()

    notion_block = f"""

---

## Get the Template

**[Click here to duplicate the Notion template →]({notion_url})**

After clicking, select **"Duplicate"** in the top-right corner of the Notion page to add it to your workspace.
"""

    full_description = listing_md + notion_block

    # Convert to HTML (reuse logic from gumroad_create)
    sys.path.insert(0, os.path.dirname(__file__))
    from gumroad_create import md_to_html
    description_html = md_to_html(full_description)

    print(f'\nUpdating Gumroad product {product_id}...')

    # Update description with Notion URL and publish
    result = api_put(f'/products/{product_id}', {
        'description': description_html,
        'published': 'true',
    })

    print(f'  Published: {result["product"].get("short_url")}')

    # Update local result file
    gumroad_result['notion_template_url'] = notion_url
    gumroad_result['published'] = True
    gumroad_result['gumroad_short_url'] = result['product'].get('short_url', '')

    with open(gumroad_result_path, 'w', encoding='utf-8') as f:
        json.dump(gumroad_result, f, indent=2, ensure_ascii=False)

    # Move draft → ready
    ready_dir = f'products/ready/{slug}'
    os.makedirs(ready_dir, exist_ok=True)

    import shutil
    for fname in os.listdir(draft_dir):
        shutil.copy2(f'{draft_dir}/{fname}', f'{ready_dir}/{fname}')

    print(f'\n{"=" * 50}')
    print(f'PUBLISHED: {gumroad_result["gumroad_short_url"]}')
    print(f'Notion:    {notion_url}')
    print(f'Files:     products/ready/{slug}/')
    print(f'\nNext: python scripts/promote.py {slug}')
    print(f'{"=" * 50}')


if __name__ == '__main__':
    main()
