# [TICKET] Developer Career OS — hotfix live продукта

**Продукт:** notion-developer-career-os
**Приоритет:** high (критично — уже на Gumroad)
**Статус:** open
**Исполнитель:** MiMo (+ Mechanic если rollup баг в скрипте)

## Проблемы (Owner review 28.06)

| Приоритет | Проблема |
|---|---|
| 🔴 | Skill Count = 0 в Projects — rollup не считает |
| 🔴 | Нет обложки на главной странице Notion |
| 🟡 | 4 базы вместо 6 — нет **Jobs** (критично для названия) |
| 🟡 | Skills → Projects пустые — двусторонняя связь не заполнена |
| 🟢 | Snippets отсутствует — добавить или честно «5 баз» в листинге |

## Корневая причина (Lead verify)

В `spec.json` sample_rows **не содержат relation-поля** (`Skills` на Projects, `Projects` на Skills). `link_sample_rows()` в `notion_create.py` работает — данные просто не переданы.

Rollup Skill Count настроен верно, но без связей count = 0.

`cover_color: blue` в spec есть — обложка не применилась на live странице (нужен re-create или patch API).

## Что сделать

### MiMo — spec.json + контент

1. **Relations в sample_rows** — каждый Project → 2-4 Skills по имени; Skills → Projects зеркально
2. **База Jobs** — Companies, Position, Status (Applied/Interview/Offer/Rejected), Salary, Applied Date, Notes; relation к Skills
3. **Snippets** (желательно) — Name, Language, Code, Tags, Project relation — или убрать из маркетинга
4. **cover_color** — проверить; после recreate должна появиться gradient cover
5. Обновить listing, user-guide, quality-report (честно: 6 баз, relations заполнены)
6. Пересоздать Notion: удалить старую страницу → `python scripts/notion_create.py notion-developer-career-os` → Playwright template publish
7. Обновить Gumroad listing если описание меняется

### Mechanic — только если после п.1 rollup всё ещё 0

Проверить `add_rollups()` — rollup_property `Name` + function `count` на relation `Skills`.

## Проверка

- [ ] Skill Count > 0 минимум у 4 Projects
- [ ] Skills.Projects заполнена у всех 6 Skills
- [ ] Jobs база с 6+ sample rows
- [ ] Cover на root page Notion
- [ ] Gumroad listing соответствует факту (6 баз)

## Решено

_(заполняет исполнитель)_
