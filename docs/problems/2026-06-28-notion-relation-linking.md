# [TICKET] notion_create: relations не линкуются если title ≠ Name

**Продукт:** все OS с rollups  
**Приоритет:** high  
**Статус:** closed  
**Исполнитель:** Mechanic

---

## Проблема

`link_sample_rows()` и `add_sample_rows()` используют только `row.get('Name')` как ключ строки.

Базы с title-полем **Company**, **Title** и т.д. — page_ids не сохраняются, relations в sample_rows **никогда не линкуются**.

**Симптомы (Developer Career OS):**
- Skill Count rollup = 0 (Projects.Skills пустой)
- Skills.Projects пустой
- Learning.Skill, Jobs.Contact, Achievements.Project — не линкуются

---

## Фикс (`scripts/notion_create.py`)

```python
def title_property_name(prop_specs):
    for p in prop_specs:
        if p['type'] == 'title':
            return p['name']
    return 'Name'

def row_key(row, prop_specs):
    return row.get(title_property_name(prop_specs), row.get('Name', ''))
```

Использовать `row_key()` в `add_sample_rows` и `link_sample_rows`.

---

## Verify

После фикса + spec с relations в sample_rows:
- Projects.Skill Count > 0
- Skills.Projects заполнен
- `python scripts/notion_create.py notion-developer-career-os` → в логе `Linked N rows via relations`, N > 0

---

## Решено (Lead verify 28.06)

- `title_property_name()` + `row_key()` в `notion_create.py`
- `add_sample_rows()` и `link_sample_rows()` используют `row_key()` — title ≠ Name (Position, Title, Objective…) линкуется
