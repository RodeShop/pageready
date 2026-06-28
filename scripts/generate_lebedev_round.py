"""
Lebedev Round — Developer Career OS
5 directions, 10 PNGs: cover 1920x1080 + thumb 1200x1200
Pass 1 + Pass 2 applied before writing any code.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = "assets/gumroad-variants/notion-developer-career-os/lebedev-round"
os.makedirs(OUT, exist_ok=True)

# ── Font registry ─────────────────────────────────────────────────────────────
W_FONTS = "C:/Windows/Fonts/"

def load_font(candidates, size):
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

F = {
    "impact":   lambda s: load_font([W_FONTS+"impact.ttf"], s),
    "black":    lambda s: load_font([W_FONTS+"seguibl.ttf", W_FONTS+"arialbd.ttf"], s),
    "bold":     lambda s: load_font([W_FONTS+"segoeuib.ttf", W_FONTS+"arialbd.ttf"], s),
    "semi":     lambda s: load_font([W_FONTS+"seguisb.ttf",  W_FONTS+"segoeuib.ttf"], s),
    "regular":  lambda s: load_font([W_FONTS+"segoeui.ttf",  W_FONTS+"arial.ttf"], s),
    "light":    lambda s: load_font([W_FONTS+"segoeuil.ttf", W_FONTS+"segoeui.ttf"], s),
    "mono":     lambda s: load_font([W_FONTS+"consola.ttf",  W_FONTS+"cour.ttf"], s),
    "monob":    lambda s: load_font([W_FONTS+"consolab.ttf", W_FONTS+"courbd.ttf"], s),
    "cour":     lambda s: load_font([W_FONTS+"cour.ttf",     W_FONTS+"consola.ttf"], s),
    "courb":    lambda s: load_font([W_FONTS+"courbd.ttf",   W_FONTS+"consolab.ttf"], s),
}

# ── Measurement helpers ───────────────────────────────────────────────────────
_dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))

def bbox(text, font):
    b = _dummy.textbbox((0, 0), text, font=font)
    return b  # (left, top, right, bottom)

def tw(text, font):
    b = bbox(text, font)
    return b[2] - b[0]

def th(text, font):
    b = bbox(text, font)
    return b[3] - b[1]

def ink_top(text, font):
    return bbox(text, font)[1]

def ink_bot(text, font):
    return bbox(text, font)[3]

def draw_text_centered(d, x_center, anchor_y, text, font, fill):
    w = tw(text, font)
    d.text((x_center - w // 2, anchor_y), text, font=font, fill=fill)

def draw_text_left(d, x, anchor_y, text, font, fill):
    d.text((x, anchor_y), text, font=font, fill=fill)

def draw_text_right(d, x_right, anchor_y, text, font, fill):
    w = tw(text, font)
    d.text((x_right - w, anchor_y), text, font=font, fill=fill)

def save(img, slug):
    path = os.path.join(OUT, slug)
    img.save(path, "PNG")
    print(f"  saved {slug}")

# ── DIRECTION H1: POSTER ──────────────────────────────────────────────────────
# Impact font, pure white BG, red "OS" 2× size of title.
# Signature: two black lines (DEVELOPER / CAREER) → red rule → giant red OS.
# Spend boldness only on the size+color break at OS.

def h1_cover():
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(img)

    MARGIN = 96
    CX = W // 2

    # Fonts
    f_title = F["impact"](160)    # DEVELOPER, CAREER — black
    f_os    = F["impact"](320)    # OS — red, dominant
    f_tag   = F["regular"](30)
    f_brand = F["mono"](22)

    RED   = "#cc0000"
    INK   = "#111111"
    MUTED = "#777777"

    # Measure title block height to center on canvas
    dev_h  = ink_bot("DEVELOPER", f_title) - ink_top("DEVELOPER", f_title)
    car_h  = ink_bot("CAREER", f_title) - ink_top("CAREER", f_title)
    os_h   = ink_bot("OS", f_os) - ink_top("OS", f_os)
    tag_h  = ink_bot("Developer Career OS", f_tag) - ink_top("Developer Career OS", f_tag)

    RULE_H   = 6
    GAP_LINE = 16   # between DEVELOPER and CAREER
    GAP_RULE = 32   # above/below red rule
    GAP_TAG  = 40   # above tagline

    block_h = (dev_h + GAP_LINE + car_h + GAP_RULE + RULE_H +
               GAP_RULE + os_h + GAP_TAG + tag_h)
    y = (H - block_h) // 2

    # DEVELOPER
    it = ink_top("DEVELOPER", f_title)
    draw_text_centered(d, CX, y - it, "DEVELOPER", f_title, INK)
    y += dev_h + GAP_LINE

    # CAREER
    it = ink_top("CAREER", f_title)
    draw_text_centered(d, CX, y - it, "CAREER", f_title, INK)
    y += car_h + GAP_RULE

    # Red rule
    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RED)
    y += RULE_H + GAP_RULE

    # OS — red, giant
    it = ink_top("OS", f_os)
    draw_text_centered(d, CX, y - it, "OS", f_os, RED)
    y += os_h + GAP_TAG

    # Tagline
    tag = "The system that shows your career growth before the interviewer asks"
    it = ink_top(tag, f_tag)
    draw_text_centered(d, CX, y - it, tag, f_tag, MUTED)

    # Brand bottom
    f_br = F["mono"](22)
    brand = "RodeShop"
    price = "$19"
    bot = H - 40
    it = ink_top(brand, f_br)
    draw_text_left(d, MARGIN, bot - it, brand, f_br, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, price, f_br, RED)

    save(img, "h1--cover-1920x1080.png")


def h1_thumb():
    W, H = 1200, 1200
    img = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(img)

    MARGIN = 72
    CX = W // 2

    f_title = F["impact"](108)
    f_os    = F["impact"](240)
    f_tag   = F["regular"](24)
    f_brand = F["mono"](20)

    RED   = "#cc0000"
    INK   = "#111111"
    MUTED = "#777777"

    dev_h = ink_bot("DEVELOPER", f_title) - ink_top("DEVELOPER", f_title)
    car_h = ink_bot("CAREER", f_title) - ink_top("CAREER", f_title)
    os_h  = ink_bot("OS", f_os) - ink_top("OS", f_os)
    tag1  = "The system that shows"
    tag2  = "your career growth"
    t1h   = ink_bot(tag1, f_tag) - ink_top(tag1, f_tag)
    t2h   = ink_bot(tag2, f_tag) - ink_top(tag2, f_tag)

    RULE_H   = 5
    GAP_LINE = 12
    GAP_RULE = 24
    GAP_TAG  = 32
    GAP_LINES = 8

    block_h = (dev_h + GAP_LINE + car_h + GAP_RULE + RULE_H +
               GAP_RULE + os_h + GAP_TAG + t1h + GAP_LINES + t2h)
    y = (H - block_h) // 2

    for text, font in [("DEVELOPER", f_title), ("CAREER", f_title)]:
        it = ink_top(text, font)
        draw_text_centered(d, CX, y - it, text, font, INK)
        h = ink_bot(text, font) - it
        y += h + GAP_LINE

    y += GAP_RULE - GAP_LINE
    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RED)
    y += RULE_H + GAP_RULE

    it = ink_top("OS", f_os)
    draw_text_centered(d, CX, y - it, "OS", f_os, RED)
    y += os_h + GAP_TAG

    for text in [tag1, tag2]:
        it = ink_top(text, f_tag)
        draw_text_centered(d, CX, y - it, text, f_tag, MUTED)
        h = ink_bot(text, f_tag) - it
        y += h + GAP_LINES

    # Brand
    bot = H - 36
    it = ink_top("RodeShop", f_brand)
    draw_text_left(d, MARGIN, bot - it, "RodeShop", f_brand, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, "$19", f_brand, RED)

    save(img, "h1--thumb-1200x1200.png")


# ── DIRECTION H2: SPLIT ───────────────────────────────────────────────────────
# 50/50 vertical split. Left: deep indigo + amber terminal lines.
# Right: cool off-white + Segoe UI Light title.
# Signature: the hard vertical boundary + amber console output.

def h2_cover():
    W, H = 1920, 1080
    SPLIT = W // 2

    img = Image.new("RGB", (W, H), "#f7f7f5")
    d = ImageDraw.Draw(img)

    # Left panel
    d.rectangle([0, 0, SPLIT - 1, H], fill="#1e1040")

    INDIGO = "#1e1040"
    AMBER  = "#f0b429"
    WHITE  = "#ffffff"
    LIGHT  = "#f7f7f5"
    INK    = "#1e1040"
    MUTED  = "#888888"

    f_mono  = F["mono"](22)
    f_monob = F["monob"](22)
    f_light = F["light"](80)
    f_semi  = F["semi"](36)
    f_small = F["regular"](26)
    f_brand = F["mono"](20)

    # Left panel — terminal lines
    L_MARGIN = 64
    lines = [
        ("> career-os --status",   WHITE, False),
        ("",                        WHITE, False),
        ("  projects    12",        AMBER, True),
        ("  skills      24",        AMBER, True),
        ("  jobs         8",        AMBER, True),
        ("  connections 31",        WHITE, False),
        ("  achievements 6",        WHITE, False),
        ("",                        WHITE, False),
        ("> skills top",            WHITE, False),
        ("  React       800h  [ADV]",  AMBER, True),
        ("  TypeScript  600h  [ADV]",  AMBER, True),
        ("  Go           80h  [BEG]",  WHITE, False),
        ("",                        WHITE, False),
        ("$ _",                     AMBER, True),
    ]

    total_line_h = len(lines) * 32
    ly = (H - total_line_h) // 2

    for text, color, bold in lines:
        if text == "":
            ly += 32
            continue
        font = f_monob if bold else f_mono
        it = ink_top(text, font)
        d.text((L_MARGIN, ly - it), text, font=font, fill=color)
        ly += 32

    # Right panel — title
    R_MARGIN = 80
    RX = SPLIT + R_MARGIN
    RX_CENTER = SPLIT + (W - SPLIT) // 2

    title1 = "Developer"
    title2 = "Career OS"
    tag    = "The system that shows your career\ngrowth before the interviewer asks"

    t1h = ink_bot(title1, f_light) - ink_top(title1, f_light)
    t2h = ink_bot(title2, f_semi) - ink_top(title2, f_semi)

    GAP_TITLES = 8
    GAP_RULE   = 32
    RULE_H     = 3
    GAP_TAG    = 32

    tag_lines  = tag.split("\n")
    tag_h_each = ink_bot(tag_lines[0], f_small) - ink_top(tag_lines[0], f_small)
    tag_block  = tag_h_each * 2 + 8

    block_h = t1h + GAP_TITLES + t2h + GAP_RULE + RULE_H + GAP_TAG + tag_block
    ry = (H - block_h) // 2

    it = ink_top(title1, f_light)
    d.text((RX, ry - it), title1, font=f_light, fill=INK)
    ry += t1h + GAP_TITLES

    it = ink_top(title2, f_semi)
    d.text((RX, ry - it), title2, font=f_semi, fill=INK)
    ry += t2h + GAP_RULE

    # Amber rule
    d.rectangle([RX, ry, W - R_MARGIN, ry + RULE_H], fill=AMBER)
    ry += RULE_H + GAP_TAG

    for line in tag_lines:
        it = ink_top(line, f_small)
        d.text((RX, ry - it), line, font=f_small, fill=MUTED)
        ry += tag_h_each + 8

    # Brand — bottom right
    bot = H - 40
    it = ink_top("RodeShop  ·  $19", f_brand)
    draw_text_right(d, W - R_MARGIN, bot - it, "RodeShop  ·  $19", f_brand, MUTED)

    save(img, "h2--cover-1920x1080.png")


def h2_thumb():
    W, H = 1200, 1200
    # Square: top 40% dark (indigo), bottom 60% light
    SPLIT_Y = int(H * 0.40)

    img = Image.new("RGB", (W, H), "#f7f7f5")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, SPLIT_Y], fill="#1e1040")

    INDIGO = "#1e1040"
    AMBER  = "#f0b429"
    WHITE  = "#ffffff"
    INK    = "#1e1040"
    MUTED  = "#888888"

    f_mono  = F["mono"](20)
    f_monob = F["monob"](20)
    f_light = F["light"](64)
    f_semi  = F["semi"](72)
    f_small = F["regular"](22)
    f_brand = F["mono"](18)

    MARGIN = 64

    # Top panel — terminal snippet
    term_lines = [
        ("> skills top",         WHITE, False),
        ("  React  800h  [ADV]", AMBER, True),
        ("  TypeScript [ADV]",   AMBER, True),
        ("$ _",                  AMBER, True),
    ]
    ty = 48
    for text, color, bold in term_lines:
        font = f_monob if bold else f_mono
        it = ink_top(text, font)
        d.text((MARGIN, ty - it), text, font=font, fill=color)
        ty += 28

    # Bottom panel — title
    title1 = "Developer"
    title2 = "Career OS"
    t1h = ink_bot(title1, f_light) - ink_top(title1, f_light)
    t2h = ink_bot(title2, f_semi) - ink_top(title2, f_semi)
    tag = "Career OS for engineers"
    tagh = ink_bot(tag, f_small) - ink_top(tag, f_small)

    RULE_H = 3
    GAP = 16

    block_h = t1h + GAP + t2h + GAP + RULE_H + GAP + tagh
    by = SPLIT_Y + (H - SPLIT_Y - block_h) // 2

    it = ink_top(title1, f_light)
    d.text((MARGIN, by - it), title1, font=f_light, fill=INK)
    by += t1h + GAP

    it = ink_top(title2, f_semi)
    d.text((MARGIN, by - it), title2, font=f_semi, fill=INK)
    by += t2h + GAP

    d.rectangle([MARGIN, by, W - MARGIN, by + RULE_H], fill=AMBER)
    by += RULE_H + GAP

    it = ink_top(tag, f_small)
    d.text((MARGIN, by - it), tag, font=f_small, fill=MUTED)

    # Brand
    bot = H - 32
    it = ink_top("RodeShop · $19", f_brand)
    draw_text_right(d, W - MARGIN, bot - it, "RodeShop · $19", f_brand, MUTED)

    save(img, "h2--thumb-1200x1200.png")


# ── DIRECTION H3: LEDGER ──────────────────────────────────────────────────────
# Courier New + dot leaders + two tables (Skills, Projects).
# Signature: the page looks like an open accounting ledger.

def make_leader(label, value, col_width, font):
    """Build 'label.......  value' using monospace dot leaders."""
    lw = tw(label, font)
    vw = tw(value, font)
    dot_w = tw(".", font)
    space_w = tw(" ", font)
    # Available space for dots
    available = col_width - lw - vw - space_w * 2
    n_dots = max(3, available // dot_w)
    return f"{label}{'.' * n_dots}  {value}"


def h3_cover():
    W, H = 1920, 1080
    BG     = "#f5f3ee"
    NAVY   = "#1a3a6e"
    DKRED  = "#8a0000"
    RULED  = "#b8b4a8"
    MUTED  = "#888880"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    MARGIN = 96
    COL_W  = W - MARGIN * 2

    f_hdr   = F["courb"](64)   # ledger header
    f_label = F["courb"](22)   # column headers
    f_data  = F["cour"](22)    # data rows
    f_tag   = F["regular"](24)
    f_brand = F["mono"](20)

    # Measure row height
    row_h = ink_bot("Ag", f_data) - ink_top("Ag", f_data) + 8

    # === Header ===
    header = "DEVELOPER CAREER OS"
    date   = "Jun 2025"

    # Start Y: center the whole block
    # Estimate block height
    RULE_H = 2
    GAP    = 16
    N_SKILLS  = 3
    N_PROJ    = 2
    # header + rule + gap + col_headers + rule + N_skills*row + rule + gap + col_headers + rule + N_proj*row + rule + gap + tag
    est_h = (
        (ink_bot(header, f_hdr) - ink_top(header, f_hdr)) +
        GAP + RULE_H + GAP +
        row_h + RULE_H + GAP +
        N_SKILLS * row_h + RULE_H + GAP + RULE_H +
        row_h + RULE_H + GAP +
        N_PROJ * row_h + RULE_H + GAP * 2 +
        (ink_bot("tag", f_tag) - ink_top("tag", f_tag))
    )
    y = (H - est_h) // 2

    # Header line
    hdr_h = ink_bot(header, f_hdr) - ink_top(header, f_hdr)
    it = ink_top(header, f_hdr)
    d.text((MARGIN, y - it), header, font=f_hdr, fill=NAVY)
    it_d = ink_top(date, f_hdr)
    draw_text_right(d, W - MARGIN, y - it_d, date, f_hdr, MUTED)
    y += hdr_h + GAP

    # Top rule
    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=NAVY)
    y += RULE_H + GAP

    # SKILLS section header
    skills_hdr = "SKILL                         HRS    LEVEL"
    it = ink_top(skills_hdr, f_label)
    d.text((MARGIN, y - it), skills_hdr, font=f_label, fill=NAVY)
    y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP // 2

    # Skills data
    skills = [
        ("React",          "800h",  "Advanced"),
        ("TypeScript",     "600h",  "Advanced"),
        ("Go",              "80h",  "Beginner"),
    ]
    # Column positions for monospace layout
    # Build fixed-width strings (Courier New is monospace)
    for skill, hrs, level in skills:
        line = f"{skill:<22}  {hrs:>6}   {level}"
        it = ink_top(line, f_data)
        d.text((MARGIN, y - it), line, font=f_data, fill=NAVY)
        y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP

    # PROJECTS section header
    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=NAVY)
    y += RULE_H + GAP // 2

    proj_hdr = "PROJECT                       STATUS       STARS"
    it = ink_top(proj_hdr, f_label)
    d.text((MARGIN, y - it), proj_hdr, font=f_label, fill=NAVY)
    y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP // 2

    projects = [
        ("DevTracker",   "Shipped",  "142"),
        ("CLI Tool",     "Building",  "28"),
    ]
    for proj, status, stars in projects:
        line = f"{proj:<22}  {status:<12} {stars:>4} *"
        it = ink_top(line, f_data)
        d.text((MARGIN, y - it), line, font=f_data, fill=NAVY)
        y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP * 2

    # Tagline
    tag = "The system that shows your career growth before the interviewer asks"
    it = ink_top(tag, f_tag)
    d.text((MARGIN, y - it), tag, font=f_tag, fill=MUTED)

    # Brand
    bot = H - 36
    it = ink_top("RodeShop", f_brand)
    draw_text_left(d, MARGIN, bot - it, "RodeShop", f_brand, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, "$19", f_brand, DKRED)

    save(img, "h3--cover-1920x1080.png")


def h3_thumb():
    W, H = 1200, 1200
    BG   = "#f5f3ee"
    NAVY = "#1a3a6e"
    RULED = "#b8b4a8"
    MUTED = "#888880"
    DKRED = "#8a0000"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    MARGIN = 72

    f_hdr   = F["courb"](52)
    f_label = F["courb"](19)
    f_data  = F["cour"](19)
    f_tag   = F["regular"](20)
    f_brand = F["mono"](18)

    row_h = ink_bot("Ag", f_data) - ink_top("Ag", f_data) + 8
    RULE_H = 2
    GAP = 14

    y = 80

    # Header
    header = "DEVELOPER CAREER OS"
    hdr_h = ink_bot(header, f_hdr) - ink_top(header, f_hdr)
    it = ink_top(header, f_hdr)
    d.text((MARGIN, y - it), header, font=f_hdr, fill=NAVY)
    y += hdr_h + GAP

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=NAVY)
    y += RULE_H + GAP

    # Skills
    skills_hdr = "SKILL              HRS   LEVEL"
    it = ink_top(skills_hdr, f_label)
    d.text((MARGIN, y - it), skills_hdr, font=f_label, fill=NAVY)
    y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP // 2

    skills = [
        ("React",       "800h", "Advanced"),
        ("TypeScript",  "600h", "Advanced"),
        ("Go",           "80h", "Beginner"),
    ]
    for skill, hrs, level in skills:
        line = f"{skill:<16}  {hrs:>5}  {level}"
        it = ink_top(line, f_data)
        d.text((MARGIN, y - it), line, font=f_data, fill=NAVY)
        y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=NAVY)
    y += RULE_H + GAP // 2

    # Projects
    proj_hdr = "PROJECT            STATUS    STARS"
    it = ink_top(proj_hdr, f_label)
    d.text((MARGIN, y - it), proj_hdr, font=f_label, fill=NAVY)
    y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP // 2

    for proj, status, stars in [("DevTracker", "Shipped", "142"), ("CLI Tool", "Building", "28")]:
        line = f"{proj:<16}  {status:<9}  {stars:>3} *"
        it = ink_top(line, f_data)
        d.text((MARGIN, y - it), line, font=f_data, fill=NAVY)
        y += row_h

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=RULED)
    y += RULE_H + GAP * 2

    tag = "6 linked databases  ·  Notion template"
    it = ink_top(tag, f_tag)
    d.text((MARGIN, y - it), tag, font=f_tag, fill=MUTED)

    # Brand
    bot = H - 36
    it = ink_top("RodeShop", f_brand)
    draw_text_left(d, MARGIN, bot - it, "RodeShop", f_brand, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, "$19", f_brand, DKRED)

    save(img, "h3--thumb-1200x1200.png")


# ── DIRECTION H4: WEIGHT ──────────────────────────────────────────────────────
# Dark bg. "Developer Career" in Segoe UI Light (thin) vs "OS" in Black (280px).
# Two gold rules bookend OS. Bold move = weight contrast within one family.

def h4_cover():
    W, H = 1920, 1080
    BG    = "#141414"
    WHITE = "#ffffff"
    GOLD  = "#c9a84c"
    MUTED = "#666666"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    MARGIN = 112

    f_light = F["light"](80)
    f_black = F["black"](280)
    f_tag   = F["regular"](27)
    f_brand = F["mono"](20)

    label = "Developer Career"
    os    = "OS"

    label_h = ink_bot(label, f_light) - ink_top(label, f_light)
    os_h    = ink_bot(os, f_black) - ink_top(os, f_black)
    tag     = "The system that shows your career growth"
    tag2    = "before the interviewer asks"
    t1h = ink_bot(tag,  f_tag) - ink_top(tag,  f_tag)
    t2h = ink_bot(tag2, f_tag) - ink_top(tag2, f_tag)

    RULE_H = 2
    GAP_ABOVE = 20
    GAP_BELOW = 24
    GAP_TAG   = 32

    block_h = (label_h + GAP_ABOVE + RULE_H + GAP_BELOW +
               os_h + GAP_BELOW + RULE_H + GAP_TAG + t1h + 8 + t2h)
    y = (H - block_h) // 2

    # "Developer Career" — light
    it = ink_top(label, f_light)
    d.text((MARGIN, y - it), label, font=f_light, fill=WHITE)
    y += label_h + GAP_ABOVE

    # Gold rule 1
    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=GOLD)
    y += RULE_H + GAP_BELOW

    # "OS" — black
    it = ink_top(os, f_black)
    d.text((MARGIN, y - it), os, font=f_black, fill=WHITE)
    y += os_h + GAP_BELOW

    # Gold rule 2
    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=GOLD)
    y += RULE_H + GAP_TAG

    # Tagline
    for line in [tag, tag2]:
        it = ink_top(line, f_tag)
        d.text((MARGIN, y - it), line, font=f_tag, fill=MUTED)
        y += ink_bot(line, f_tag) - ink_top(line, f_tag) + 8

    # Brand
    bot = H - 40
    it = ink_top("RodeShop", f_brand)
    draw_text_left(d, MARGIN, bot - it, "RodeShop", f_brand, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, "$19", f_brand, GOLD)

    save(img, "h4--cover-1920x1080.png")


def h4_thumb():
    W, H = 1200, 1200
    BG    = "#141414"
    WHITE = "#ffffff"
    GOLD  = "#c9a84c"
    MUTED = "#666666"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    MARGIN = 80

    f_light = F["light"](64)
    f_black = F["black"](220)
    f_tag   = F["regular"](24)
    f_brand = F["mono"](18)

    label = "Developer Career"
    os    = "OS"

    label_h = ink_bot(label, f_light) - ink_top(label, f_light)
    os_h    = ink_bot(os, f_black) - ink_top(os, f_black)
    tag     = "The system that shows your"
    tag2    = "career growth"
    t1h = ink_bot(tag, f_tag) - ink_top(tag, f_tag)
    t2h = ink_bot(tag2, f_tag) - ink_top(tag2, f_tag)

    RULE_H = 2
    GAP = 20
    GAP_TAG = 28

    block_h = label_h + GAP + RULE_H + GAP + os_h + GAP + RULE_H + GAP_TAG + t1h + 8 + t2h
    y = (H - block_h) // 2

    it = ink_top(label, f_light)
    d.text((MARGIN, y - it), label, font=f_light, fill=WHITE)
    y += label_h + GAP

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=GOLD)
    y += RULE_H + GAP

    it = ink_top(os, f_black)
    d.text((MARGIN, y - it), os, font=f_black, fill=WHITE)
    y += os_h + GAP

    d.rectangle([MARGIN, y, W - MARGIN, y + RULE_H], fill=GOLD)
    y += RULE_H + GAP_TAG

    for line in [tag, tag2]:
        it = ink_top(line, f_tag)
        d.text((MARGIN, y - it), line, font=f_tag, fill=MUTED)
        y += ink_bot(line, f_tag) - ink_top(line, f_tag) + 8

    bot = H - 36
    it = ink_top("RodeShop", f_brand)
    draw_text_left(d, MARGIN, bot - it, "RodeShop", f_brand, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, "$19", f_brand, GOLD)

    save(img, "h4--thumb-1200x1200.png")


# ── DIRECTION H5: BLUEPRINT ───────────────────────────────────────────────────
# Deep engineering blue + dot grid + 6 database boxes with connector lines.
# Signature: the product's actual structure (6 DBs) drawn as a system diagram.

def draw_box(d, x, y, w, h, label, f_label, line_color, text_color):
    d.rectangle([x, y, x + w, y + h], outline=line_color, width=2)
    lw = tw(label, f_label)
    lh = ink_bot(label, f_label) - ink_top(label, f_label)
    cx = x + (w - lw) // 2
    cy = y + (h - lh) // 2
    it = ink_top(label, f_label)
    d.text((cx, cy - it), label, font=f_label, fill=text_color)


def draw_connector(d, x1, y1, x2, y2, color):
    """L-shaped connector: horizontal first, then vertical."""
    if x1 == x2:
        d.line([(x1, y1), (x2, y2)], fill=color, width=1)
    elif y1 == y2:
        d.line([(x1, y1), (x2, y2)], fill=color, width=1)
    else:
        # go horizontal to x2, then vertical to y2
        d.line([(x1, y1), (x2, y1)], fill=color, width=1)
        d.line([(x2, y1), (x2, y2)], fill=color, width=1)


def h5_cover():
    W, H = 1920, 1080
    BG_DARK  = "#002b55"
    GRID_COL = "#0d4a80"
    WHITE    = "#ffffff"
    ACCENT   = "#4a9eff"
    MUTED    = "#6a9fd0"

    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)

    # Dot grid
    GRID = 64
    for gx in range(0, W, GRID):
        for gy in range(0, H, GRID):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=GRID_COL)

    MARGIN = 96
    f_title = F["semi"](60)
    f_sub   = F["mono"](22)
    f_box   = F["mono"](19)
    f_tag   = F["regular"](23)
    f_brand = F["mono"](19)

    # Title
    title  = "DEVELOPER CAREER OS"
    it = ink_top(title, f_title)
    d.text((MARGIN, 80 - it), title, font=f_title, fill=WHITE)
    ty = 80 + (ink_bot(title, f_title) - ink_top(title, f_title)) + 16

    tag = "The system that shows your career growth before the interviewer asks"
    it = ink_top(tag, f_tag)
    d.text((MARGIN, ty - it), tag, font=f_tag, fill=MUTED)

    # Database diagram — 2 rows × 3 boxes
    databases = [
        "Projects", "Jobs",  "Skills",
        "Learning", "Network", "Achieve"
    ]
    BOX_W  = 200
    BOX_H  = 56
    BOX_COLS = 3
    BOX_GAP_X = 56
    BOX_GAP_Y = 64

    grid_w = BOX_COLS * BOX_W + (BOX_COLS - 1) * BOX_GAP_X
    grid_h = 2 * BOX_H + BOX_GAP_Y

    # Center the diagram
    DX = (W - grid_w) // 2
    DY = (H + 80) // 2 - grid_h // 2  # slightly below center

    # Box centers (for connectors)
    boxes = []
    for row in range(2):
        for col in range(3):
            bx = DX + col * (BOX_W + BOX_GAP_X)
            by = DY + row * (BOX_H + BOX_GAP_Y)
            idx = row * 3 + col
            draw_box(d, bx, by, BOX_W, BOX_H,
                     databases[idx], f_box, ACCENT, WHITE)
            boxes.append((bx + BOX_W // 2, by + BOX_H // 2, bx, by))

    # Connectors: Projects → Jobs, Projects → Skills (row 0 horizontal)
    # Projects → Learning (vertical to row 1)
    # Using box center points
    LINE = "#2a6aaa"
    for i, j in [(0, 1), (1, 2), (0, 3), (1, 4), (3, 4), (4, 5)]:
        bx1, by1, _, _ = boxes[i]
        bx2, by2, _, _ = boxes[j]
        draw_connector(d, bx1, by1, bx2, by2, LINE)

    # Sub label below diagram
    sub = "6 linked databases  ·  Relations  ·  Rollups  ·  Sample data"
    it = ink_top(sub, f_sub)
    sub_y = DY + grid_h + 40
    draw_text_centered(d, W // 2, sub_y - it, sub, f_sub, MUTED)

    # Brand
    bot = H - 40
    it = ink_top("RodeShop", f_brand)
    draw_text_left(d, MARGIN, bot - it, "RodeShop", f_brand, MUTED)
    draw_text_right(d, W - MARGIN, bot - it, "$19", f_brand, WHITE)

    save(img, "h5--cover-1920x1080.png")


def h5_thumb():
    W, H = 1200, 1200
    BG_DARK  = "#002b55"
    GRID_COL = "#0d4a80"
    WHITE    = "#ffffff"
    ACCENT   = "#4a9eff"
    MUTED    = "#6a9fd0"

    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)

    # Dot grid
    GRID = 56
    for gx in range(0, W, GRID):
        for gy in range(0, H, GRID):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=GRID_COL)

    MARGIN = 72
    f_title = F["semi"](52)
    f_box   = F["mono"](18)
    f_brand = F["mono"](18)
    f_sub   = F["mono"](18)

    # Title
    title = "DEVELOPER CAREER OS"
    it = ink_top(title, f_title)
    d.text((MARGIN, 80 - it), title, font=f_title, fill=WHITE)

    # Diagram — 2×3 boxes
    databases = ["Projects", "Jobs", "Skills", "Learning", "Network", "Achieve"]
    BOX_W = 212
    BOX_H = 52
    BOX_GAP_X = 40
    BOX_GAP_Y = 48

    grid_w = 3 * BOX_W + 2 * BOX_GAP_X
    grid_h = 2 * BOX_H + BOX_GAP_Y
    DX = (W - grid_w) // 2
    DY = (H - grid_h) // 2 + 24

    boxes = []
    for row in range(2):
        for col in range(3):
            bx = DX + col * (BOX_W + BOX_GAP_X)
            by = DY + row * (BOX_H + BOX_GAP_Y)
            idx = row * 3 + col
            draw_box(d, bx, by, BOX_W, BOX_H,
                     databases[idx], f_box, ACCENT, WHITE)
            boxes.append((bx + BOX_W // 2, by + BOX_H // 2))

    LINE = "#2a6aaa"
    for i, j in [(0, 1), (1, 2), (0, 3), (1, 4), (3, 4), (4, 5)]:
        draw_connector(d, boxes[i][0], boxes[i][1],
                       boxes[j][0], boxes[j][1], LINE)

    sub = "6 linked databases"
    it = ink_top(sub, f_sub)
    draw_text_centered(d, W // 2, DY + grid_h + 36 - it, sub, f_sub, MUTED)

    # Brand
    bot = H - 36
    it = ink_top("RodeShop  ·  $19", f_brand)
    draw_text_right(d, W - MARGIN, bot - it, "RodeShop  ·  $19", f_brand, WHITE)

    save(img, "h5--thumb-1200x1200.png")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("H1 — Poster (Impact / Red)")
    h1_cover(); h1_thumb()

    print("H2 — Split (Indigo / Amber)")
    h2_cover(); h2_thumb()

    print("H3 — Ledger (Courier New / Navy)")
    h3_cover(); h3_thumb()

    print("H4 — Weight (Light vs Black / Gold)")
    h4_cover(); h4_thumb()

    print("H5 — Blueprint (Navy grid / System diagram)")
    h5_cover(); h5_thumb()

    print("\nDone. 10 PNGs in", OUT)
