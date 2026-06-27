#!/usr/bin/env python3
"""
notion_create.py — Creates a Notion template from spec.json
Usage: python scripts/notion_create.py <slug>
"""

import json
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_ROOT_PAGE_ID = os.getenv('NOTION_ROOT_PAGE_ID')
BASE_URL = 'https://api.notion.com/v1'

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

COVER_URLS = {
    'green':  'https://www.notion.so/images/page-cover/gradients_2.png',
    'yellow': 'https://www.notion.so/images/page-cover/gradients_8.png',
    'purple': 'https://www.notion.so/images/page-cover/gradients_6.png',
    'blue':   'https://www.notion.so/images/page-cover/gradients_3.png',
    'orange': 'https://www.notion.so/images/page-cover/gradients_11.png',
    'pink':   'https://www.notion.so/images/page-cover/gradients_10.png',
}


def api(method, path, data=None):
    url = f'{BASE_URL}{path}'
    r = getattr(requests, method)(url, headers=HEADERS, json=data)
    if r.status_code not in (200, 201):
        print(f'  API error {r.status_code}: {r.text[:300]}')
        r.raise_for_status()
    time.sleep(0.35)
    return r.json()


# ── Property schema (for database creation) ────────────────────────────────

def build_property_schema(prop):
    t = prop['type']
    if t == 'title':
        return {'title': {}}
    if t == 'select':
        opts = [{'name': o['name'], 'color': o.get('color', 'default')}
                for o in prop.get('options', [])]
        return {'select': {'options': opts}}
    if t == 'multi_select':
        opts = [{'name': o['name'], 'color': o.get('color', 'default')}
                for o in prop.get('options', [])]
        return {'multi_select': {'options': opts}}
    if t == 'number':
        return {'number': {'format': prop.get('format', 'number')}}
    if t == 'date':
        return {'date': {}}
    if t == 'email':
        return {'email': {}}
    if t == 'url':
        return {'url': {}}
    if t == 'checkbox':
        return {'checkbox': {}}
    if t in ('text', 'rich_text'):
        return {'rich_text': {}}
    if t == 'phone_number':
        return {'phone_number': {}}
    if t == 'status':
        return {'status': {}}
    return {'rich_text': {}}


# ── Property values (for sample rows) ──────────────────────────────────────

def build_property_value(prop_spec, value):
    if value is None:
        return None
    t = prop_spec['type']
    if t == 'title':
        return {'title': [{'text': {'content': str(value)}}]}
    if t == 'select':
        return {'select': {'name': str(value)}}
    if t == 'multi_select':
        vals = value if isinstance(value, list) else [value]
        return {'multi_select': [{'name': str(v)} for v in vals]}
    if t == 'number':
        return {'number': float(value)}
    if t == 'date':
        return {'date': {'start': str(value)}}
    if t == 'email':
        return {'email': str(value)}
    if t == 'url':
        return {'url': str(value)}
    if t == 'checkbox':
        return {'checkbox': bool(value)}
    if t in ('text', 'rich_text'):
        return {'rich_text': [{'text': {'content': str(value)}}]}
    return None


# ── Block conversion ────────────────────────────────────────────────────────

def block_to_notion(b):
    t = b['type']

    if t == 'divider':
        return {'object': 'block', 'type': 'divider', 'divider': {}}

    text = b.get('text', '')
    rt = [{'type': 'text', 'text': {'content': text}}]

    if t in ('heading_1', 'heading_2', 'heading_3'):
        return {'object': 'block', 'type': t,
                t: {'rich_text': rt, 'color': b.get('color', 'default')}}

    if t == 'paragraph':
        return {'object': 'block', 'type': 'paragraph',
                'paragraph': {'rich_text': rt}}

    if t == 'bullet':
        return {'object': 'block', 'type': 'bulleted_list_item',
                'bulleted_list_item': {'rich_text': rt}}

    if t == 'numbered':
        return {'object': 'block', 'type': 'numbered_list_item',
                'numbered_list_item': {'rich_text': rt}}

    if t == 'quote':
        return {'object': 'block', 'type': 'quote',
                'quote': {'rich_text': rt}}

    if t == 'callout':
        return {
            'object': 'block', 'type': 'callout',
            'callout': {
                'rich_text': rt,
                'icon': {'type': 'emoji', 'emoji': b.get('emoji', '💡')},
                'color': b.get('color', 'default')
            }
        }

    if t == 'toggle':
        children = [block_to_notion(c) for c in b.get('children', [])]
        children = [c for c in children if c]
        return {'object': 'block', 'type': 'toggle',
                'toggle': {'rich_text': rt, 'children': children}}

    return None


# ── Notion API actions ──────────────────────────────────────────────────────

def create_product_page(spec):
    cover_url = COVER_URLS.get(spec.get('cover_color', 'green'),
                               COVER_URLS['green'])
    data = {
        'parent': {'page_id': NOTION_ROOT_PAGE_ID},
        'icon': {'type': 'emoji', 'emoji': spec.get('emoji', '📋')},
        'cover': {'type': 'external', 'external': {'url': cover_url}},
        'properties': {
            'title': {'title': [{'text': {'content': spec['title']}}]}
        }
    }
    result = api('post', '/pages', data)
    page_id = result['id']
    print(f'  Root page created: {page_id}')
    return page_id


def create_database(parent_id, db_spec):
    props = {}
    for prop in db_spec.get('properties', []):
        if prop['type'] == 'relation':
            continue  # relations added in second pass
        props[prop['name']] = build_property_schema(prop)

    data = {
        'parent': {'type': 'page_id', 'page_id': parent_id},
        'icon': {'type': 'emoji', 'emoji': db_spec.get('emoji', '📋')},
        'title': [{'type': 'text', 'text': {'content': db_spec['name']}}],
        'is_inline': False,
        'properties': props
    }
    result = api('post', '/databases', data)
    db_id = result['id']
    print(f'  Database "{db_spec["name"]}": {db_id}')
    return db_id


def add_relations(db_spec, db_id, db_map):
    for prop in db_spec.get('properties', []):
        if prop['type'] != 'relation':
            continue
        related_name = prop.get('related_db')
        related_id = db_map.get(related_name)
        if not related_id:
            print(f'  Warning: related db "{related_name}" not found, skipping')
            continue
        data = {
            'properties': {
                prop['name']: {
                    'relation': {
                        'database_id': related_id,
                        'type': 'single_property',
                        'single_property': {}
                    }
                }
            }
        }
        api('patch', f'/databases/{db_id}', data)
        print(f'  Relation "{prop["name"]}" → "{related_name}"')


def add_sample_rows(db_id, rows, prop_specs):
    prop_map = {p['name']: p for p in prop_specs}
    for row in rows:
        props = {}
        for key, value in row.items():
            spec = prop_map.get(key)
            if not spec or spec['type'] == 'relation':
                continue
            val = build_property_value(spec, value)
            if val is not None:
                props[key] = val
        api('post', '/pages', {'parent': {'database_id': db_id}, 'properties': props})
    print(f'  Added {len(rows)} sample rows')


def create_welcome_page(parent_id, spec):
    blocks_raw = spec.get('welcome_blocks', [])
    blocks = [block_to_notion(b) for b in blocks_raw]
    blocks = [b for b in blocks if b is not None]

    data = {
        'parent': {'page_id': parent_id},
        'icon': {'type': 'emoji', 'emoji': '👋'},
        'properties': {
            'title': {'title': [{'text': {'content': '👋 Welcome — Start Here'}}]}
        },
        'children': blocks[:100]
    }
    result = api('post', '/pages', data)
    page_id = result['id']

    # Append if more than 100 blocks
    for i in range(100, len(blocks), 100):
        api('patch', f'/blocks/{page_id}/children', {'children': blocks[i:i+100]})

    print(f'  Welcome page: {page_id}')
    return page_id


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/notion_create.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]
    spec_path = f'products/draft/{slug}/spec.json'

    if not os.path.exists(spec_path):
        print(f'Error: {spec_path} not found')
        sys.exit(1)

    with open(spec_path, encoding='utf-8') as f:
        spec = json.load(f)

    print(f'\nCreating: {spec["title"]}')
    print('=' * 50)

    print('\n[1/4] Root page...')
    page_id = create_product_page(spec)

    print('\n[2/4] Databases...')
    db_map = {}
    for db_spec in spec.get('databases', []):
        db_id = create_database(page_id, db_spec)
        db_map[db_spec['name']] = db_id

    print('\n[3/4] Relations + sample data...')
    for db_spec in spec.get('databases', []):
        has_relations = any(p['type'] == 'relation'
                           for p in db_spec.get('properties', []))
        if has_relations:
            add_relations(db_spec, db_map[db_spec['name']], db_map)
        rows = db_spec.get('sample_rows', [])
        if rows:
            add_sample_rows(db_map[db_spec['name']], rows, db_spec['properties'])

    print('\n[4/4] Welcome page...')
    create_welcome_page(page_id, spec)

    result = {
        'notion_page_id': page_id,
        'notion_url': f'https://notion.so/{page_id.replace("-", "")}',
        'databases': db_map,
        'slug': slug
    }
    result_path = f'products/draft/{slug}/notion_result.json'
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print('\n' + '=' * 50)
    print(f'DONE: https://notion.so/{page_id.replace("-", "")}')
    print(f'Result: {result_path}')
    print(f'\nNext: Share the Notion page → "Share" → enable "Allow template duplication"')
    print(f'Then: python scripts/set_template_url.py {slug} <notion_template_url>')


if __name__ == '__main__':
    main()
