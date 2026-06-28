# [TICKET] gumroad_create — GET by permalink не работает

**Продукт:** factory-wide
**Приоритет:** high
**Статус:** closed

---

## Решено

**28.06 Mechanic + Lead verify**

- `find_product_by_permalink()` → `GET /products` + filter `custom_permalink` ✅
- POST conflict → list fallback ✅ (код)
- Lead API test: `notion-developer-career-os` → `PNbspS7ueNGa-I4sqb0xCw==` ✅
**Блокирует:** idempotency когда `gumroad_result.json` потерян

---

## Проблема (Lead verify 28.06)

`find_product_by_permalink()` вызывает `GET /v2/products/{permalink}`.

**Факт:** Gumroad возвращает `success: false` для permalink, хотя продукт существует:

```
GET /v2/products/notion-developer-career-os → "The product was not found"
GET /v2/products/PNbspS7ueNGa-I4sqb0xCw==  → success (работает)
POST /products → "Custom permalink has already been taken" + KeyError crash
```

---

## Fix

```python
def find_product_by_permalink(permalink):
    # 1. Try by id if we have saved id (optional)
    # 2. List all products — filter custom_permalink == permalink
    result = api_get('/products')
    if result.get('success'):
        for p in result.get('products', []):
            if p.get('custom_permalink') == permalink:
                return p
    return None
```

Также: если POST вернул "permalink already taken" — не падать с KeyError, вызвать list fallback.

---

## Проверка

Удалить draft+ready `gumroad_result.json` → run gumroad_create → "Found existing" без POST.

---

## Решено

_(Mechanic)_
