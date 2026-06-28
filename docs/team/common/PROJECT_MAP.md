# PROJECT_MAP — Gumroad Factory
_Статичная карта проекта. Меняется редко. Живые данные — в STATUS.md._

---

## Корень

**Репо:** `C:\Users\hramo\gumroad`  
**Платформа:** Gumroad (rodeshop.gumroad.com)  
**Chrome debug port:** 9222 (ярлык RodeShop Factory на рабочем столе)

---

## Структура папок

```
gumroad/
├── .cursor/rules/
│   ├── mimo.mdc          MiMo — генератор продуктов
│   ├── lead.mdc          Lead — документация и очередь
│   ├── mechanic.mdc      Mechanic — тикеты и QA
│   └── owner.mdc         Owner — запускает скрипты
│
├── .mimocode/
│   └── MIMO_FACTORY.md   Главные правила MiMo (читает первым)
│
├── docs/team/
│   ├── common/
│   │   ├── STATUS.md       ← ЖИВОЙ статус фабрики (обновлять постоянно)
│   │   ├── PROJECT_MAP.md  ← этот файл (структура, меняется редко)
│   │   └── PROD_FACTS.md   ← ценообразование, рыночные данные
│   ├── active/
│   │   └── TASK.md         ← текущая задача для MiMo (Lead пишет, MiMo читает)
│   ├── agents/
│   │   ├── EXECUTOR_RULES.md
│   │   └── handoff/        ← шаблоны для запуска агентов
│   └── architect/
│       ├── LEAD.md
│       └── ROADMAP.md
│
├── docs/problems/          ← тикеты для Mechanic (Lead создаёт)
│
├── products/
│   ├── queue/              ← ниши в очереди (Lead создаёт <slug>.md)
│   ├── draft/<slug>/       ← MiMo пишет сюда
│   │   ├── spec.json
│   │   ├── listing.md
│   │   ├── user-guide.md
│   │   ├── blog-post.md
│   │   ├── notion_result.json   (создаётся setup_product.py)
│   │   └── gumroad_result.json  (создаётся setup_product.py)
│   └── ready/<slug>/       ← финальная версия (может содержать те же файлы)
│       ├── spec.json
│       ├── gumroad-thumb.png
│       └── pinterest-pin.png
│
├── research/
│   └── TRENDS.md           ← тренды, ниши, оценки (Lead обновляет)
│
├── scripts/                ← все скрипты автоматизации
│   ├── setup_product.py    ← ГЛАВНЫЙ: запускает полный цикл для одного продукта
│   ├── notion_create.py    ← Notion API: страница + DB + relations + sample rows
│   ├── playwright_notion.py← Playwright: Share + views (Board/Calendar)
│   ├── gumroad_create.py   ← Gumroad API: создаёт продукт
│   ├── playwright_gumroad.py← Playwright: thumbnail + publish
│   ├── set_template_url.py ← обновляет Notion template URL в листинге
│   └── promote.py          ← blog post + Pinterest
│
├── skills/
│   ├── MIMO_SKILL.md       ← как проектировать Notion шаблоны
│   ├── NOTION_BLOCKS.md    ← примеры spec.json для premium шаблонов
│   └── NOTION_QUALITY.md   ← чеклист самооценки A/B/C
│
└── board.html              ← визуальный дашборд (Lead обновляет при важных изменениях)
```

---

## Агенты и зоны ответственности

| Агент | Запускается | Что делает | Не делает |
|---|---|---|---|
| **MiMo** | `/execute` с ролью | Генерирует spec.json, listing.md, user-guide.md, blog-post.md | Не запускает скрипты напрямую |
| **Lead** | Этот чат | Обновляет STATUS.md, TASK.md, TRENDS.md, ставит задачи MiMo | Не генерирует продукты |
| **Mechanic** | При баге | Создаёт тикеты в `docs/problems/`, чинит скрипты | — |
| **Owner** | Каждый продукт | Открывает Chrome → `python scripts/setup_product.py <slug>` | Ничего вручную — всё автоматика |

---

## Пайплайн одной строкой

```
MiMo генерирует → Lead проверяет → Owner: Chrome + setup_product.py → всё автоматически
```

---

## Ключевые правила

1. **STATUS.md — единственный источник правды** о текущем состоянии
2. **Никаких ручных шагов в Notion или Gumroad** — всё через Playwright
3. **spec.json** всегда в `draft/<slug>/` — скрипты читают оттуда (также проверяют `ready/`)
4. **notion_result.json + gumroad_result.json** — если удалить, setup_product.py пересоздаёт
5. **Premium-стандарт обязателен** — 3+ DB, formula, rollup, связанный sample data
