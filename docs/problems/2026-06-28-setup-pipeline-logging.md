# [TICKET] setup pipeline: логи + fail loud на каждом шаге

**Приоритет:** high  
**Статус:** closed  
**Исполнитель:** Mechanic

---

## Проблема

`setup_product.py` **не падает** когда Playwright молча фейлится:

| Шаг | Симптом | Сейчас |
|---|---|---|
| `upload_notion_cover` | Default gradient вместо Direction D | WARNING, exit 0 |
| `publish_as_template` | «Only people invited», нет `notion.site` | `return None`, exit 0 |
| `upload_thumbnail` (Gumroad) | Старый thumb на edit page | WARNING, exit 0 |
| `set_template_url` | Пишет stale `app.notion.com` из json | Продолжает |

MiMo/Lead видят «SETUP COMPLETE» — Owner видит ничего не изменилось.

---

## Фикс

### 1. `setup.log` — один файл на slug

`products/draft/<slug>/setup.log` — append каждого шага:

```
[2026-06-28 15:13:01] STEP notion_create START
[2026-06-28 15:08:31] STEP notion_create OK page_id=...
[2026-06-28 15:13:10] STEP pillow_pin OK
[2026-06-28 15:13:45] STEP notion_cover FAIL reason=navigation
[2026-06-28 15:14:02] STEP publish FAIL reason=no_notion_site
[2026-06-28 15:14:05] STEP gumroad_thumb FAIL reason=file_chooser
[2026-06-28 15:14:05] ABORT exit=1
```

Helper: `scripts/log_step.py` или функция в `setup_product.py`.

### 2. Fail loud

| Условие | Действие |
|---|---|
| `notion.site` не получен | `sys.exit(1)`, не писать template_url |
| cover upload fail | `sys.exit(1)` или `--continue` flag |
| gumroad thumb fail | `sys.exit(1)` |
| `playwright_*.py` | `sys.exit(1)` если critical step fail |

`setup_product.py`: после каждого `run()` — `if not ok: sys.exit(1)`.

### 3. `playwright_notion.py`

- `main()` → `sys.exit(1)` если `template_url is None`
- `upload_notion_cover` fail → exit 1 (или flag)
- В конце печатать **SUMMARY**: cover OK/FAIL, publish OK/FAIL, views N/M

### 4. `playwright_gumroad.py`

- `upload_thumbnail` fail → `sys.exit(1)`
- В конце: thumb OK/FAIL, guide OK/FAIL, published OK/FAIL

### 5. `playwright_gumroad.py` — wrong product

Stored `app.gumroad.com/.../edit` → Page not found → fallback `find_edit_url_from_products` вернул **первый** `/edit` link (`xhvifs`) — не Career OS.

**Fix:** искать по `gumroad_product_id` или permalink slug; **никогда** fallback «first /edit»; fail loud если slug mismatch.

---

## Verify

```bash
python scripts/setup_product.py notion-developer-career-os
# При fail — exit 1, setup.log с FAIL строкой
# При success — notion.site в json, cover на Notion, thumb на Gumroad
```

Owner checklist после success:
- [ ] Notion cover Direction D
- [ ] Share → Publish (not private)
- [ ] Gumroad thumb обновлён + Save

---

## Решено (Lead verify 28.06)

| Fix | Файл | Статус |
|---|---|---|
| setup.log | `setup_product.py` `log_step()` | ✅ |
| exit 1 notion fail | `setup_product.py` + `playwright_notion.py` | ✅ |
| exit 1 no notion.site | `playwright_notion.py` | ✅ |
| exit 1 gumroad thumb | `playwright_gumroad.py` | ✅ |
| no «first /edit» fallback | `playwright_gumroad.py` product_id URL | ✅ |
| SUMMARY blocks | оба playwright | ✅ |
| exit 1 cover fail | `playwright_notion.py` | ⚠️ FAIL только в SUMMARY |
| exit 1 guide/publish gumroad | `playwright_gumroad.py` | ⚠️ WARN, не abort |
