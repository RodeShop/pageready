# Executor Rules — Gumroad Factory

**Shared:** MiMo · Lead · все исполнители

---

## Read order

1. `docs/team/active/TASK.md` — задача
2. `docs/team/agents/EXECUTOR_RULES.md` — этот файл
3. `research/TRENDS.md` — тренды и очередь
4. `docs/team/common/STATUS.md` — текущий снимок

---

## Scope

- Продукты: `products/` только своя стадия (draft → ready)
- Листинги: `listings/`
- Документы: `docs/team/` только свои файлы
- Новый файл/папку — только по логике пайплайна

---

## Нейминг продуктов

`<тип>-<ниша>-<аудитория>` — всё в lowercase, дефисы

Примеры:
- `notion-freelance-tracker-designers`
- `notion-content-calendar-solopreneurs`
- `prompts-copywriting-ecommerce`

---

## Анти-дублирование

Перед генерацией нового продукта:
1. Проверь `products/ready/` и `products/published/` — такая ниша уже есть?
2. Проверь `docs/team/common/STATUS.md` § «Готово»
3. Если есть похожее — возьми другую нишу из `research/TRENDS.md`

---

## Структура продукта (Notion Template)

```
products/draft/<slug>/
├── template.md          # полная структура шаблона (базы, вьюхи, контент)
├── sample-data.md       # примеры данных для заполнения
├── user-guide.md        # инструкция для покупателя
└── notion-setup.md      # шаги настройки в Notion
```

## Структура продукта (Prompt Bundle)

```
products/draft/<slug>/
├── prompts.md           # 50+ промптов по нише
├── system-prompt.md     # system prompt для GPT/Claude
├── usage-guide.md       # как использовать
└── examples.md          # примеры результатов
```

---

## Листинг (обязательно для каждого продукта)

```
listings/<slug>.md
├── Title                # до 60 символов, нишевый
├── Subtitle             # что получает покупатель
├── Price                # $19 / $29 / $39
├── Description          # 200-300 слов, benefits-first
├── Tags                 # 10 тегов для поиска
└── Thumbnail concept    # описание обложки
```

---

## Verify перед ready/

Чеклист из `skills/NOTION_QUALITY.md` — все пункты зелёные.

---

## Project roots

| Key | Path |
|-----|------|
| `[PRODUCTS]` | `products/` |
| `[REPO_ROOT]` | `C:\Users\hramo\gumroad` |
| `[SKILLS]` | `skills/` |
| `[LISTINGS]` | `listings/` |

---

_Gumroad Factory · EXECUTOR_RULES · обновляет Lead_
