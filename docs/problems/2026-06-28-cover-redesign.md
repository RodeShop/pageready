# [TICKET] Cover redesign D + Notion cover via Playwright

**Продукт:** factory-wide
**Приоритет:** high
**Статус:** closed
**Выбор Owner:** Direction D — System Cards, **без emoji**

---

## 1. pillow_pin.py — Direction D

Переписать `make_pin()` и `make_thumb()` под `skills/COVER_DIRECTIONS.md`:

- Фон: solid `#eef1f5` (не gradient)
- 3 white cards с названиями баз (первые 3 из `spec.databases`)
- Title + tagline из spec
- **Убрать:** emoji, initial-in-circle, gradient hero, accent bar editorial
- Добавить **`make_notion_cover()`** → `notion-cover.png` **1920×540**

### notion-cover.png

- Wide banner для Notion page cover
- Title слева, 3 compact cards справа
- Same color tokens as thumb
- Save to `products/draft/<slug>/notion-cover.png` (and ready/)

---

## 2. playwright_notion.py — upload cover

**До** или **после** `publish_as_template`, на root page:

```
1. navigate_to_notion_page (root page_id)
2. Hover cover area → click "Change cover" (или "Add cover")
3. Tab "Upload" (не Gallery)
4. set_input_files на notion-cover.png
5. Wait for upload · Escape to close
6. screenshot notion_cover_uploaded
```

Selectors (из UI Owner):
- `text="Change cover"` / `text="Add cover"`
- Tab: `Upload`
- Button: `Upload file` → underlying `input[type="file"]`

Fallback: CDP `DOM.setFileInputFiles` как в playwright_gumroad.py

**Путь к файлу:** ищи `notion-cover.png` в draft/ и ready/

Если файла нет → skip с warning (не блокировать pipeline)

### Порядок в main()

```
[0] upload_notion_cover(page, context, page_id, slug)   ← NEW
[1] publish_as_template(...)
[2] setup_database_views(...)
[3] save template URL
```

---

## 3. setup_product.py

Без изменений если pillow_pin вызывается в Designer Mode до setup.
В `ensure_images()` добавить fallback: если нет notion-cover → pillow_pin.

---

## 4. notion_create.py (опционально)

Убрать generic gradient `COVER_URLS` из API create — cover будет через Playwright.
Или оставить placeholder; Playwright перезапишет.

---

## Проверка

```bash
python scripts/pillow_pin.py notion-developer-career-os
# → gumroad-thumb.png, pinterest-pin.png, notion-cover.png

python scripts/playwright_notion.py notion-developer-career-os
# → Notion root page shows custom cover (not empty "Add cover")
```

Visual: no emoji on any of 3 outputs.

---

## Решено

**28.06 Lead verify (final)**

- `pillow_pin.py` — Direction D, 3 файла, без emoji — ✅
- `playwright_notion.py` — `upload_notion_cover()` E2E — ✅ (file chooser)
- `setup_product.py` — ensure_images включает notion-cover — ✅
