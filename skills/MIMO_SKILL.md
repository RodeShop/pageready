# MIMO_SKILL — Инструкции для МиМо

Читай этот файл **перед каждой сессией** после EXECUTOR_RULES.

---

## 1. Ведение доски (board.html) — обязательно

Доска — главный дашборд Owner. Обновляй её при каждом изменении статуса.

### Что обновлять

**STATS** (вверху доски) — после каждого готового продукта:
```js
const STATS = [
  { val: '5',    lbl: 'Продуктов готово' },   // ← количество в products/ready/
  { val: '3',    lbl: 'Опубликовано' },         // ← количество в products/published/
  { val: '$47',  lbl: 'Доход' },                // ← из STATUS.md если есть данные
  { val: '7',    lbl: 'Ниш в очереди' },        // ← оставшиеся в TRENDS.md
];
```

**TASKS** — меняй статус задачи когда берёшь в работу или завершаешь:
```js
// Статусы: 'done' | 'in_progress' | 'backlog' | 'blocked'
{ id: 'TASK-003', status: 'in_progress', ... }  // взял в работу
{ id: 'TASK-003', status: 'done', ... }          // завершил
```

**Subtasks** — отмечай done: true по мере выполнения:
```js
{ id: 's3-1', title: 'Читает spec.json', done: true }
```

**NOTES** — добавляй заметку если:
- Столкнулся с трудностью
- Принял нестандартное решение
- Нишу пришлось пропустить (и почему)
- Продукт получил оценку C (и что не так)

```js
const NOTES = [
  ...существующие,
  {
    id: 'n3', date: '27 июн 2026',
    text: 'Ниша "Remote Team Wiki" пропущена — слишком широкая аудитория. Взял "Freelance Client Tracker".',
  },
];
```

### Где редактировать

Файл: `board.html` — секция `<script>` в самом начале (константы STATS, PHASES, TASKS, NOTES).

### Когда обновлять

| Событие | Что обновить |
|---------|-------------|
| Взял нишу в работу | TASK статус → in_progress |
| Готов draft продукт | TASK subtasks |
| Продукт в ready/ | TASK статус → done, STATS обновить |
| Есть трудность | NOTES добавить |
| Пропустил нишу | NOTES объяснить |
| После 5 продуктов | STATS полностью обновить |

---

## 2. Проектирование Notion шаблона

### Хорошая ниша vs плохая

| Плохо | Хорошо |
|-------|--------|
| Project Tracker | Freelance Client & Invoice Tracker for Designers |
| Study Notes | Second Brain for Computer Science Students |
| Budget | Monthly Budget & Savings Tracker for Solopreneurs |

Правило: **кто + что + зачем** в названии.

### Обязательные базы данных

Минимум 2 базы, связанные через Relation:

```
Clients (база 1)
  └── Projects (база 2) — relation к Clients
       └── Tasks (база 3, опционально) — relation к Projects
```

### Свойства по типам

```
title       — главное имя (всегда первое)
select      — статус, приоритет, категория (3-5 вариантов с цветами)
multi_select — теги, навыки, платформы
date        — дедлайн, дата старта
number      — деньги ($), часы, оценка (1-10)
email       — контакты
url         — ссылки
checkbox    — выполнено да/нет
relation    — связь с другой базой
formula     — вычисляемые поля (осторожно, не перегружай)
```

### Sample data — реалистичный, не generic

```
# Плохо:
{"Name": "Client 1", "Status": "Active", "Revenue": 0}

# Хорошо:
{"Name": "Acme Design Studio", "Status": "Active", "Revenue": 3500,
 "Email": "sarah@acmedesign.com", "Projects": ["Brand Refresh", "Website"]}
```

Минимум 5 строк в главной базе, 3-4 в связанных.

### Welcome-страница (обязательно)

```
# 🎉 Welcome to [Template Name]!

## What this template does
[2-3 предложения]

## Quick Start (3 steps)
1. Duplicate this template to your workspace
2. Delete sample data (or keep as reference)
3. Start with the [Main Database] view

## Database Overview
- **[База 1]** — [для чего]
- **[База 2]** — [для чего]

## Pro Tips
- [Совет 1]
- [Совет 2]

## Adding Views (Board, Calendar, Gallery)
Notion API doesn't support views — add them manually:
1. Open [Main Database]
2. Click + next to view tabs
3. Choose Board → Group by Status
```

---

## 3. Gumroad листинг — формула

### Структура описания (200-300 слов)

```
**Tired of [КОНКРЕТНАЯ БОЛЬ]?**

[2 предложения про проблему]

**Introducing [НАЗВАНИЕ] — [короткое описание решения]**

[2 предложения про ценность]

**What's inside:**
✅ [База 1] with [кол-во] pre-built properties
✅ [База 2] linked to [База 1]
✅ [Конкретная фича] — [что даёт]
✅ [Конкретная фича]
✅ Step-by-step Welcome guide

**Perfect for:**
→ [Аудитория 1 — конкретно]
→ [Аудитория 2]
→ [Ситуация использования]

**Works with:** Notion Free & Paid plans
**Instant download. One-time payment.**
```

### Цена

- 1 база, простой шаблон → **$19**
- 2-3 базы, средняя сложность → **$29**
- 3+ базы, формулы, сложная логика → **$39**

### Теги (10 штук)

```
notion template, [ниша], [аудитория], productivity, digital download,
notion dashboard, [конкретная задача], workflow, [год 2026], notion planner
```

---

## 4. Pinterest пин

```markdown
# pinterest-pin.md

## Title (до 100 символов)
[Нишевое название] Notion Template for [Аудитория]

## Description (до 500 символов)
Stop [БОЛЬ]. This [название] Notion template helps [аудитория]
[что делает]. Includes [главная фича], [фича 2], and [фича 3].
Download instantly on Gumroad. #notion #[ниша] #productivity #digitaldownload

## Hashtags
#notion #notiontemplate #[ниша] #productivity #digitaldownload #[аудитория]

## Image concept
Background: [цвет hex]
Text overlay: "[название шаблона]"
Subtitle: "Notion Template for [аудитория]"
Style: clean, minimal, professional
Size: 1000x1500px
```

---

## 5. SEO blog post

```markdown
# blog-post.md

## SEO Title (50-60 символов)
[Keyword]: Best Notion Template for [аудитория] in 2026

## Meta Description (150-160 символов)
[Benefit-driven description с keyword]

## Article structure
H1: [SEO Title]
Intro: [боль аудитории — 2 абзаца]
H2: Why [аудитория] Need a Notion System
H2: Introducing [Template Name]
H2: What's Inside [Template Name]
  - [База 1]: [описание]
  - [База 2]: [описание]
H2: How to Get Started
H2: FAQ (2-3 вопроса)
CTA: "Get [Template Name] on Gumroad →"
```

---

## 6. Трендовый ресёрч — каждые 10 продуктов

### Когда запускать

- После каждых **10 готовых продуктов** (или когда в очереди TRENDS.md < 3 ниш)
- Announce: `=== ARCHITECT MODE — TREND RESEARCH ===`

### Источники для анализа (в порядке приоритета)

**1. Gumroad Discover**
```
Открой: https://gumroad.com/discover?query=notion+template&sort=popular
Ищи: шаблоны с 100+ продажами, читай названия и аудиторию
Вопрос: какие ниши продаются, но у нас ещё нет?
```

**2. Pinterest Trends**
```
Открой: https://trends.pinterest.com
Ищи: "notion template", "notion planner", "notion dashboard"
Смотри: что растёт по impressions последние 30 дней
```

**3. Reddit — боли аудитории**
```
r/Notion — sort by Hot — ищи посты "how do you track X"
r/productivity — ищи "I need a system for X"
r/freelance — ищи жалобы на организацию работы
```

**4. Etsy — конкурентный анализ**
```
Открой: https://www.etsy.com/search?q=notion+template
Фильтр: Top customer reviews
Смотри: что продаётся 500+ раз — значит спрос есть
```

### Формула оценки ниши

| Критерий | Хорошо | Плохо |
|----------|--------|-------|
| Аудитория | Конкретная (UX designers) | Широкая (people) |
| Боль | "Теряю клиентов" | "Хочу быть продуктивнее" |
| Конкуренция | < 10 похожих на Gumroad | > 50 похожих |
| Цена рынка | $15-40 | < $5 (слишком дёшево) |
| Трендовость | Растёт в Pinterest | Плоская линия |

### Что добавить в TRENDS.md

После ресёрча добавь 5-7 новых ниш:

```markdown
## Приоритет A — [дата ресёрча]

| Ниша | Аудитория | Тип | Цена | Источник |
|------|-----------|-----|------|----------|
| [название] | [кто] | Notion | $29 | Gumroad popular |
```

Также добавь в NOTES доски:
```js
{ id: 'nN', date: '[дата]',
  text: 'Трендовый ресёрч: найдено 6 новых ниш. Топ: [ниша 1], [ниша 2]. Источник: Gumroad + Pinterest.' }
```

---

## 7. Autocompact — каждые 5 продуктов

После каждых 5 готовых продуктов:

1. Обнови `docs/team/common/STATUS.md` полностью — что сделано, что в очереди
2. Обнови STATS в `board.html`
3. Запусти `/compact` для сжатия контекста
4. После компакта первым делом читай: STATUS.md → TRENDS.md → board.html NOTES

---

## 7. Самооценка A/B/C

**A** — публикуем сразу:
- Все обязательные поля в spec.json заполнены
- 2+ базы данных
- 5+ sample rows в главной базе
- Welcome страница есть
- Листинг 200+ слов, benefits-first
- Нишевое название с аудиторией

**B** — публикуем, но фиксируем недочёт в NOTES:
- 1-2 незначительных пункта не выполнены
- Например: меньше sample data или листинг 150 слов

**C** — дорабатываем (макс 2 попытки), потом пропускаем нишу:
- Нет связи между базами
- Generic название без аудитории
- Листинг меньше 100 слов
- Sample data "Example 1", "Task A"

При C: пишем в NOTES причину → берём следующую нишу из TRENDS.md.
