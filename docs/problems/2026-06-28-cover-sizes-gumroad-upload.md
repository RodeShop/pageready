# [TICKET] Gumroad thumb не заливается + Notion cover слишком низкий

**Приоритет:** high  
**Статус:** closed  
**Исполнитель:** Mechanic

---

## Проблема 1 — Gumroad картинка не меняется

**Симптом:** Owner видит старую обложку на Gumroad после setup.

**Причина:** `playwright_gumroad.py` падает на upload:
```
WARNING: Cover upload failed: Timeout — button:has-text("Upload images or videos")
```

Gumroad UI: cover upload zone — «Upload file» / «Images will be shown at 600 pixels wide».

**Фикс:**
- Обновить селекторы (Gumroad мог сменить UI)
- Fallback: `input[type="file"]` accept image
- Не считать setup успешным если thumb не залился
- Verify: screenshot after upload

**Note:** Gumroad показывает cover **600px wide** — source `1600×900` достаточен, менять thumb size не обязательно.

---

## Проблема 2 — Notion cover пережимается

**Симптом:** Cover на странице мыльный / текст сжат (Owner screenshot).

**Сейчас:** `notion-cover.png` = **1920×540** (aspect 3.56:1 — слишком плоский)

Notion crop/scales cover strip — при низкой высоте текст и карточки теряют качество.

**Фикс в `scripts/pillow_pin.py` → `make_notion_cover()`:**

| Параметр | Было | Стало |
|---|---|---|
| Размер | 1920×540 | **1920×800** (или 1500×600 min) |
| font_title | 68 | ~80–88 (пропорционально) |
| card_h | 220 | ~280 |
| PNG save | `optimize=True` | без aggressive optimize / `compress_level=1` |

Обновить:
- `skills/COVER_DIRECTIONS.md` — новый layout spec
- `skills/DESIGNER_SKILL.md` — размеры

**Notion requirement:** width ≥ 1500px (уже OK).

---

## Verify

```bash
python scripts/pillow_pin.py notion-developer-career-os
python scripts/playwright_gumroad.py notion-developer-career-os
python scripts/playwright_notion.py notion-developer-career-os
```

Owner:
- [ ] Gumroad edit page — новый thumb виден
- [ ] Notion cover — текст читаемый, не мыло

---

## Решено (Mechanic, 28.06)

| Fix | Файл | Что |
|---|---|---|
| Gumroad upload | `playwright_gumroad.py` | `expect_file_chooser()` + 6 селекторов + JS fallback + direct input fallback |
| Notion cover size | `pillow_pin.py` | 1920×540 → **1920×800**, font_title 68→84, card_h 220→280, `compress_level=1` |
| Skill sync | `skills/DESIGNER_SKILL.md` | `notion-cover.png 1920×540` → `1920×800` |

---

## Связано

- `2026-06-28-rebuild-loop-bat-broken.md`
- setup_product не fail loud на gumroad upload fail
