#!/usr/bin/env python3
"""
pillow_pin.py — Generates Pinterest pin (1000x1500) and Gumroad thumbnail (1600x900)
Usage: python scripts/pillow_pin.py <slug>
"""

import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Color schemes keyed by cover_color in spec.json
SCHEMES = {
    'green':  {'bg1': (240,253,244), 'bg2': (220,252,231), 'accent': (5,150,105),  'dark': (6,95,70)},
    'yellow': {'bg1': (254,249,195), 'bg2': (254,240,138), 'accent': (202,138,4),  'dark': (133,77,14)},
    'purple': {'bg1': (237,233,254), 'bg2': (221,214,254), 'accent': (124,58,237), 'dark': (91,33,182)},
    'blue':   {'bg1': (239,246,255), 'bg2': (219,234,254), 'accent': (37,99,235),  'dark': (29,78,216)},
    'orange': {'bg1': (255,247,237), 'bg2': (255,237,213), 'accent': (234,88,12),  'dark': (154,52,18)},
    'pink':   {'bg1': (253,242,248), 'bg2': (252,231,243), 'accent': (219,39,119), 'dark': (157,23,77)},
}
DEFAULT_SCHEME = SCHEMES['green']

# Font candidates (Windows → Linux → macOS)
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
EMOJI_FONTS = [
    'C:/Windows/Fonts/seguiemj.ttf',
    'C:/Windows/Fonts/segoe ui emoji.ttf',
    '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
]


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def gradient(width, height, c1, c2):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / height
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (width - 1, y)], fill=(r, g, b))
    return img


def centered_text(draw, text, y, width, font, color, max_width=None, line_height=None):
    """Draw centered text, wrapping if needed. Returns bottom y."""
    if max_width is None:
        max_width = width - 80

    words = text.split()
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    if line_height is None:
        bbox = font.getbbox('Ag')
        line_height = int((bbox[3] - bbox[1]) * 1.3)

    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        x = (width - w) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += line_height

    return y


def make_pin(spec, out_path):
    """1000 x 1500 Pinterest pin."""
    W, H = 1000, 1500
    scheme = SCHEMES.get(spec.get('cover_color', 'green'), DEFAULT_SCHEME)

    img = gradient(W, H, scheme['bg1'], scheme['bg2'])
    draw = ImageDraw.Draw(img)

    # Accent bar at top
    draw.rectangle([(0, 0), (W, 6)], fill=scheme['accent'])

    # "NOTION TEMPLATE" label
    font_label = load_font(BOLD_FONTS, 28)
    label = 'NOTION TEMPLATE'
    bbox = font_label.getbbox(label)
    lw = bbox[2] - bbox[0]
    draw.text(((W - lw) // 2, 60), label, font=font_label, fill=scheme['accent'])

    # Emoji (large, centered)
    emoji = spec.get('emoji', '📋')
    font_emoji = load_font(EMOJI_FONTS, 200)
    try:
        bbox = font_emoji.getbbox(emoji)
        ew = bbox[2] - bbox[0]
        draw.text(((W - ew) // 2, 120), emoji, font=font_emoji, fill=(0, 0, 0))
        emoji_bottom = 340
    except Exception:
        # fallback: draw placeholder circle
        cx, cy, r = W // 2, 230, 90
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=scheme['accent'])
        emoji_bottom = 340

    # Divider line
    draw.rectangle([(W // 2 - 40, emoji_bottom + 20), (W // 2 + 40, emoji_bottom + 24)],
                   fill=scheme['accent'])

    # Title
    font_title = load_font(BOLD_FONTS, 72)
    title = spec.get('title', 'Notion Template')
    y = centered_text(draw, title, emoji_bottom + 60, W, font_title,
                      color=(15, 23, 42), max_width=860)

    # Audience
    font_sub = load_font(REG_FONTS, 38)
    audience = f'for {spec.get("target_audience", "Professionals")}'
    y = centered_text(draw, audience, y + 16, W, font_sub,
                      color=(71, 85, 105), max_width=800)

    # Tagline
    tagline = spec.get('tagline', '')
    if tagline:
        font_tag = load_font(REG_FONTS, 34)
        y = centered_text(draw, tagline, y + 30, W, font_tag,
                          color=(100, 116, 139), max_width=780)

    # Bottom section
    bottom_y = H - 220
    draw.rectangle([(0, bottom_y), (W, H)], fill=scheme['accent'])

    font_brand = load_font(BOLD_FONTS, 48)
    font_price = load_font(BOLD_FONTS, 44)
    font_url   = load_font(REG_FONTS,  30)

    # Brand name
    brand = 'RodeShop'
    bbox = font_brand.getbbox(brand)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, bottom_y + 28), brand, font=font_brand, fill=(255, 255, 255))

    # Price
    price_text = f'From ${spec.get("price", 29)}'
    bbox = font_price.getbbox(price_text)
    pw = bbox[2] - bbox[0]
    draw.text(((W - pw) // 2, bottom_y + 90), price_text, font=font_price, fill=(255, 255, 255))

    # URL
    url_text = 'rodeshop.github.io/pageready'
    bbox = font_url.getbbox(url_text)
    uw = bbox[2] - bbox[0]
    draw.text(((W - uw) // 2, bottom_y + 154), url_text, font=font_url,
              fill=(255, 255, 255, 180))

    img.save(out_path, 'PNG', optimize=True)
    print(f'  Pinterest pin saved: {out_path}')


def make_thumb(spec, out_path):
    """1600 x 900 Gumroad thumbnail."""
    W, H = 1600, 900
    scheme = SCHEMES.get(spec.get('cover_color', 'green'), DEFAULT_SCHEME)

    img = gradient(W, H, scheme['bg1'], scheme['bg2'])
    draw = ImageDraw.Draw(img)

    # Left half — main content
    cx = W // 2

    # Accent bar left
    draw.rectangle([(0, 0), (8, H)], fill=scheme['accent'])

    # Emoji
    emoji = spec.get('emoji', '📋')
    font_emoji = load_font(EMOJI_FONTS, 160)
    try:
        bbox = font_emoji.getbbox(emoji)
        ew = bbox[2] - bbox[0]
        draw.text(((cx - ew) // 2, 80), emoji, font=font_emoji, fill=(0, 0, 0))
    except Exception:
        r = 70
        draw.ellipse([(80, 80), (80 + r*2, 80 + r*2)], fill=scheme['accent'])

    # Title
    font_title = load_font(BOLD_FONTS, 72)
    y = centered_text(draw, spec.get('title', 'Notion Template'), 280, cx,
                      font_title, color=(15, 23, 42), max_width=cx - 60)

    # Audience
    font_aud = load_font(REG_FONTS, 38)
    y = centered_text(draw, f'for {spec.get("target_audience", "")}', y + 14, cx,
                      font_aud, color=(71, 85, 105), max_width=cx - 60)

    # Price badge
    price_text = f'${spec.get("price", 29)}'
    font_price = load_font(BOLD_FONTS, 56)
    bbox = font_price.getbbox(price_text)
    pw, ph = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 20
    px = (cx - pw) // 2
    py = H - 140
    draw.rounded_rectangle([(px - pad, py - pad), (px + pw + pad, py + ph + pad)],
                            radius=12, fill=scheme['accent'])
    draw.text((px, py), price_text, font=font_price, fill=(255, 255, 255))

    # Right half — feature list
    font_feat_title = load_font(BOLD_FONTS, 32)
    font_feat       = load_font(REG_FONTS,  30)

    draw.text((cx + 60, 80), 'What\'s inside:', font=font_feat_title, fill=scheme['dark'])

    databases = spec.get('databases', [])
    features = [f'{db.get("emoji","📋")} {db["name"]}' for db in databases[:4]]
    if not features:
        features = ['📊 Linked databases', '📝 Sample data included',
                    '👋 Setup guide', '🎯 Ready to use']

    fy = 140
    for feat in features:
        draw.text((cx + 60, fy), feat, font=font_feat, fill=(30, 41, 59))
        fy += 52

    # Divider between halves
    draw.rectangle([(cx - 1, 60), (cx + 1, H - 60)], fill=scheme['accent'])

    # Brand bottom-right
    font_brand = load_font(BOLD_FONTS, 34)
    brand = 'RodeShop'
    bbox = font_brand.getbbox(brand)
    draw.text((W - bbox[2] - bbox[0] - 40, H - 60), brand,
              font=font_brand, fill=scheme['accent'])

    img.save(out_path, 'PNG', optimize=True)
    print(f'  Gumroad thumbnail saved: {out_path}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/pillow_pin.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]

    # Try ready/ first, fall back to draft/
    for base in [f'products/ready/{slug}', f'products/draft/{slug}']:
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
    make_pin(spec,   f'{out_dir}/pinterest-pin.png')
    make_thumb(spec, f'{out_dir}/gumroad-thumb.png')
    print('Done.')


if __name__ == '__main__':
    main()
