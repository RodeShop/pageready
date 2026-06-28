# [TICKET] Gumroad duplicate products — idempotency

**Продукт:** factory-wide
**Приоритет:** **critical**
**Статус:** closed

---

## Проблема

`gumroad_create.py:122` — `api_post('/products', data)` **без проверки** существующего permalink.

Каждый вызов создаёт **новый** листинг на Gumroad. Покупатели видят дубли в магazine.

### Цепочка

```
publish.py → gumroad_create.py → POST /products  (всегда CREATE)
setup_product.py:79-88 — skip только если gumroad_result.json + notion_result.json оба есть
```

Если `gumroad_result.json` потерян / не записан / draft пересоздан → **ещё один продукт**.

---

## Owner — СЕЙЧАС (руками)

1. Открыть https://gumroad.com/products
2. Для каждого slug — **оставить один** листинг, остальные **Delete**
3. Оставить тот, чей URL совпадает с `gumroad_result.json` в draft/ready (если есть)
4. **До фикса:** не запускать `setup_product.py` / фабрику на slug где gumroad_result.json отсутствует

---

## Fix — gumroad_create.py

### 1. Локальный check (первым)

```python
for base in [f'products/draft/{slug}', f'products/ready/{slug}']:
    path = f'{base}/gumroad_result.json'
    if exists: load product_id → return existing, skip POST
```

### 2. API check по permalink (до POST)

Gumroad v2: **`GET /v2/products/:id`** принимает **custom permalink**.

```python
def find_product_by_permalink(permalink):
    r = requests.get(f'{BASE_URL}/products/{permalink}',
                     params={'access_token': GUMROAD_TOKEN})
    result = r.json()
    if result.get('success') and result.get('product'):
        return result['product']
    return None
```

В `create_product()`:
```python
existing = find_product_by_permalink(permalink)
if existing:
    print(f'  Found existing: {existing["id"]} — skip create')
    return existing
# else POST /products
```

### 3. Всегда писать gumroad_result.json

Даже при reuse — обновить файл с актуальным `gumroad_product_id`, `short_url`, `published`.

### 4. api_get helper

Добавить `api_get(path, params)` рядом с `api_post` / `api_put`.

---

## Дополнительно (желательно)

### setup_product.py

Если `gumroad_result.json` нет, но Notion есть — вызывать gumroad_create (который теперь idempotent), не полный publish с notion recreate.

### publish.py

Перед `gumroad_create.py` — skip если gumroad_result.json valid? (опционально, если fix в gumroad_create достаточно)

---

## Проверка

```bash
# Два раза подряд — один product_id
python scripts/gumroad_create.py notion-developer-career-os
python scripts/gumroad_create.py notion-developer-career-os
# → второй раз: "Found existing, skip create"
```

Удалить `gumroad_result.json` локально, запустить снова — GET by permalink, не POST.

---

## Решено

**28.06 Lead verify**

- `api_get`, local `gumroad_result.json` reuse — ✅ 2× run один ID
- ⚠️ `GET /products/{permalink}` на Gumroad **не находит** продукт (API quirk) → follow-up `2026-06-28-gumroad-permalink-lookup.md`
- Статус: **partial** — safe если json на месте
