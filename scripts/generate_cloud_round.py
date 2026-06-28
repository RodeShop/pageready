#!/usr/bin/env python3
"""
Cloud Round — 5 directions × 2 sizes = 10 PNGs
Rules: 8px grid, bbox tracking (no overlap), tagline always visible
"""

from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = "assets/gumroad-variants/notion-developer-career-os/cloud-round"
os.makedirs(OUT, exist_ok=True)

WF = "C:/Windows/Fonts/"

FONT_MAP = {
    "bold":    [WF+"segoeuib.ttf", WF+"arialbd.ttf"],
    "regular": [WF+"segoeui.ttf",  WF+"arial.ttf"],
    "semi":    [WF+"seguisb.ttf",  WF+"segoeui.ttf"],
    "light":   [WF+"segoeuil.ttf", WF+"segoeui.ttf"],
    "mono":    [WF+"consola.ttf",  WF+"cour.ttf"],
    "monob":   [WF+"consolab.ttf", WF+"courbd.ttf"],
}

def fnt(style, size):
    for path in FONT_MAP.get(style, FONT_MAP["regular"]):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def measure(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]

def ink_bottom(draw, text, font):
    """b[3]: actual distance from draw anchor to bottom of ink (not ink height)."""
    return draw.textbbox((0, 0), text, font=font)[3]

def ink_top(draw, text, font):
    """b[1]: distance from draw anchor to top of ink."""
    return draw.textbbox((0, 0), text, font=font)[1]

def hline(draw, x, y, w, color, t=3):
    draw.rectangle([x, y, x + w, y + t - 1], fill=color)

def vline(draw, x, y, h, color, t=2):
    draw.rectangle([x, y, x + t - 1, y + h], fill=color)

def dot_grid(draw, W, H, spacing=32, dot_color="#1a2d46"):
    for gx in range(0, W, spacing):
        for gy in range(0, H, spacing):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=dot_color)

def rounded_rect(draw, x, y, w, h, r, fill, outline=None, outline_w=2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill,
                            outline=outline, width=outline_w)

def save_png(img, name):
    path = os.path.join(OUT, name)
    img.save(path, "PNG")
    print(f"  saved {name}")

# ─── DIRECTION 01 — SWISS COMMAND ────────────────────────────────────────────

def d01_cover():
    W, H = 1920, 1080
    BG, INK, MUTED, ACCENT = "#f8f8f6", "#0a0a0a", "#525252", "#2563EB"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    lm = 120

    # Pre-measure to vertically center block
    f_title = fnt("bold", 112)
    f_tag = fnt("regular", 32)
    f_proof = fnt("regular", 26)
    proofs = [
        "6 linked databases",
        "Projects · Jobs · Skills · Learning · Networking · Achievements",
        "Relations · rollups · sample data included",
    ]
    th = measure(d, "Developer Career OS", f_title)[1]
    t1h = measure(d, "The system that shows your career growth", f_tag)[1]
    t2h = measure(d, "before the interviewer asks", f_tag)[1]
    proof_block_h = sum(measure(d, p, f_proof)[1] + 20 for p in proofs)
    total = 8 + th + 40 + t1h + 8 + t2h + 56 + proof_block_h
    y0 = max(80, (H - total) // 2 - 32)

    # Accent rule above title
    hline(d, lm, y0, 560, ACCENT, 4)
    ty = y0 + 40

    # Title
    d.text((lm, ty), "Developer Career OS", font=f_title, fill=INK)
    _, tith = measure(d, "Developer Career OS", f_title)

    # Tagline — guaranteed gap after title bbox
    tag_top = ty + tith + 40
    tag1 = "The system that shows your career growth"
    tag2 = "before the interviewer asks"
    d.text((lm, tag_top), tag1, font=f_tag, fill=MUTED)
    d.text((lm, tag_top + t1h + 8), tag2, font=f_tag, fill=MUTED)

    # Proof lines
    py = tag_top + t1h + 8 + t2h + 56
    for line in proofs:
        hline(d, lm, py + 12, 32, ACCENT, 3)
        d.text((lm + 52, py), line, font=f_proof, fill=MUTED)
        _, lh = measure(d, line, f_proof)
        py += lh + 20

    # Bottom editorial rule
    hline(d, lm, H - 88, W - lm * 2, MUTED, 1)

    # Brand bottom-right
    f_brand = fnt("regular", 20)
    brand = "RodeShop · $19"
    bw, _ = measure(d, brand, f_brand)
    d.text((W - 120 - bw, H - 64), brand, font=f_brand, fill=MUTED)

    save_png(img, "direction-01--cover-1920x1080.png")


def d01_thumb():
    W, H = 1200, 1200
    BG, INK, MUTED, ACCENT = "#f8f8f6", "#0a0a0a", "#525252", "#2563EB"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    lm = 80

    # Pre-measure for vertical centering
    f_title = fnt("bold", 80)
    f_tag = fnt("regular", 26)
    f_proof = fnt("regular", 22)
    l1h = measure(d, "Developer", f_title)[1]
    l2h = measure(d, "Career OS", f_title)[1]
    tags = ["The system that shows", "your career growth", "before the interviewer asks"]
    tag_block_h = sum(measure(d, t, f_tag)[1] + 8 for t in tags)
    proofs = ["6 databases", "Projects · Jobs · Skills", "Learning · Networking"]
    proof_h = sum(measure(d, p, f_proof)[1] + 14 for p in proofs)
    total = 8 + l1h + 8 + l2h + 40 + tag_block_h + 40 + proof_h
    y0 = max(64, (H - total) // 2 - 24)

    hline(d, lm, y0, 400, ACCENT, 4)
    ty = y0 + 40

    d.text((lm, ty), "Developer", font=f_title, fill=INK)
    d.text((lm, ty + l1h + 8), "Career OS", font=f_title, fill=INK)
    tag_top = ty + l1h + 8 + l2h + 40

    ty2 = tag_top
    for t in tags:
        d.text((lm, ty2), t, font=f_tag, fill=MUTED)
        _, th = measure(d, t, f_tag)
        ty2 += th + 8

    py = ty2 + 40
    for line in proofs:
        hline(d, lm, py + 10, 24, ACCENT, 3)
        d.text((lm + 40, py), line, font=f_proof, fill=MUTED)
        _, lh = measure(d, line, f_proof)
        py += lh + 14

    hline(d, lm, H - 80, W - lm * 2, MUTED, 1)
    f_brand = fnt("regular", 18)
    d.text((lm, H - 56), "RodeShop · $19", font=f_brand, fill=MUTED)

    save_png(img, "direction-01--thumb-1200x1200.png")


# ─── DIRECTION 02 — TERMINAL NATIVE ──────────────────────────────────────────

def d02_cover():
    W, H = 1920, 1080
    BG, BAR, BORDER = "#0d1117", "#161b22", "#30363d"
    TEXT, MUTED, GREEN, BLUE = "#c9d1d9", "#8b949e", "#3fb950", "#58a6ff"
    TITLE_C = "#e6edf3"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Terminal chrome bar
    d.rectangle([0, 0, W, 56], fill=BAR)
    f_chrome = fnt("mono", 16)
    d.text((32, 18), "( )( )( )   ~/developer-career-os", font=f_chrome, fill=MUTED)
    hline(d, 0, 56, W, BORDER, 1)

    # git log — left column, full height
    f_mono = fnt("mono", 22)
    lm = 72
    log_entries = [
        ("a3f2c1", "green", "[career]  Stripe interview · Senior Frontend"),
        ("b8e401", "blue",  "[skill]   +800h React · +600h TypeScript"),
        ("c91d3e", "blue",  "[shipped] DevTracker · 142 stars on GitHub"),
        ("d04a77", "green", "[cert]    AWS Solutions Architect passed"),
        ("e5b12f", "blue",  "[jobs]    6 active · Railway offer received"),
        ("f8c219", "green", "[network] Sarah Chen (Stripe) · mentor call"),
        ("91ab34", "blue",  "[learn]   Rust book ch.8 · Go tour done"),
    ]
    prompt_y = 88
    d.text((lm, prompt_y), "$ git log --oneline", font=f_mono, fill=BLUE)
    _, ph = measure(d, "$ git log --oneline", f_mono)
    log_y = prompt_y + ph + 16
    for hash_str, color_key, msg in log_entries:
        hash_col = GREEN if color_key == "green" else BLUE
        d.text((lm, log_y), hash_str, font=f_mono, fill=hash_col)
        hw, _ = measure(d, hash_str, f_mono)
        d.text((lm + hw + 20, log_y), msg, font=f_mono, fill=TEXT)
        _, lh = measure(d, msg, f_mono)
        log_y += lh + 12

    d.text((lm, log_y + 8), "| ", font=f_mono, fill=GREEN)

    # Separator vertical rule
    sep_x = W // 2 + 80
    vline(d, sep_x, 56, H - 56, BORDER, 1)

    # Right column: title + tagline
    rx = sep_x + 80
    title_y = (H - 250) // 2
    f_title = fnt("semi", 64)
    d.text((rx, title_y), "Developer Career OS", font=f_title, fill=TITLE_C)
    _, tith = measure(d, "Developer Career OS", f_title)

    tag_y = title_y + tith + 32
    f_tag = fnt("regular", 28)
    tag1 = "The system that shows your"
    tag2 = "career growth before the"
    tag3 = "interviewer asks"
    for line in [tag1, tag2, tag3]:
        d.text((rx, tag_y), line, font=f_tag, fill=MUTED)
        _, lh = measure(d, line, f_tag)
        tag_y += lh + 8

    f_brand = fnt("mono", 16)
    brand = "RodeShop · $19"
    bw, _ = measure(d, brand, f_brand)
    d.text((W - 72 - bw, H - 48), brand, font=f_brand, fill=MUTED)

    save_png(img, "direction-02--cover-1920x1080.png")


def d02_thumb():
    W, H = 1200, 1200
    BG, BAR, BORDER = "#0d1117", "#161b22", "#30363d"
    TEXT, MUTED, GREEN, BLUE = "#c9d1d9", "#8b949e", "#3fb950", "#58a6ff"
    TITLE_C = "#e6edf3"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 52], fill=BAR)
    f_chrome = fnt("mono", 15)
    d.text((24, 17), "( )( )( )   ~/career-os", font=f_chrome, fill=MUTED)
    hline(d, 0, 52, W, BORDER, 1)

    f_mono = fnt("mono", 22)
    lm = 56
    prompt_y = 88
    d.text((lm, prompt_y), "$ career --status", font=f_mono, fill=BLUE)
    _, ph = measure(d, "$ career --status", f_mono)
    log_y = prompt_y + ph + 16
    lines = [
        (GREEN, "[OK] 6 databases active"),
        (GREEN, "[OK] Stripe [Interviewing · React Senior]"),
        (GREEN, "[OK] DevTracker · 142 stars on GitHub"),
        (GREEN, "[OK] AWS Solutions Architect passed"),
        (BLUE,  "[..] Railway · Offer pending"),
        (GREEN, "[OK] 6 active applications"),
        (GREEN, "[OK] Sarah Chen (Stripe) · mentor"),
    ]
    for col, txt in lines:
        d.text((lm, log_y), txt, font=f_mono, fill=col)
        _, lh = measure(d, txt, f_mono)
        log_y += lh + 12

    d.text((lm, log_y + 8), "| ", font=f_mono, fill=GREEN)
    sep_y = log_y + 56
    hline(d, lm, sep_y, W - lm * 2, BORDER, 1)

    # Title + tagline fill lower half
    title_y = sep_y + 48
    f_title = fnt("semi", 48)
    d.text((lm, title_y), "Developer Career OS", font=f_title, fill=TITLE_C)
    _, tith = measure(d, "Developer Career OS", f_title)

    tag_y = title_y + tith + 24
    f_tag = fnt("regular", 24)
    tags = ["The system that shows your", "career growth before the", "interviewer asks"]
    ty = tag_y
    for t in tags:
        d.text((lm, ty), t, font=f_tag, fill=MUTED)
        _, th = measure(d, t, f_tag)
        ty += th + 10

    f_brand = fnt("mono", 15)
    d.text((lm, H - 56), "RodeShop · $19", font=f_brand, fill=MUTED)

    save_png(img, "direction-02--thumb-1200x1200.png")


# ─── DIRECTION 03 — CAREER ARTIFACT ──────────────────────────────────────────

def d03_cover():
    W, H = 1920, 1080
    BG, INK, MUTED = "#ffffff", "#0a0a0a", "#6b7280"
    SEP, ACCENT = "#e5e7eb", "#0077B5"
    BAR_BG, BAR_FILL = "#e0e7ef", "#0077B5"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    lm, rm = 120, 120

    f_title = fnt("bold", 80)
    title = "DEVELOPER CAREER OS"
    d.text((lm, 88), title, font=f_title, fill=INK)
    _, tith = measure(d, title, f_title)

    rule_y = 88 + tith + 20
    hline(d, lm, rule_y, W - lm - rm, ACCENT, 3)

    tag_y = rule_y + 3 + 28
    f_tag = fnt("regular", 28)
    tag1 = "The system that shows your career"
    tag2 = "growth before the interviewer asks"
    d.text((lm, tag_y), tag1, font=f_tag, fill=MUTED)
    _, t1h = measure(d, tag1, f_tag)
    d.text((lm, tag_y + t1h + 8), tag2, font=f_tag, fill=MUTED)
    _, t2h = measure(d, tag2, f_tag)

    # Three-column section — placed so it fills the lower 2/3 of canvas
    section_top = tag_y + t1h + 8 + t2h + 64
    col_w = (W - lm - rm) // 3
    col_x = [lm, lm + col_w, lm + col_w * 2]
    col_headers = ["EXPERIENCE", "SKILLS", "STATUS"]
    f_col_h = fnt("bold", 20)
    f_col_b = fnt("regular", 26)

    # Calculate row height to fill remaining space
    remaining = H - 88 - section_top
    row_h = max(40, remaining // 7)

    for i, (cx, ch) in enumerate(zip(col_x, col_headers)):
        d.text((cx, section_top), ch, font=f_col_h, fill=INK)
        _, chh = measure(d, ch, f_col_h)
        hline(d, cx, section_top + chh + 10, col_w - 32, SEP, 1)
        row_y = section_top + chh + 28

        if i == 0:
            rows = [
                ("Projects", "10"),
                ("Shipped", "7"),
                ("GitHub Stars", "142"),
                ("Active apps", "6"),
                ("Certifications", "1"),
            ]
            for label, val in rows:
                d.text((cx, row_y), label, font=f_col_b, fill=MUTED)
                d.text((cx + col_w - rm - 32, row_y), val, font=fnt("bold", 26), fill=INK)
                row_y += row_h

        elif i == 1:
            skills = [
                ("React", 8, "Advanced · 800h"),
                ("TypeScript", 6, "Advanced · 600h"),
                ("Node.js", 5, "Intermediate"),
                ("Go", 3, "Beginner · 80h"),
                ("Rust", 1, "Learning"),
            ]
            bar_h = 12
            bar_max = col_w - 80
            for skill_name, level, label_text in skills:
                d.text((cx, row_y), skill_name, font=f_col_b, fill=INK)
                sw, sh = measure(d, skill_name, f_col_b)
                d.text((cx + sw + 16, row_y + 4), label_text, font=fnt("regular", 18), fill=MUTED)
                bar_y = row_y + sh + 8
                filled = int(bar_max * level / 10)
                d.rectangle([cx, bar_y, cx + bar_max, bar_y + bar_h], fill=BAR_BG)
                d.rectangle([cx, bar_y, cx + filled, bar_y + bar_h], fill=BAR_FILL)
                row_y = bar_y + bar_h + (row_h - sh - 8 - bar_h)

        else:
            status_rows = [
                ("Interviewing", ACCENT),
                ("@ Stripe", INK),
                ("$180 – 220k", INK),
                ("Railway · Offer", "#16a34a"),
                ("6 applications", MUTED),
            ]
            for sr, sc in status_rows:
                d.text((cx, row_y), sr, font=f_col_b, fill=sc)
                row_y += row_h

    # Bottom separator + brand
    hline(d, lm, H - 80, W - lm - rm, SEP, 1)
    f_brand = fnt("regular", 20)
    d.text((lm, H - 56), "RodeShop", font=f_brand, fill=MUTED)
    f_price = fnt("bold", 20)
    price_w, _ = measure(d, "$19", f_price)
    d.text((W - rm - price_w, H - 56), "$19", font=f_price, fill=ACCENT)

    save_png(img, "direction-03--cover-1920x1080.png")


def d03_thumb():
    W, H = 1200, 1200
    BG, INK, MUTED = "#ffffff", "#0a0a0a", "#6b7280"
    SEP, ACCENT = "#e5e7eb", "#0077B5"
    BAR_BG, BAR_FILL = "#e0e7ef", "#0077B5"

    # Pre-measure to vertically center
    dummy_img = Image.new("RGB", (1, 1))
    dummy = ImageDraw.Draw(dummy_img)
    lm = 80
    f_title = fnt("bold", 56)
    f_col_h = fnt("bold", 16)
    f_col_b = fnt("regular", 22)
    f_tag = fnt("regular", 22)
    f_brand = fnt("bold", 18)

    t1h = measure(dummy, "DEVELOPER", f_title)[1]
    t2h = measure(dummy, "CAREER OS", f_title)[1]
    rule_h = 3
    chh = measure(dummy, "SKILLS", f_col_h)[1]
    bar_h = 16
    skill_row_h = measure(dummy, "React", f_col_b)[1] + 6 + bar_h + 20
    n_skills = 4
    tag_line_h = measure(dummy, "The system", f_tag)[1]
    n_tags = 3

    block_h = (t1h + 8 + t2h + 20 + rule_h +   # title block
               32 + chh + 12 + 1 +               # col headers + separator
               skill_row_h * n_skills +           # skill rows
               32 + 1 + 24 +                      # separator + tagline gap
               tag_line_h * n_tags + 8 * (n_tags - 1))  # tagline

    y0 = max(64, (H - block_h) // 2 - 32)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.text((lm, y0), "DEVELOPER", font=f_title, fill=INK)
    d.text((lm, y0 + t1h + 8), "CAREER OS", font=f_title, fill=INK)
    rule_y = y0 + t1h + 8 + t2h + 20
    hline(d, lm, rule_y, W - lm * 2, ACCENT, 3)

    cx_left, cx_right = lm, lm + (W - lm * 2) // 2
    col_top = rule_y + 3 + 32

    d.text((cx_left, col_top), "SKILLS", font=f_col_h, fill=INK)
    d.text((cx_right, col_top), "STATUS", font=f_col_h, fill=INK)
    hline(d, lm, col_top + chh + 12, W - lm * 2, SEP, 1)

    row_y = col_top + chh + 28
    bar_max = (W - lm * 2) // 2 - 24
    skills = [("React", 8), ("TypeScript", 6), ("Go", 4), ("Rust", 2)]
    for skill_name, level in skills:
        d.text((cx_left, row_y), skill_name, font=f_col_b, fill=INK)
        # Use ink_bottom so bar starts AFTER actual ink bottom, not measure height
        ib = ink_bottom(d, skill_name, f_col_b)
        bar_y = row_y + ib + 6
        filled = int(bar_max * level / 10)
        d.rectangle([cx_left, bar_y, cx_left + bar_max, bar_y + bar_h], fill=BAR_BG)
        d.rectangle([cx_left, bar_y, cx_left + filled, bar_y + bar_h], fill=BAR_FILL)
        row_y = bar_y + bar_h + 20

    status_y = col_top + chh + 28
    status_rows = ["Searching", "6 applications", "React · Stripe", "Railway offer"]
    for sr in status_rows:
        d.text((cx_right, status_y), sr, font=f_col_b, fill=INK)
        _, srh = measure(d, sr, f_col_b)
        status_y += srh + 20

    sep_y = max(row_y, status_y) + 32
    hline(d, lm, sep_y, W - lm * 2, SEP, 1)
    tag_y = sep_y + 1 + 28
    tags = ["The system that shows your", "career growth before the", "interviewer asks"]
    ty = tag_y
    for t in tags:
        d.text((lm, ty), t, font=f_tag, fill=MUTED)
        _, th = measure(d, t, f_tag)
        ty += th + 8

    # Brand — fixed at bottom, regardless of centering
    d.text((lm, H - 56), "RodeShop · $19", font=f_brand, fill=ACCENT)

    save_png(img, "direction-03--thumb-1200x1200.png")


# ─── DIRECTION 04 — BLUEPRINT GRID ───────────────────────────────────────────

def draw_node(draw, cx, cy, label, nw=200, nh=56, bg="#0f2035",
              border="#2a5298", text_c="#e8f4ff"):
    x, y = cx - nw // 2, cy - nh // 2
    rounded_rect(draw, x, y, nw, nh, 8, bg, border, 2)
    f = fnt("semi", 20)
    d_temp = draw
    tw, th = measure(d_temp, label, f)
    d_temp.text((cx - tw // 2, cy - th // 2), label, font=f, fill=text_c)
    return x, y, nw, nh


def draw_ortho_line(draw, x1, y1, x2, y2, color="#4A9EFF", t=2):
    """L-shaped Manhattan routing"""
    mid_x = (x1 + x2) // 2
    draw.rectangle([min(x1, mid_x), y1, max(x1, mid_x), y1 + t], fill=color)
    draw.rectangle([mid_x, min(y1, y2), mid_x + t, max(y1, y2)], fill=color)
    draw.rectangle([mid_x, y2, max(mid_x, x2), y2 + t], fill=color)


def d04_cover():
    W, H = 1920, 1080
    BG = "#0a1628"
    TEXT, MUTED, ACCENT = "#e8f4ff", "#6b8cad", "#4A9EFF"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Dot grid
    dot_grid(d, W, H, 32, "#1a2d46")

    # Title block left
    lm = 96
    f_title = fnt("bold", 72)
    d.text((lm, 96), "Developer Career OS", font=f_title, fill=TEXT)
    _, tith = measure(d, "Developer Career OS", f_title)

    tag_y = 96 + tith + 24
    f_tag = fnt("regular", 24)
    d.text((lm, tag_y), "The system that shows your career growth", font=f_tag, fill=MUTED)
    _, t1h = measure(d, "The system that shows your career growth", f_tag)
    d.text((lm, tag_y + t1h + 8), "before the interviewer asks", font=f_tag, fill=MUTED)

    # Node positions — right side
    # Layout in right portion x=800..1824
    nodes = {
        "Projects":     (1100, 400),
        "Skills":       (1400, 280),
        "Learning":     (1650, 400),
        "Jobs":         (1100, 650),
        "Networking":   (1400, 650),
        "Achievements": (1100, 840),
    }
    nw, nh = 220, 56

    for label, (cx, cy) in nodes.items():
        draw_node(d, cx, cy, label, nw, nh)

    # Connections (from spec.json relations)
    connections = [
        ("Projects", "Skills"),
        ("Projects", "Jobs"),
        ("Projects", "Achievements"),
        ("Skills", "Learning"),
        ("Jobs", "Networking"),
    ]
    for src, dst in connections:
        sx, sy = nodes[src]
        dx, dy = nodes[dst]
        draw_ortho_line(d, sx, sy, dx, dy, ACCENT, 2)

    # Brand
    f_brand = fnt("regular", 20)
    d.text((lm, H - 64), "RodeShop · $19", font=f_brand, fill=MUTED)

    save_png(img, "direction-04--cover-1920x1080.png")


def d04_thumb():
    W, H = 1200, 1200
    BG = "#0a1628"
    TEXT, MUTED, ACCENT = "#e8f4ff", "#6b8cad", "#4A9EFF"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    dot_grid(d, W, H, 32, "#1a2d46")

    lm = 72
    f_title = fnt("bold", 56)
    d.text((lm, 72), "Developer Career OS", font=f_title, fill=TEXT)
    _, tith = measure(d, "Developer Career OS", f_title)

    tag_y = 72 + tith + 20
    f_tag = fnt("regular", 20)
    d.text((lm, tag_y), "The system that shows your career growth", font=f_tag, fill=MUTED)
    _, t1h = measure(d, "The system that shows your career growth", f_tag)
    d.text((lm, tag_y + t1h + 6), "before the interviewer asks", font=f_tag, fill=MUTED)

    # Compact 5-node diagram
    nodes = {
        "Projects":    (440, 560),
        "Skills":      (700, 440),
        "Jobs":        (440, 720),
        "Networking":  (700, 720),
        "Learning":    (900, 560),
    }
    nw, nh = 180, 48
    for label, (cx, cy) in nodes.items():
        draw_node(d, cx, cy, label, nw, nh)

    connections = [
        ("Projects", "Skills"),
        ("Projects", "Jobs"),
        ("Jobs", "Networking"),
        ("Skills", "Learning"),
    ]
    for src, dst in connections:
        sx, sy = nodes[src]
        dx, dy = nodes[dst]
        draw_ortho_line(d, sx, sy, dx, dy, ACCENT, 2)

    # +Achievements label
    f_note = fnt("regular", 16)
    d.text((lm + 16, 900), "+Achievements", font=f_note, fill=MUTED)

    f_brand = fnt("regular", 18)
    d.text((lm, H - 56), "RodeShop · $19", font=f_brand, fill=MUTED)

    save_png(img, "direction-04--thumb-1200x1200.png")


# ─── DIRECTION 05 — BOLD POSTER ──────────────────────────────────────────────

def d05_cover():
    W, H = 1920, 1080
    BG, INK, MUTED, ACCENT, RULE = "#fafafa", "#0a0a0a", "#6b7280", "#2563EB", "#d1d5db"

    dummy_img = Image.new("RGB", (1, 1))
    dummy = ImageDraw.Draw(dummy_img)
    f_over  = fnt("regular", 64)
    f_os    = fnt("bold", 320)
    f_tag   = fnt("regular", 26)
    f_db    = fnt("regular", 20)
    f_brand = fnt("regular", 18)

    # Use ink_bottom() — actual distance from anchor to bottom of rendered ink
    over_ib  = ink_bottom(dummy, "Developer Career", f_over)   # 85
    over_it  = ink_top(dummy, "Developer Career", f_over)      # 23
    over_ink_h = over_ib - over_it                             # 62
    os_ib    = ink_bottom(dummy, "OS", f_os)                   # 350
    os_it    = ink_top(dummy, "OS", f_os)                      # 118
    os_ink_h = os_ib - os_it                                   # 232
    tag1_ib  = ink_bottom(dummy, "The system that shows your career growth", f_tag)
    tag1_it  = ink_top(dummy, "The system that shows your career growth", f_tag)
    tag2_ib  = ink_bottom(dummy, "before the interviewer asks", f_tag)
    db_ib    = ink_bottom(dummy, "Projects · Jobs · Skills · Learning · Networking · Achievements", f_db)
    db_it    = ink_top(dummy, "Projects · Jobs · Skills · Learning · Networking · Achievements", f_db)

    # Total ink-to-ink height of the block
    GAP_R1  = 20   # overline ink bottom → rule1
    GAP_OS  = 16   # rule1 → OS ink top
    GAP_R2  = 24   # OS ink bottom → rule2
    GAP_TAG = 40   # rule2 → tagline ink top
    GAP_DB  = 24   # tagline2 ink bottom → db ink top

    block_h = (over_ink_h + GAP_R1 + 1 + GAP_OS + os_ink_h
               + GAP_R2 + 1 + GAP_TAG + (tag1_ib - tag1_it) + 8 + (tag2_ib - tag1_it)
               + GAP_DB + (db_ib - db_it))
    # First ink pixel y
    ink_y0 = max(48, (H - block_h) // 2)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Overline — anchor so ink top is at ink_y0
    over_anchor_y = ink_y0 - over_it
    ow, _ = measure(d, "Developer Career", f_over)
    d.text(((W - ow) // 2, over_anchor_y), "Developer Career", font=f_over, fill=INK)
    rule1_y = ink_y0 + over_ink_h + GAP_R1
    hline(d, 0, rule1_y, W, RULE, 1)

    # OS — anchor so ink top is at rule1_y + 1 + GAP_OS
    os_ink_top_y = rule1_y + 1 + GAP_OS
    os_anchor_y = os_ink_top_y - os_it
    osw, _ = measure(d, "OS", f_os)
    d.text(((W - osw) // 2, os_anchor_y), "OS", font=f_os, fill=ACCENT)

    # Rule2 — placed AFTER os ink bottom
    os_ink_bot_y = os_ink_top_y + os_ink_h
    rule2_y = os_ink_bot_y + GAP_R2
    hline(d, 0, rule2_y, W, RULE, 1)

    # Tagline — anchor so ink top is at rule2_y + 1 + GAP_TAG
    tag_ink_top_y = rule2_y + 1 + GAP_TAG
    tag_anchor_y = tag_ink_top_y - tag1_it
    tag1 = "The system that shows your career growth"
    tag2 = "before the interviewer asks"
    tw1, th1 = measure(d, tag1, f_tag)
    tw2, th2 = measure(d, tag2, f_tag)
    d.text(((W - tw1) // 2, tag_anchor_y), tag1, font=f_tag, fill=MUTED)
    d.text(((W - tw2) // 2, tag_anchor_y + th1 + 8), tag2, font=f_tag, fill=MUTED)

    # DB list
    tag2_ink_bot = tag_anchor_y + ink_bottom(d, tag2, f_tag) + th1 + 8
    db_anchor_y = tag2_ink_bot + GAP_DB - db_it
    db_text = "Projects · Jobs · Skills · Learning · Networking · Achievements"
    dbw, _ = measure(d, db_text, f_db)
    d.text(((W - dbw) // 2, db_anchor_y), db_text, font=f_db, fill=MUTED)

    d.text((120, H - 56), "RodeShop", font=f_brand, fill=MUTED)
    f_price = fnt("bold", 18)
    pw, _ = measure(d, "$19", f_price)
    d.text((W - 120 - pw, H - 56), "$19", font=f_price, fill=ACCENT)

    save_png(img, "direction-05--cover-1920x1080.png")


def d05_thumb():
    W, H = 1200, 1200
    BG, INK, MUTED, ACCENT, RULE = "#fafafa", "#0a0a0a", "#6b7280", "#2563EB", "#d1d5db"

    dummy_img = Image.new("RGB", (1, 1))
    dummy = ImageDraw.Draw(dummy_img)
    f_over  = fnt("regular", 48)
    f_os    = fnt("bold", 240)
    f_tag   = fnt("regular", 22)
    f_db    = fnt("regular", 18)
    f_brand = fnt("regular", 18)

    over_ib = ink_bottom(dummy, "Developer Career", f_over)
    over_it = ink_top(dummy, "Developer Career", f_over)
    os_ib   = ink_bottom(dummy, "OS", f_os)      # 262
    os_it   = ink_top(dummy, "OS", f_os)          # 88
    os_ink_h = os_ib - os_it                      # 174
    tags = ["The system that shows", "your career growth", "before the interviewer asks"]
    tag_it  = ink_top(dummy, tags[0], f_tag)
    tag_ib  = ink_bottom(dummy, tags[0], f_tag)
    tag_ink_h = tag_ib - tag_it
    db_it   = ink_top(dummy, "6 databases · Projects · Jobs · Skills", f_db)
    db_ib   = ink_bottom(dummy, "6 databases · Projects · Jobs · Skills", f_db)

    block_h = ((over_ib - over_it) + 20 + 1 + 16 + os_ink_h
               + 20 + 1 + 40 + (tag_ink_h + 8) * len(tags) + 20 + (db_ib - db_it))
    ink_y0 = max(48, (H - block_h) // 2)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    over_anchor_y = ink_y0 - over_it
    ow, _ = measure(d, "Developer Career", f_over)
    d.text(((W - ow) // 2, over_anchor_y), "Developer Career", font=f_over, fill=INK)

    rule1_y = ink_y0 + (over_ib - over_it) + 20
    hline(d, 0, rule1_y, W, RULE, 1)

    os_ink_top_y = rule1_y + 1 + 16
    os_anchor_y = os_ink_top_y - os_it
    osw, _ = measure(d, "OS", f_os)
    d.text(((W - osw) // 2, os_anchor_y), "OS", font=f_os, fill=ACCENT)

    os_ink_bot_y = os_ink_top_y + os_ink_h
    rule2_y = os_ink_bot_y + 20
    hline(d, 0, rule2_y, W, RULE, 1)

    tag_ink_top_y = rule2_y + 1 + 40
    tag_anchor_y = tag_ink_top_y - tag_it
    ty = tag_anchor_y
    for t in tags:
        tw, th = measure(d, t, f_tag)
        d.text(((W - tw) // 2, ty), t, font=f_tag, fill=MUTED)
        ty += th + 8

    db_anchor_y = ty + 20 - db_it
    db_text = "6 databases · Projects · Jobs · Skills"
    dbw, _ = measure(d, db_text, f_db)
    d.text(((W - dbw) // 2, db_anchor_y), db_text, font=f_db, fill=MUTED)

    brand = "RodeShop · $19"
    bw, _ = measure(d, brand, f_brand)
    d.text(((W - bw) // 2, H - 56), brand, font=f_brand, fill=MUTED)

    save_png(img, "direction-05--thumb-1200x1200.png")


# ─── RUN ALL ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Direction 01 — Swiss Command")
    d01_cover()
    d01_thumb()
    print("Direction 02 — Terminal Native")
    d02_cover()
    d02_thumb()
    print("Direction 03 — Career Artifact")
    d03_cover()
    d03_thumb()
    print("Direction 04 — Blueprint Grid")
    d04_cover()
    d04_thumb()
    print("Direction 05 — Bold Poster")
    d05_cover()
    d05_thumb()
    print("\nDone — 10 PNG in", OUT)
