# [TICKET] Notion Publish — ложный успех, страница остаётся private

**Приоритет:** critical  
**Статус:** closed  
**Исполнитель:** Mechanic  
**Продукт:** все (playwright_notion.py)

---

## Проблема

`publish_as_template()` пишет в лог `Template URL saved`, но страница **не опубликована**.

**Симптом (Owner verify):** Share → General access = **"Only people invited"**. Нет public web / duplicate as template.

**Причина в коде:** fallback сохраняет `app.notion.com/p/...` — это **приватный workspace URL**, не публичный template link.

```python
# playwright_notion.py ~668-673 — ЛОЖНЫЙ УСПЕХ
if not template_url:
    template_url = current_url  # app.notion.com = private!
```

Скрипт не проверяет что после Publish:
- General access ≠ "Only people invited"
- Есть toggle "Allow duplicate as template" / site published
- URL работает в incognito

---

## Ожидаемое состояние после успеха

Share → вкладка **Publish** (не Share):
- Site published / Anyone with link
- Allow duplicate as template — ON
- URL: `notion.site/...` или public link, **не** `app.notion.com/p/...`

---

## Фикс

1. Убрать fallback `current_url` как success — если нет public URL → **fail**, не сохранять в json
2. После клика Publish — verify в DOM: "Published" / "Anyone on the web" / switch ON
3. Optional: incognito check что URL открывается без login
4. Screenshot on fail → debug_screenshots/

---

## Verify

```bash
python scripts/playwright_notion.py notion-developer-career-os
```

Owner открывает Share → Publish tab → не "Only people invited".

---

## Решено (Mechanic, 28.06)

| Fix | Что сделано |
|---|---|
| Убран fallback `current_url` | `app.notion.com/p/...` больше не сохраняется как template URL |
| "Allow duplicate as template" | Toggle включается автоматически после Publish |
| Fail loud | Нет `notion.site` URL → `ERROR` в лог + screenshot `publish_no_public_url.png` + `return None` |

---

## Связано

- `2026-06-28-setup-product-stale-ready.md` — stale ready/ json
- Developer Career OS — 3+ дубля страниц в workspace (мусор)
