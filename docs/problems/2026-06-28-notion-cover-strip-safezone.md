# [TICKET] Notion cover — strip safe zone (round 4)

**Продукт:** `pillow_pin.py` → `make_notion_cover`  
**Slug:** `notion-developer-career-os` (+ все slug)  
**Приоритет:** high  
**Статус:** closed

---

## Симптом (Owner Gate 3)

PNG на диске **OK** (center cluster). В **Notion app + notion.site** cover:
- Title + 3 cards **огромные**, обрезаны
- Дублируют title/список баз **ниже** cover
- На wide monitor — ещё хуже (скрины Owner 28.06)

Center cluster (round 3) **не помог** — проблема не ширина canvas.

---

## Root cause

**Notion cover ≠ Gumroad thumb.**

Cover strip на экране ≈ **250–320px высотой**, `object-fit: cover` по **ширине viewport**:
- На 1920px+ масштабирует 3000×1200 PNG **вверх**
- Видимая зона ≈ **центральная полоса ~350px** по Y
- Наш cluster (88px title + 250px cards) **заполняет всю полосу** → выглядит как гигантский баннер

Direction D **полный** (title + 3 cards) работает на Gumroad/Pinterest, **не** на Notion cover.

---

## Fix — отдельный layout `make_notion_cover`

Canvas **3000×1200** (5:2) оставить. Контент **только strip safe zone**:

```
y = 480..720  (240px band, center of 1200)
x = 900..2100 (1200px band, center of 3000)
```

**Содержимое (без карточек):**
- Title **48px** max, 1–2 строки, centered
- Tagline **22px**, centered, muted
- Accent line или «RodeShop» **18px**
- **NO 3 cards** — на странице уже есть emoji + список баз

Бока/верх/низ — plain `#eef1f5`.

Gumroad thumb / pin — **не менять** (полный Direction D).

---

## Regen + upload

```bat
python scripts/pillow_pin.py notion-developer-career-os
python scripts/playwright_notion.py notion-developer-career-os
```

Обновить `COVER_DIRECTIONS.md` — секция «Notion cover = strip only».

---

## Verify

- [x] PNG 3000×1200, strip y=480–720, **no cards**
- [x] Playwright upload exit 0
- [x] Gumroad thumb 1600×900 unchanged (full Direction D)
- [x] Owner: strip cover принят (28.06)

---

## Reopens

`notion-cover-center-cluster.md` — closed преждевременно
