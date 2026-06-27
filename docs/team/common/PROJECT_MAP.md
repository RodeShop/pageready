# PROJECT_MAP — Gumroad Factory

**Тип:** Автономная фабрика цифровых продуктов (Notion Templates + AI Prompt Bundles)
**Платформа:** Gumroad
**Репо:** `C:\Users\hramo\gumroad`

---

## Структура

```
gumroad/
├── .cursor/rules/          Роли агентов (mimo, lead, mechanic, owner)
├── .mimocode/
│   └── MIMO_FACTORY.md     Главные правила MiMo
├── docs/
│   ├── team/
│   │   ├── active/
│   │   │   └── TASK.md     Активная задача для MiMo
│   │   ├── agents/
│   │   │   ├── handoff/    Копипасты для запуска агентов
│   │   │   └── EXECUTOR_RULES.md
│   │   ├── common/
│   │   │   ├── PROJECT_MAP.md  (этот файл)
│   │   │   ├── STATUS.md       Текущее состояние фабрики
│   │   │   └── PROD_FACTS.md   Факты о продуктах и продажах
│   │   └── architect/
│   │       ├── LEAD.md         Правила Lead агента
│   │       └── ROADMAP.md      Дорожная карта
│   └── problems/           Тикеты для Mechanic
├── products/
│   ├── queue/              Ниши в очереди на генерацию
│   ├── draft/              Продукты в процессе
│   ├── ready/              Готово к загрузке на Gumroad
│   └── published/          Уже опубликовано
├── research/
│   └── TRENDS.md           Тренды, ниши, оценки спроса
├── listings/               Описания для Gumroad листингов
└── skills/
    └── NOTION_QUALITY.md   Чеклист качества продукта
```

---

## Пайплайн

```
TRENDS.md → queue/ → draft/ → [quality check] → ready/ → Gumroad → published/
```

## Агенты

| Агент | Роль | Файл |
|-------|------|------|
| MiMo | Генерирует продукты автономно | `.mimocode/MIMO_FACTORY.md` |
| Lead | Исследует тренды, ведёт очередь | `docs/team/architect/LEAD.md` |
| Mechanic | Проверяет качество по тикетам | `docs/problems/` |
| Owner | Загружает на Gumroad | — |
