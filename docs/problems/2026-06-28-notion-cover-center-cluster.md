# [TICKET] Notion cover — center cluster (round 3)

**Продукт:** `pillow_pin.py` → `make_notion_cover`  
**Slug:** `notion-developer-career-os` (+ стандарт для всех)  
**Приоритет:** high  
**Статус:** closed

---

## Симптом (Owner Gate 3, 28.06)

3000×1200 загружен, но **Notion app + notion.site** на wide monitor:
- Title слева, «Projects / Jobs / Skills» **разъезжаются** по всей ширине баннера
- Выглядит растянутым (скрины Owner)

---

## Root cause (не размер файла)

Canvas 3000×1200 OK, но **layout** тянет контент на **2400px** (x=300…2700):
```
[Title+tagline @300] ........ huge gap ........ [3 cards @1330-2700]
```

Notion cover = `object-fit: cover` на **viewport width**. На широком экране видна **вся** ширина PNG → title и cards на противоположных краях = «растянуто».

3000×1200 fix не помог — проблема **композиция**, не DPI.

---

## Fix

1. Canvas **3000×1200** (5:2) — оставить  
2. **Весь** Direction D блок (title + tagline + divider + 3 cards) — **один cluster ~1400–1600px**, **центр canvas**:
   ```
   [=====#eef1f5=====[ Title | cards ]=====#eef1f5=====]
         x≈700–2300 только контент; бока — plain bg
   ```
3. Gumroad thumb уже compact — можно масштабировать ту же композицию  
4. Regen + upload:
   ```bat
   python scripts/pillow_pin.py notion-developer-career-os
   python scripts/playwright_notion.py notion-developer-career-os
   ```
5. `COVER_DIRECTIONS.md` — «center cluster, not edge-to-edge»

---

## Verify

- [x] PNG 3000×1200, cluster x=700–2300 (Lead: edges pure bg)
- [x] Playwright upload exit 0
- [ ] Owner: wide monitor — **FAIL** (cover giant + duplicate)
- [ ] Малый экран OK

---

## Reopens

`2026-06-28-notion-cover-large-screen.md` — closed преждевременно
