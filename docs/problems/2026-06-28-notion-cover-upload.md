# [TICKET] Notion cover upload — Change cover button not found

**Продукт:** playwright_notion.py
**Приоритет:** high
**Статус:** closed

---

## Lead verify round 5 (28.06) — ✅ PASS

```
[0] Clicked Change cover button (JS)
[0] Clicked Upload tab
[0] Cover uploaded via file chooser
[0] Notion cover uploaded.
```

Publish ✅ `...8110...c1c92f` · Chrome CDP ✅

---

## Lead verify round 4 (28.06)

| Step | Результат |
|---|---|
| Navigate + page_id assert | ✅ |
| JS click `Change` | ✅ `Clicked Change cover button (JS)` |
| Upload tab | ✅ |
| **File upload** | ❌ `[0] Upload failed` |
| Publish template URL | ✅ `...8110...c1c92f` |
| `draft/` before `ready/` | ✅ в main() |

**Следующий fix:** `input[type="file"]` не находится после Upload tab — возможно нужен клик «Upload file» / `filechooser` / CDP с логом ошибки.

---

## Root cause (Lead verify round 3)

1. **Stale `products/ready/` page_id** — `playwright_notion.py` читает `ready/` **раньше** `draft/`. В ready был дубль `...8133...` → publish/cover шли не туда. Lead синхронизировал ready → publish ✅ на `...8110...`.

2. **Cover click** — `get_by_text('Change')` **находит** элемент (`<span>Change</span>`), но click падает:
   ```
   element is not visible, enabled and stable → element was detached from the DOM
   ```
   Триггер: `screenshot()` перед hover (TimeoutError 8s, fonts loaded) — Notion перерисовывает cover strip.

**E2E после fix ready page_id:**
- Publish → ✅ правильный template URL
- Cover → ❌ `[0] Cover button not found`

---

## Root cause (Owner + Lead verify)

1. **Stale page_id** — `notion_result.json` указывал на удалённый дубль (`...8133...b1db...`). Актуальная страница:
   `https://app.notion.com/p/Developer-Career-OS-38c8515aba658110b2c1d4c145c1c92f`
   → `notion_page_id`: `38c8515a-ba65-8110-b2c1-d4c145c1c92f` ✅ исправлено Lead

2. **Неверный селектор** — на живой странице после hover кнопки **`Change`** и **`Reposition`**, не `Change cover` / `Add cover`. Lead verify на правильном URL: `Change visible: True`, `Change cover visible: False`.

## Воспроизведение (Lead E2E 28.06)

```bash
start_chrome_debug.bat
python scripts/playwright_notion.py notion-developer-career-os
```

```
[0] Cover file: .../notion-cover.png
[0] Cover button not found — skipping (pipeline continues)
```

Chrome CDP ✅ · Navigation ✅ · Share/Publish ✅ · Cover ❌

**Re-verify Mechanic (28.06, 2× E2E):** частично — код улучшен, cover ❌.

| Изменение в коде | Lead |
|---|---|
| `app.notion.com/p/...` navigate + assert page_id | ✅ в коде |
| `text=Change` / `button:has-text("Change")` | ✅ в коде |
| template_url guard (не save если id mismatch) | ✅ в коде |
| screenshot логирует exception | ✅ видно TimeoutError |
| **E2E cover upload** | ❌ `[0] Cover button not found` |
| **E2E publish** | ⚠️ stdout: старый дубль `...8133...` — `notion_result.json` на диске **не** перезаписан (guard?) |

**Изолированный тест** (новая вкладка, правильный URL): `text="Change"` visible ✅, клик ✅.  
**Гипотеза follow-up:** `quick_find_navigate` попадает на дубль по title; в full run `button:has-text("Change")` → false, `text="Change"` не срабатывает (tab/screenshot timeout).

---

## Причина (вероятно)

`upload_notion_cover()` hover at `y=180` — кнопки **Change cover / Reposition** появляются только при hover **на banner cover** (верх страницы, y≈40–120).

Owner UI (скрин): кнопки справа на cover strip, не в body.

---

## Fix

1. Читать `notion_page_id` из `notion_result.json` — **Owner обновляет после удаления дублей**
2. Navigate: `app.notion.com/p/...` (fallback `notion.so/{id}`)
3. После navigate — assert `page.url` содержит ожидаемый page id; иначе fail loud, не сохранять template_url
4. Hover cover strip y=40–90
5. Селекторы: **`text=Change`**, `text=Reposition`, `button:has-text("Change")` — не только `Change cover`
6. Не перезаписывать `notion_template_url` из `page.url` если id не совпадает с `notion_page_id`
7. Screenshot: логировать exception, не глотать
8. **Navigate:** prefer `notion_template_url` из json (если есть)
9. **Убрать** `quick_find_navigate` fallback когда задан `notion_page_id` — попадает на дубль
10. Cover click: **`page.get_by_text("Change", exact=True).first.click()`** первым (не `button:has-text`)
11. **Не делать screenshot до cover click** (или `animations: 'disabled'`, timeout 3s)
12. Click fallback: `evaluate(el => el.click())` или `.click(force=True, timeout=5000)`
13. **Mechanic:** `playwright_notion` — prefer `draft/` over `ready/` when оба exist (hotfix)

---

## Проверка

После fix — `[0] Notion cover uploaded.` + визуально custom banner на Developer Career OS.

---

## Решено (Mechanic, 28.06 round 3)

| # | Fix | Статус |
|---|---|---|
| 11 | Убран `screenshot(page, '0_cover_page')` до hover — был таймаут 8с, Notion перерисовывал strip | ✅ |
| 12 | JS-click первым (`el.click()` через evaluate) — обходит DOM-detach; Playwright click как fallback | ✅ |
| 13 | `main()` читает `draft/` раньше `ready/` | ✅ |

**Round 4 Mechanic:** `page.expect_file_chooser()` при клике "Upload file" → `fc.set_files(path)`. Fallback: hidden input, CDP.

**Round 5 Lead E2E:** ✅ **PASS** — полный cover upload pipeline.
