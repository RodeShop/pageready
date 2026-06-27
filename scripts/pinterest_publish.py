#!/usr/bin/env python3
"""
pinterest_publish.py — Posts a pin to Pinterest via API v5
Usage: python scripts/pinterest_publish.py <slug>
"""

import base64
import json
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

PINTEREST_TOKEN = os.getenv('PINTEREST_ACCESS_TOKEN')
PINTEREST_BOARD_ID = os.getenv('PINTEREST_BOARD_ID')
BASE_URL = 'https://api.pinterest.com/v5'


def get_headers():
    return {
        'Authorization': f'Bearer {PINTEREST_TOKEN}',
        'Content-Type': 'application/json',
    }


def get_or_create_board():
    """Return PINTEREST_BOARD_ID from env, or first board found."""
    if PINTEREST_BOARD_ID:
        return PINTEREST_BOARD_ID

    r = requests.get(f'{BASE_URL}/boards', headers=get_headers(),
                     params={'page_size': 1})
    r.raise_for_status()
    boards = r.json().get('items', [])
    if not boards:
        print('Error: no Pinterest boards found. Create one first.')
        sys.exit(1)
    board_id = boards[0]['id']
    print(f'  Using board: {boards[0]["name"]} ({board_id})')
    return board_id


def post_pin(board_id, spec, image_path, product_url):
    with open(image_path, 'rb') as f:
        image_b64 = base64.b64encode(f.read()).decode('utf-8')

    title = spec.get('title', 'Notion Template')
    audience = spec.get('target_audience', 'Professionals')
    tagline = spec.get('tagline', '')
    price = spec.get('price', 29)

    description = (
        f'{title} — Notion template for {audience}. '
        f'{tagline} '
        f'One-time payment ${price}. Works with Notion Free. '
        f'Download at RodeShop → link in bio'
    ).strip()

    payload = {
        'board_id': board_id,
        'title': f'{title} | Notion Template for {audience}',
        'description': description,
        'link': product_url,
        'media_source': {
            'source_type': 'image_base64',
            'content_type': 'image/png',
            'data': image_b64,
        },
    }

    r = requests.post(f'{BASE_URL}/pins', headers=get_headers(), json=payload)
    if r.status_code not in (200, 201):
        print(f'  Pinterest API error {r.status_code}: {r.text[:300]}')
        r.raise_for_status()

    pin = r.json()
    print(f'  Pin created: {pin.get("id")}')
    return pin


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/pinterest_publish.py <slug>')
        sys.exit(1)

    if not PINTEREST_TOKEN:
        print('Error: PINTEREST_ACCESS_TOKEN not set in .env')
        print('Pinterest app still under review — skip for now.')
        sys.exit(1)

    slug = sys.argv[1]
    ready_dir = f'products/ready/{slug}'

    spec_path  = f'{ready_dir}/spec.json'
    image_path = f'{ready_dir}/pinterest-pin.png'
    gumroad_result_path = f'{ready_dir}/gumroad_result.json'

    for path in [spec_path, image_path, gumroad_result_path]:
        if not os.path.exists(path):
            print(f'Error: {path} not found')
            sys.exit(1)

    with open(spec_path, encoding='utf-8') as f:
        spec = json.load(f)
    with open(gumroad_result_path, encoding='utf-8') as f:
        gumroad = json.load(f)

    product_url = gumroad.get('gumroad_short_url', '')

    print(f'\nPosting Pinterest pin: {spec["title"]}')
    board_id = get_or_create_board()
    pin = post_pin(board_id, spec, image_path, product_url)

    # Save pin result
    result_path = f'{ready_dir}/pinterest_result.json'
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump({'pin_id': pin.get('id'), 'board_id': board_id}, f, indent=2)

    print(f'  Done. Pin ID: {pin.get("id")}')


if __name__ == '__main__':
    main()
