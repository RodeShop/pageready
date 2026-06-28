#!/usr/bin/env python3
"""Gumroad cover variant previews D/E/F/G — round-2 PNGs."""
import json
import os
from PIL import Image, ImageDraw, ImageFont

SLUG = "notion-developer-career-os"
OUT = f"assets/gumroad-variants/{SLUG}/round-2"
TITLE = "Developer Career OS"
TAGLINE = "The system that shows your career growth before the interviewer asks"
BRAND = "RodeShop · $19"
ROWS = [("DevTracker", "Shipped", "React TS Node", "142", "Side Proj"),
        ("CLI Tool", "Building", "Go PostgreSQL", "28", "Side Proj"),
        ("OSS Lib", "Building", "React TS", "89", "Open Src")]
CHIP = {"Shipped": ("#dbeddb", "#448361"), "Building": ("#d3e5ef", "#337ea9"),
        "Side Proj": ("#e8deee", "#9065b0"), "Open Src": ("#dbeddb", "#448361")}
BOLD = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
REG = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
NODES = {"Projects": (960, 480), "Skills": (1280, 280), "Learning": (1280, 680),
         "Jobs": (480, 680), "Networking": (640, 680), "Achievements": (480, 880)}
EDGES = [("Projects", "Skills"), ("Projects", "Learning"), ("Projects", "Jobs"),
         ("Jobs", "Networking"), ("Jobs", "Achievements"), ("Skills", "Learning")]
PROOFS = ["6 linked databases", "Relations · rollups · sample data",
          "Projects · Jobs · Skills · Learning · Networking · Achievements"]

def F(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def tw(f, t):
    bb = f.getbbox(t)
    return bb[2] - bb[0]

def lh(f):
    bb = f.getbbox("Ag")
    return int((bb[3] - bb[1]) * 1.35)

def wrap(text, f, mw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if tw(f, test) <= mw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [text])

def tag(d, x, y, text, f, color, mw):
    for ln in wrap(text, f, mw):
        d.text((x, y), ln, font=f, fill=color)
        y += lh(f)
    return y

def chip(d, x, y, label, f):
    bg, fg = CHIP.get(label, ("#e3e2e0", "#787774"))
    w = tw(f, label) + 16
    d.rounded_rectangle([(x, y), (x + w, y + lh(f) + 4)], 4, fill=bg)
    d.text((x + 8, y + 2), label, font=f, fill=fg)

def table(d, x, y, w, cols, rows, f_h, f_c, ink="#37352f", border="#e9e9e7"):
    hdrs = ["Name", "Status", "Tech Stack", "Stars", "Type"][:len(cols)]
    cw, rh, zebra = [int(w * r) for r in cols], lh(f_c) + 16, ["#fafafa", "#fff"]
    yy = y
    for i, h in enumerate(hdrs):
        xx = x + sum(cw[:i])
        d.rectangle([(xx, yy), (xx + cw[i], yy + rh)], fill="#f7f7f5", outline=border)
        d.text((xx + 8, yy + 8), h, font=f_h, fill=ink)
    yy += rh
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row[:len(cols)]):
            xx = x + sum(cw[:ci])
            d.rectangle([(xx, yy), (xx + cw[ci], yy + rh)], fill=zebra[ri % 2], outline=border)
            chip(d, xx + 8, yy + 8, cell, f_c) if ci in (1, 4) and cell in CHIP else d.text((xx + 8, yy + 8), cell, font=f_c, fill=ink)
        yy += rh

def mini_table(d, x, y, w, h):
    cols, rh = [0.4, 0.35, 0.25], (h - 32) // 4
    for i, hdr in enumerate(["Name", "Status", "Stars"]):
        xx, cw = x + int(w * sum(cols[:i])), int(w * cols[i])
        d.rectangle([(xx, y + 8), (xx + cw, y + 8 + rh)], fill="#fff", outline="#e9e9e7")
        d.text((xx + 8, y + 16), hdr, font=F(BOLD, 14), fill="#37352f")
    fc = F(REG, 12)
    for ri, row in enumerate(ROWS):
        yy = y + 8 + rh * (ri + 1)
        for ci, val in enumerate((row[0], row[1], row[3])):
            xx, cw = x + int(w * sum(cols[:ci])), int(w * cols[ci])
            d.rectangle([(xx, yy), (xx + cw, yy + rh)], fill=["#fafafa", "#fff"][ri % 2], outline="#e9e9e7")
            chip(d, xx + 8, yy + 8, row[1], fc) if ci == 1 else d.text((xx + 8, yy + 12), val, font=F(REG, 13), fill="#37352f")

def hub_map(d, W, H, scale=1.0, line="#2563EB", ink="#121212"):
    cx, cy = W // 2, H // 2 + 40
    pos = {k: (cx + int((v[0] - 960) * scale), cy + int((v[1] - 480) * scale)) for k, v in NODES.items()}
    fn = F(REG, 20)
    for a, b in EDGES:
        ax, ay, bx, by = *pos[a], *pos[b]
        mx = (ax + bx) // 2
        for seg in [(ax, ay, mx, ay), (mx, ay, mx, by), (mx, by, bx, by)]:
            d.line(seg[:2] + seg[2:], fill=line, width=2)
    nw, nh = 160, 56
    for name, (x, y) in pos.items():
        d.rounded_rectangle([(x - nw // 2 + 3, y - nh // 2 + 4), (x + nw // 2 + 3, y + nh // 2 + 4)], 8, fill="#d2d6dc")
        d.rounded_rectangle([(x - nw // 2, y - nh // 2), (x + nw // 2, y + nh // 2)], 8, fill="#fff")
        d.text((x - tw(fn, name) // 2, y - lh(fn) // 2), name, font=fn, fill=ink)

def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    p = f"{OUT}/{name}"
    img.save(p, "PNG", optimize=True)
    print(f"  {p}")

def canvas(w, h, c):
    img = Image.new("RGB", (w, h), c)
    return img, ImageDraw.Draw(img)

def variant_d():
    ink, muted, bg = "#37352f", "#787774", "#f7f7f5"
    img, d = canvas(1920, 1080, bg)
    d.text((64, 48), TITLE, font=F(BOLD, 40), fill=ink)
    tag(d, 64, 104, TAGLINE, F(REG, 22), muted, 1200)
    d.text((1600, 56), "Projects ▾  table", font=F(REG, 18), fill=muted)
    table(d, 64, 200, 1792, [.22, .14, .32, .1, .22], ROWS, F(BOLD, 24), F(REG, 18), ink)
    d.text((64, 992), BRAND, font=F(BOLD, 24), fill="#2383e2")
    save(img, "variant-D-cover-1920x1080.png")
    img, d = canvas(1200, 1200, bg)
    d.text((48, 48), TITLE, font=F(BOLD, 56), fill=ink)
    ty = tag(d, 48, 120, TAGLINE, F(REG, 28), muted, 1100)
    table(d, 48, ty + 24, 1104, [.4, .32, .28], [(r[0], r[1], r[3]) for r in ROWS], F(BOLD, 26), F(REG, 24), ink)
    d.text((48, 1120), BRAND, font=F(BOLD, 28), fill="#2383e2")
    save(img, "variant-D-thumb-1200x1200.png")

def variant_e():
    bg, accent = "#eef1f5", "#2563EB"
    img, d = canvas(1920, 1080, bg)
    d.text((64, 48), TITLE, font=F(BOLD, 44), fill="#121212")
    tag(d, 64, 104, TAGLINE, F(REG, 22), "#64748b", 720)
    hub_map(d, 1920, 1080)
    d.text((64, 992), BRAND, font=F(BOLD, 24), fill=accent)
    save(img, "variant-E-cover-1920x1080.png")
    img, d = canvas(1200, 1200, bg)
    d.text((48, 40), TITLE, font=F(BOLD, 48), fill="#121212")
    hub_map(d, 1200, 1200, 0.55)
    d.text((48, 1120), BRAND, font=F(BOLD, 24), fill=accent)
    save(img, "variant-E-thumb-1200x1200.png")

def editorial(w, h, title_sz, body_sz, proof_sz, brand_sz, pad, mw):
    img, d = canvas(w, h, "#fafafa")
    ink, muted, accent = "#0a0a0a", "#525252", "#2563EB"
    thumb = h > 1100
    y0 = pad + (80 if thumb else 40)
    d.text((pad, y0), "Developer", font=F(BOLD, title_sz), fill=ink)
    d.text((pad, y0 + title_sz + 8), "Career OS", font=F(BOLD, title_sz), fill=ink)
    ty = tag(d, pad, pad + (256 if thumb else 160), TAGLINE, F(REG, body_sz), muted, mw) + (32 if thumb else 48)
    fp, bar = F(REG, proof_sz), 36 if thumb else 32
    for p in PROOFS:
        d.rectangle([(pad, ty + 8), (pad + 12, ty + bar)], fill=accent)
        d.text((pad + 32, ty), p, font=fp, fill=ink)
        ty += 56 if thumb else 48
    if thumb:
        d.rectangle([(pad, ty + 16), (pad + mw, ty + 19)], fill=accent)
    d.text((pad, h - 80), BRAND, font=F(BOLD, brand_sz), fill=accent)
    return img


def variant_g():
    pink, surf, ink, muted = "#ff90e8", "#f4f4f0", "#000", "#848484"
    img, d = canvas(1920, 1080, "#fff")
    d.rectangle([(0, 0), (1920, 56)], fill=surf)
    d.rectangle([(0, 56), (1920, 57)], fill="#e0e0dc")
    mx, my, mw, mh = 120, 160, 720, 480
    d.rectangle([(mx, my), (mx + mw, my + mh)], fill=surf, outline="#e0e0dc")
    mini_table(d, mx + 24, my + 24, mw - 48, mh - 48)
    rx = 920
    d.text((rx, 160), TITLE, font=F(BOLD, 48), fill=ink)
    d.text((rx, 224), "by RodeShop", font=F(REG, 24), fill=muted)
    ty = tag(d, rx, 288, TAGLINE, F(REG, 26), ink, 880)
    d.text((rx, ty + 32), "$19", font=F(BOLD, 40), fill=ink)
    bx, by, bw, bh = rx, ty + 96, 280, 56
    d.rounded_rectangle([(bx, by), (bx + bw, by + bh)], 8, fill=pink)
    d.text((bx + 48, by + 14), "I want this!", font=F(BOLD, 24), fill=ink)
    d.text((rx, by + 80), "6 databases · Notion template", font=F(REG, 20), fill=muted)
    save(img, "variant-G-cover-1920x1080.png")
    img, d = canvas(1200, 1200, surf)
    ox, oy, cw, ch = 60, 40, 1080, 1120
    d.rounded_rectangle([(ox + 4, oy + 6), (ox + cw + 4, oy + ch + 6)], 16, fill="#d8d8d4")
    d.rounded_rectangle([(ox, oy), (ox + cw, oy + ch)], 16, fill="#fff")
    ph = int(cw * 9 / 16)
    d.rectangle([(ox + 16, oy + 16), (ox + cw - 16, oy + 16 + ph)], fill=surf, outline="#e0e0dc")
    mini_table(d, ox + 32, oy + 32, cw - 64, ph - 32)
    ty = oy + 16 + ph + 24
    d.text((ox + 24, ty), TITLE, font=F(BOLD, 36), fill=ink)
    d.text((ox + 24, ty + 48), "RodeShop", font=F(REG, 24), fill=muted)
    d.text((ox + 24, ty + 96), "$19", font=F(BOLD, 32), fill=ink)
    save(img, "variant-G-thumb-1200x1200.png")

def main():
    global TITLE, TAGLINE, BRAND
    p = f"products/draft/{SLUG}/spec.json"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            s = json.load(f)
        TITLE, TAGLINE = s.get("title", TITLE), s.get("tagline", TAGLINE)
        BRAND = f"RodeShop · ${s.get('price', 19)}"
    print(f"Generating round-2 variants for {TITLE}")
    variant_d(); variant_e()
    save(editorial(1920, 1080, 88, 24, 24, 24, 120, 900), "variant-F-cover-1920x1080.png")
    save(editorial(1200, 1200, 56, 28, 28, 28, 64, 1072), "variant-F-thumb-1200x1200.png")
    variant_g()
    print("Done — 8 PNG in round-2/")

if __name__ == "__main__":
    main()
