# [TICKET] Notion cover stretch — wrong aspect / old png

**Продукт:** `pillow_pin.py` + `playwright_notion.py`  
**Slug:** `notion-developer-career-os`  
**Приоритет:** high  
**Статус:** closed

---

## Симптом (Owner Gate 3)

Cover загружается, но на странице **растянут по горизонтали** — видны карточки Projects/Jobs/Skills, но картинка «плывёт», не как Direction D в файле.

Owner: «подгрузил, но старую».

---

## Гипотезы

1. **Aspect ratio:** `make_notion_cover` → 1920×800; Notion cover strip шире/ниже → пережимает при `object-fit: cover`.
2. **Старый png:** в `ready/` лежит старая `notion-cover.png`; скрипт берёт `draft/` первым — проверить оба.
3. **Не та страница:** в json `delicious-cucumber-254.notion.site`; если в UI другой subdomain (`callous-…`) — это **другая** (удалённая) копия, не текущий pilot.

---

## Не делать

- **Не удалять** текущую Notion page с `page_id` из `notion_result.json` — иначе снова `notion_create.py` → новая page + новый subdomain + дубликат.

---

## Fix

1. Подобрать размер cover под Notion (тест 1920×540 vs 1920×600 vs safe zone 1500px center).
2. `pillow_pin.py` → regen → только cover step:
   `python scripts/pillow_pin.py notion-developer-career-os`
   `python scripts/playwright_notion.py notion-developer-career-os` (или cover-only flag)
3. Owner verify: cover без stretch, subdomain = json.

---

## Verify

- [x] `notion-cover.png` в draft = 1920×540 (Lead regen 28.06)
- [x] `playwright_notion.py` exit 0 — cover uploaded (2-й прогон)
- [ ] Owner: cover **без stretch** на live site (Gate 3 visual)
- [x] `notion_template_url` = `delicious-cucumber-254.notion.site`
