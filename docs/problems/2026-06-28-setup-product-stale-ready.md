# [TICKET] setup_product читает stale template URL из ready/

**Приоритет:** medium  
**Статус:** closed  
**Исполнитель:** Mechanic

---

## Проблема

`get_template_url()` и `playwright_notion` при rebuild читают `products/ready/<slug>/gumroad_result.json` **раньше** draft — в JSON остаётся старый `notion_template_url`.

**Симптом:** Gumroad description ссылается на удалённую Notion-страницу после rebuild.

---

## Фикс

1. `setup_product.py` / `get_template_url()` — **всегда prefer draft/** over ready/
2. После `notion_create.py` — синхронизировать draft → ready/ или invalidate ready json
3. `ensure_images()` — вызывать **до** первого `playwright_notion.py` (cover upload fail если png ещё нет)

---

## Verify

Rebuild slug → gumroad_result.notion_template_url == notion_result.notion_template_url == новая страница.

---

## Решено (Lead verify 28.06)

| Fix | Файл |
|---|---|
| draft before ready | `setup_product.py` `get_template_url()` — `[draft, ready]` + `notion_result.json` первым |
| draft before ready | `playwright_notion.py` — product_dir и cover path draft first |
| ensure_images до Playwright | `setup_product.py` — уже было |
| draft → ready sync | `set_template_url.py` — копирует draft/ в ready/ после UPDATE |
