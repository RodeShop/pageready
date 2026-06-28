# Gumroad edit URL — API id vs UI short slug

**Дата:** 2026-06-28  
**Статус:** fixed (workaround in playwright_gumroad.py)  
**Slug:** notion-developer-career-os

## Симптом

Playwright открывает `gumroad.com/products/4f4Im3eYDC2c7kPGQ_sahA==/edit` → **Page not found**.  
На `gumroad.com/products` продукт виден; edit в UI: `gumroad.com/products/pamwqu/edit`.

## Причина

API `gumroad_product_id` ≠ slug в URL edit-страницы.  
`find_edit_url_from_products()` при re-discover собирал URL из API id — всегда 404.

## Fix (round 1)

`playwright_gumroad.py`: искать edit-ссылку в списке products по имени/slug; сохранять `gumroad_edit_url` из UI.

## Follow-up для Mechanic

- `gumroad_create.py`: после create/list — сохранять UI edit slug если API отдаёт
- При 404 на edit — never construct URL from product_id alone
