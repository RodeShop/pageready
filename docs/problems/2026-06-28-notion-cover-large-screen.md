# [TICKET] Notion cover stretch on large viewport — wrong aspect + low width

**Продукт:** `pillow_pin.py` → `make_notion_cover`  
**Slug:** `notion-developer-career-os` (стандарт для всех slug)  
**Приоритет:** high  
**Статус:** closed

---

## Симптом (Owner Gate 3)

- **Маленький экран:** cover норм  
- **Большой / wide monitor:** cover снова «увеличивается», растягивается

---

## Root cause

| Сейчас | Notion desktop |
|--------|----------------|
| **1920×540** (≈3.55:1) | **5:2** (2.5:1) — типично **1500×600**, лучше **3000×1200** |

540px fix убрал один вид stretch, но:
1. Aspect **не 5:2** → Notion перекадрирует/масштабирует на wide viewport  
2. Ширина **1920px** → на 2560px+ мониторе bitmap **upscale** → «раздувание»

Источники: Notion «images wider than 1500px work best»; рекомендация 5:2, high-res 3000×1200.

---

## Fix (Mechanic)

1. `make_notion_cover`: canvas **3000×1200** (5:2), Direction D layout масштабировать пропорционально  
2. **Safe zone:** title + 3 cards в центральных ~2400px; бока — plain `#eef1f5` (crop-safe)  
3. Regen + re-upload:
   ```bat
   python scripts/pillow_pin.py notion-developer-career-os
   python scripts/playwright_notion.py notion-developer-career-os
   ```
4. Обновить `skills/COVER_DIRECTIONS.md` → **3000×1200, 5:2**

---

## Не делать

- Не удалять Notion page  
- Не менять `playwright_notion.py` (upload OK)

---

## Verify

- [x] `notion-cover.png` = 3000×1200 (Lead verify 28.06)
- [x] `playwright_notion.py` exit 0 — uploaded
- [ ] Owner: OK wide monitor — **FAIL** round 3 center cluster needed
- [x] Live URL unchanged

---

## Reopen

Закрывает `2026-06-28-notion-cover-stretch.md` round 2.
