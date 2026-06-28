#!/usr/bin/env python3
"""
pillow_pin.py — Direction D: System Cards (solid bg, white cards, no emoji)
Outputs: gumroad-thumb.png (1600x900), pinterest-pin.png (1000x1500), notion-cover.png (3000x1200)
Usage: python scripts/pillow_pin.py <slug>
"""

import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

BG     = (238, 241, 245)   # #eef1f5
INK    = (18, 18, 18)      # #121212
MUTED  = (100, 116, 139)   # #64748b
CARD   = (255, 255, 255)
SHADOW = (210, 215, 222)

SCHEMES = {
    'green':  (5, 150, 105),
    'yellow': (202, 138, 4),
    'purple': (124, 58, 237),
    'blue':   (37, 99, 235),
    'orange': (234, 88, 12),
    'pink':   (219, 39, 119),
}
DEFAULT_ACCENT = SCHEMES['blue']

BOLD_FONTS = [
    'C:/Windows/Fonts/arialbd.ttf',
    'C:/Windows/Fonts/segoeuib.ttf',
    'C:/Windows/Fonts/verdanab.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]
REG_FONTS = [
    'C:/Windows/Fonts/arial.ttf',
    'C:/Windows/Fonts/segoeui.ttf',
    'C:/Windows/Fonts/verdana.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap_lines(text, font, max_width):
    words = text.split()
    lines, current = [], ''
    for word in words:
        test = (current + ' ' + word).strip()
        try:
            w = font.getbbox(test)[2] - font.getbbox(test)[0]
        except Exception:
            w = len(test) * 8
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]


def lh(font):
    try:
        bb = font.getbbox('Ag')
        return int((bb[3] - bb[1]) * 1.35)
    except Exception:
        return 20


def draw_centered(draw, text, y, cx, font, color, max_width):
    """Centered wrapped text. Returns y after last line."""
    for line in wrap_lines(text, font, max_width):
        try:
            w = font.getbbox(line)[2] - font.getbbox(line)[0]
        except Exception:
            w = len(line) * 8
        draw.text((cx - w // 2, y), line, font=font, fill=color)
        y += lh(font)
    return y


def draw_card(draw, x, y, w, h, text, font):
    """White card with shadow, DB name centered."""
    draw.rounded_rectangle([(x + 3, y + 4), (x + w + 3, y + h + 4)], radius=12, fill=SHADOW)
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=CARD)
    lines = wrap_lines(text, font, w - 40)
    total_h = len(lines) * lh(font)
    ty = y + (h - total_h) // 2
    for line in lines:
        try:
            lw_ = font.getbbox(line)[2] - font.getbbox(line)[0]
        except Exception:
            lw_ = len(line) * 8
        draw.text((x + (w - lw_) // 2, ty), line, font=font, fill=INK)
        ty += lh(font)


def make_thumb(spec, out_path):
    """1600 × 900 Gumroad thumbnail — Direction D."""
    W, H = 1600, 900
    accent = SCHEMES.get(spec.get('cover_color', ''), DEFAULT_ACCENT)
    dbs = [db['name'] for db in spec.get('databases', [])[:3]]
    while len(dbs) < 3:
        dbs.append('Module')

    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    cx = W // 2

    font_title = load_font(BOLD_FONTS, 60)
    font_tag   = load_font(REG_FONTS,  30)
    font_card  = load_font(BOLD_FONTS, 28)
    font_brand = load_font(BOLD_FONTS, 30)

    y = 58
    y = draw_centered(draw, spec.get('title', 'Notion Template'), y, cx, font_title, INK, W - 200)

    y += 14
    draw.rectangle([(cx - 56, y), (cx + 56, y + 4)], fill=accent)
    y += 18

    tagline = spec.get('tagline', '')
    if tagline:
        y = draw_centered(draw, tagline, y, cx, font_tag, MUTED, W - 320)

    card_w, card_h = 440, 200
    gap = 30
    total = 3 * card_w + 2 * gap
    card_x0 = (W - total) // 2
    card_y = max(y + 50, 345)

    for i, db in enumerate(dbs):
        draw_card(draw, card_x0 + i * (card_w + gap), card_y, card_w, card_h, db, font_card)

    brand_text = f'RodeShop  ·  ${spec.get("price", 19)}'
    try:
        bw = font_brand.getbbox(brand_text)[2] - font_brand.getbbox(brand_text)[0]
    except Exception:
        bw = 200
    draw.text((cx - bw // 2, H - 62), brand_text, font=font_brand, fill=accent)

    img.save(out_path, 'PNG', optimize=True)
    print(f'  Gumroad thumbnail saved: {out_path}')


def make_pin(spec, out_path):
    """1000 × 1500 Pinterest pin — Direction D."""
    W, H = 1000, 1500
    accent = SCHEMES.get(spec.get('cover_color', ''), DEFAULT_ACCENT)
    dbs = [db['name'] for db in spec.get('databases', [])[:3]]
    while len(dbs) < 3:
        dbs.append('Module')

    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    cx = W // 2

    font_title = load_font(BOLD_FONTS, 64)
    font_tag   = load_font(REG_FONTS,  34)
    font_card  = load_font(BOLD_FONTS, 30)
    font_brand = load_font(BOLD_FONTS, 34)

    y = 80
    y = draw_centered(draw, spec.get('title', 'Notion Template'), y, cx, font_title, INK, W - 120)

    y += 20
    draw.rectangle([(cx - 56, y), (cx + 56, y + 4)], fill=accent)
    y += 24

    tagline = spec.get('tagline', '')
    if tagline:
        y = draw_centered(draw, tagline, y, cx, font_tag, MUTED, W - 160)

    card_w, card_h = 820, 190
    gap = 22
    card_x = (W - card_w) // 2
    card_y = max(y + 60, 500)

    for i, db in enumerate(dbs):
        draw_card(draw, card_x, card_y + i * (card_h + gap), card_w, card_h, db, font_card)

    brand_text = f'RodeShop  ·  ${spec.get("price", 19)}'
    try:
        bw = font_brand.getbbox(brand_text)[2] - font_brand.getbbox(brand_text)[0]
    except Exception:
        bw = 220
    draw.text((cx - bw // 2, H - 96), brand_text, font=font_brand, fill=accent)

    img.save(out_path, 'PNG', optimize=True)
    print(f'  Pinterest pin saved: {out_path}')


def make_notion_cover(spec, out_path):
    """3000 × 1200 Notion page cover — strip-only, NO cards.

    Notion's cover strip is ~250-320px tall on screen (object-fit:cover scales
    the PNG to fill viewport width). A full Direction D layout with 250px cards
    fills the entire visible strip, looks giant, and duplicates the title + DB
    list that Notion renders below the cover anyway.

    Instead: text-only content confined to the vertical safe zone y=480..720
    and horizontal safe zone x=900..2100 (center 1200px). Everything outside
    is plain #eef1f5 — clean crop on any viewport.

    Gumroad thumb and Pinterest pin keep the full Direction D with cards.
    """
    W, H = 3000, 1200
    accent = SCHEMES.get(spec.get('cover_color', ''), DEFAULT_ACCENT)

    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Safe zone dimensions
    CX     = W // 2        # 1500 — horizontal center
    SY_TOP = 480
    SY_BOT = 720
    SY_H   = SY_BOT - SY_TOP   # 240px
    SW     = 1200               # horizontal zone width (x=900..2100)

    font_title = load_font(BOLD_FONTS, 48)
    font_tag   = load_font(REG_FONTS,  22)
    font_brand = load_font(BOLD_FONTS, 18)

    title   = spec.get('title', 'Notion Template')
    tagline = spec.get('tagline', '')

    title_lines = wrap_lines(title, font_title, SW - 40)
    tag_lines   = wrap_lines(tagline, font_tag, SW - 40) if tagline else []

    title_h  = len(title_lines) * lh(font_title)
    tag_h    = (8 + len(tag_lines) * lh(font_tag)) if tag_lines else 0
    accent_h = 14 + 3 + 6 + lh(font_brand)   # gap + line + gap + brand
    total_h  = title_h + tag_h + accent_h

    ty = SY_TOP + (SY_H - total_h) // 2

    # Title — centered in safe zone
    for line in title_lines:
        try:
            w = font_title.getbbox(line)[2] - font_title.getbbox(line)[0]
        except Exception:
            w = len(line) * 14
        draw.text((CX - w // 2, ty), line, font=font_title, fill=INK)
        ty += lh(font_title)

    # Tagline
    if tag_lines:
        ty += 8
        for line in tag_lines:
            try:
                w = font_tag.getbbox(line)[2] - font_tag.getbbox(line)[0]
            except Exception:
                w = len(line) * 8
            draw.text((CX - w // 2, ty), line, font=font_tag, fill=MUTED)
            ty += lh(font_tag)

    # Accent rule
    ty += 14
    draw.rectangle([(CX - 40, ty), (CX + 40, ty + 3)], fill=accent)
    ty += 9

    # Brand
    brand = 'RodeShop'
    try:
        bw = font_brand.getbbox(brand)[2] - font_brand.getbbox(brand)[0]
    except Exception:
        bw = len(brand) * 8
    draw.text((CX - bw // 2, ty), brand, font=font_brand, fill=accent)

    img.save(out_path, 'PNG', compress_level=1)
    print(f'  Notion cover saved: {out_path}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/pillow_pin.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]

    for base in [f'products/draft/{slug}', f'products/ready/{slug}']:
        spec_path = f'{base}/spec.json'
        if os.path.exists(spec_path):
            out_dir = base
            break
    else:
        print(f'Error: spec.json not found for slug "{slug}"')
        sys.exit(1)

    with open(spec_path, encoding='utf-8') as f:
        spec = json.load(f)

    print(f'\nGenerating images for: {spec["title"]}')
    make_thumb(spec,         f'{out_dir}/gumroad-thumb.png')
    make_pin(spec,           f'{out_dir}/pinterest-pin.png')
    make_notion_cover(spec,  f'{out_dir}/notion-cover.png')
    print('Done.')


if __name__ == '__main__':
    main()
