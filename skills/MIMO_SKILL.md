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

### Название — формула

```
[Прилагательное] [Аудитория] [Конкретный инструмент] — [Результат]
```

| Плохо | Хорошо |
|-------|--------|
| Project Tracker | Freelance Client & Invoice Tracker for Designers |
| Study Notes | Second Brain for Computer Science Students |
| Budget | Monthly Budget & Savings Tracker for Solopreneurs |
| Productivity Dashboard | Content Creator Publishing OS |

Правило: название отвечает на вопрос **кто + что + зачем**.

---

### Структура шаблона — обязательный минимум (все продукты $19+)

**МЫ НЕ ДЕЛАЕМ одиночные трекеры. Каждый продукт — это OS (operating system) для конкретного человека.**
Продукт называется "[Аудитория] OS" / "[Аудитория] Hub" / "[Аудитория] System". Никогда просто "Tracker" или "Dashboard".

**Минимум 5 баз данных**, связанных через Relations (цепочка):

```
[Главная база]
  ├── [База 2] — relation к Главной
  │     └── [База 3] — relation к Базе 2
  ├── [База 4] — relation к Главной
  └── [База 5] — standalone или relation к любой
```

Rollup-цепочка обязательна: данные из База 3 → поднимаются в База 2 → поднимаются в Главную.

**Обязательные формулы** (минимум 2 — одна в главной базе, одна в дочерней):
```
Overdue:       if(prop("Deadline") < now() and not prop("Complete"), true, false)
Days Until:    dateBetween(prop("Deadline"), now(), "days")
Progress %:    if(prop("Total") > 0, round(prop("Done") / prop("Total") * 100), 0)
Balance:       prop("Income") - prop("Expenses")
Revenue/hr:    if(prop("Hours") > 0, prop("Budget") / prop("Hours"), 0)
```

**Обязательные rollup** (минимум 2, цепочка):
```
Total Revenue:  relation=Projects, property=Budget, function=sum  (на Clients)
Task Count:     relation=Tasks,    property=Name,   function=count (на Projects)
Done Count:     relation=Tasks,    property=Done,   function=count_values (на Projects)
```

### Структура шаблона — стандарт (все новые продукты)

- **5–6 баз данных** с rollup-цепочками (Tasks → Projects → Clients)
- Rollup chains 2 уровня: часы из Tasks → Projects → Clients
- **2+ формулы** — минимум в главной и в одной дочерней базе
- Welcome-страница с инструкцией по старту (обязательно, 10+ блоков)
- **Минимум 10 строк** sample data в главной базе, 5+ в каждой дочерней
- Реалистичные данные: настоящие имена компаний, реальные суммы, даты текущего года
- user-guide.md **минимум 1200 слов** с пошаговыми примерами и скриншот-описаниями

---

### Свойства по типам (spec.json)

```
title            — главное имя (всегда первое)
select           — статус, приоритет, категория (3-5 вариантов с цветами)
multi_select     — теги, навыки, платформы
date             — дедлайн, дата старта
number           — деньги ($), часы, оценка
email            — email контакт
url              — ссылка
checkbox         — выполнено да/нет
relation         — связь с другой базой (related_db: "Название базы")
formula          — вычисляемое поле (expression: "формула Notion")
rollup           — агрегация из связанной базы (relation_property, rollup_property, function)
```

**Пример формулы в spec.json:**
```json
{"name": "Overdue", "type": "formula",
 "expression": "if(prop(\"Deadline\") < now() and not prop(\"Complete\"), true, false)"}
```

**Пример rollup в spec.json:**
```json
{"name": "Total Project Budget", "type": "rollup",
 "relation_property": "Projects", "rollup_property": "Budget", "function": "sum"}
```

---

### Sample data — реалистичный, не generic

**Плохо:**
```json
{"Name": "Client 1", "Status": "Active", "Revenue": 0}
```

**Хорошо:**
```json
{"Name": "Acme Design Studio", "Status": "Active", "Monthly Revenue": 3500,
 "Email": "sarah@acmedesign.com", "Notes": "Long-term retainer. Logo + brand identity work."}
```

Правила:
- **Минимум 10 строк** в главной базе, 5+ в каждой дочерней
- Реальные имена компаний (не "Acme Corp"), реальные суммы, даты текущего года
- Показывай все статусы: минимум 2 Active, 1 Prospect/Backlog, 1 Done, 1 On Hold
- Notes — конкретные детали как настоящий человек пишет ("Waiting for final mockup approval before invoice")
- Все relation-поля заполнены: каждая строка дочерней базы связана с родительской
- **Rollup = 0 → проверь relations в sample_rows.** Title-поле базы всегда `"Name"`
- Двусторонние связи заполняй с обеих сторон (Projects.Skills + Skills.Projects)
- **Rollup не работает без relations в sample_rows** — если Projects.Skills пустой, Skill Count = 0
- Title-поле базы **всегда `"Name"`** (не Company/Title) — иначе `notion_create.py` не линкует строки
- Для каждого relation в properties — ключ с **точными именами строк** в sample_rows:

```json
{"Name": "DevTracker — ...", "Skills": ["React", "TypeScript", "Node.js"]}
{"Name": "React", "Projects": ["DevTracker — ...", "Open Source React Component Library"]}
```

Правило: **rollup count/sum = 0 → проверь relations в sample_rows первым делом**

---

### Views — ручной шаг Owner

Notion API не создаёт виды. Owner добавляет вручную (~5 мин на продукт).

**Обязательные виды для main database:**
- Table (default — всегда есть)
- Board → grouped by Status (Kanban)
- Timeline или Calendar → by Deadline

**Дополнительные виды (если применимо):**
- Gallery (для визуального контента)
- Filtered "Active" (только активные записи)
- Filtered "This Week" (дедлайн в текущей неделе)
- Filtered "Overdue" (просроченные)

Welcome-страница должна объяснять какие виды добавить и как.

---

## 3. Gumroad листинг — формула

### Структура описания (проверенный порядок, 250-400 слов)

```
[1] HOOK — одно предложение, конкретная боль (не "boost productivity")
[2] AGITATE — что происходит без системы (1-2 предложения)
[3] SOLUTION — что это за шаблон (1 предложение)
[4] WHAT'S INSIDE — детальный список (см. ниже)
[5] PERFECT FOR — 3-4 bullet, конкретные профессии/ситуации
[6] QUICK START — 3 шага (опционально, но повышает конверсию)
[7] COMPATIBILITY — Works with Notion Free plan
[8] CTA — Duplicate with one click. One-time payment. Lifetime updates.
```

### What's Inside — писать конкретно (не просто имена баз!)

**Плохо:**
```
✅ Client Database
✅ Project Tracker
✅ Invoice Template
```

**Хорошо:**
```
✅ Clients Database — status (Active/Prospect/On Hold), monthly revenue, email, phone, notes
✅ Projects Database — deadline, budget, hours logged, hourly rate, linked to client
✅ Tasks Database — priority, due date, linked to project, Overdue formula
✅ Total Revenue rollup — each client shows their total budget automatically
✅ Overdue formula — highlights tasks past deadline in red automatically
✅ 6 realistic sample clients + 6 projects pre-filled so you see it working
✅ Board view, Calendar view, Timeline view pre-configured
✅ Step-by-step Welcome guide — start in under 5 minutes
✅ Works with Notion Free plan — no paid subscription needed
```

### Обязательные фразы (вставлять в каждый листинг)

- "Duplicate with one click to your Notion workspace"
- "Works with Notion Free plan — no paid subscription needed"
- "One-time payment. Yours forever. Free updates included."
- "[N] realistic sample entries pre-filled"
- "Start in under 5 minutes"
- "Not a subscription — pay once, use forever"

### Фразы-запреты (никогда не писать)

- "Boost your productivity"
- "Streamline your workflow"
- "All-in-one solution" (заменяй на конкретику что внутри)
- "Empower", "leverage", "robust", "comprehensive"
- Любая фраза без конкретных цифр или объектов

### Цена по количеству баз и сложности

| Структура | Цена |
|-----------|------|
| < 5 баз | Не публикуем — доработать |
| 5 баз + 2 формулы + rollup-цепочка | **$19** |
| 6 баз + 2+ формулы + rollup-цепочка | **$24** |

Стратегия: overdeliver at $19. Покупатель должен чувствовать что получил больше чем заплатил.

**Якорная фраза:**
"Replaces 3 separate spreadsheets — one-time $19, yours forever"

### Теги (10 штук)

```
notion template, [ниша], [аудитория], notion dashboard, digital download,
productivity template, notion planner, [конкретная задача], workflow, 2026
```

---

## 4. ТЕКСТ — обязательные скиллы перед написанием

**Это самый важный раздел.** Слабый текст = нет продаж. Сильный текст = органический трафик + конверсия.

### Шаг 1 — вызови скиллы через `/` (не просто читай файлы)

Перед тем как писать `listing.md` или `user-guide.md`, **обязательно запусти**:

```
/copywriting
```
> Это активирует режим conversion copywriting. Применяй принципы из него к каждому разделу листинга.

```
/marketing-psychology
```
> Это активирует режим психологии покупателя. Применяй выбранные модели к copy до финала.

Без этих вызовов листинг будет feature-dump, не copy.

### 4.1 — video-script.md (TikTok/Reels)

**4 скилла через `/`** перед `video-script.md` — канон: `skills/VIDEO_SCRIPT_SKILL.md`

```
/copywriting
/marketing-psychology
/social-media
/tiktok-script-writer
```

| Скилл | Что даёт video-script |
|-------|----------------------|
| copywriting | clarity, benefits, ≤10 слов в spoken |
| marketing-psychology | JTBD hook, loss aversion, present bias |
| social-media | TikTok algo, hook 0–3s, silent viewers |
| tiktok-script-writer | beat-структура, overlays каждые 3–5s |

**tiktok-script-writer** — установить из GitHub (тикет Mechanic). Адаптация: без FTC #ad, builder tone, 25 сек.

**Verify video-script:**
- [ ] 4 скилла вызваны
- [ ] Hook = JTBD **target_audience** slug
- [ ] Voiceover = builder, spoken ≤10 слов/фраза
- [ ] `## Caption` по шаблону VIDEO_PIPELINE (архив)
- [ ] Нет «I struggled», buzzwords

---

### Шаг 2 — Jobs-to-be-Done (из marketing-psychology)

Перед написанием ответь на вопрос: **что покупатель "нанимает" этот шаблон делать?**

| Аудитория | Ошибка (что MiMo пишет) | Правда (что хочет покупатель) |
|---|---|---|
| Developer | "Track skills and projects" | Получить оффер / не выглядеть джуном на интервью |
| Freelancer | "Manage clients" | Не потерять деньги / иметь нормальный ответ когда клиент спрашивает статус |
| Student | "Organize courses" | Сдать сессию / не провалить дедлайн в 3 часа ночи |
| Founder | "Track metrics" | Не проспать момент когда бизнес умирает / показать инвесторам рост |

**Headline пиши под Job-to-be-Done, не под фичи шаблона.**

---

### Шаг 3 — психологические хуки (применять в listing.md)

Для каждого листинга выбери **3–4 из списка** и явно примени:

**Loss aversion** — покупатель боится потерять больше, чем хочет получить:
```
❌ "Track your freelance clients"
✅ "Stop losing $400 projects because you forgot to follow up"
```

**Anchoring** — поставь дорогое сравнение перед $19:
```
"Career coaches charge $150/hour for what this system does automatically."
"LinkedIn Premium costs $40/month. This is $19. Once."
```

**Specificity > vagueness** (из copywriting):
```
❌ "6 databases with sample data"
✅ "47 pre-filled entries across 6 databases — open it and it already looks like your business"
```

**Present bias** — выгода сейчас, не потом:
```
❌ "You'll see results over time"
✅ "Open it today. By this evening you'll know exactly which client owes you money."
```

**Contrast effect** — before/after (из marketing-psychology):
```
❌ "Organized workspace"
✅ "Before: 3 spreadsheets, 2 Notion pages, and a sticky note.
    After: one workspace where everything connects."
```

---

### Шаг 4 — AIDA в структуре листинга (из copywriting)

```
A — Attention:  Headline + первый абзац. Конкретная боль, без buzzwords.
I — Interest:   Agitate. Что происходит БЕЗ системы. 1-2 предложения.
D — Desire:     What's Inside — конкретные свойства, формулы, данные.
A — Action:     CTA. Не "Instant download" — а что произойдёт КОГДА они купят.
```

**CTA формула (из copywriting):**
```
❌ "Instant download. One-time payment."
✅ "Duplicate to your Notion in 30 seconds. Start using it today."
```

---

### Шаг 5 — чеклист перед финалом listing.md

- [ ] Заголовок отвечает на реальный Job-to-be-Done (не список фич)
- [ ] Первый абзац — конкретная ситуация, не абстрактная боль
- [ ] Есть anchoring (сравнение с более дорогой альтернативой)
- [ ] What's Inside: каждый пункт показывает **что значит** для покупателя (не только имя базы)
- [ ] Есть present bias фраза ("today", "by tonight", "in 5 minutes")
- [ ] CTA — действие + результат, без "streamline" и "boost"
- [ ] Нет: "all-in-one", "productivity", "leverage", "robust", "comprehensive"
- [ ] Tagline = конкретная боль → конкретное решение

---

### Шаг 6 — user-guide.md 1200+ слов (обязательно)

Структура (применяй copywriting принципы к каждому разделу):

```markdown
# User Guide — [Product Name]
## What Problem This Solves  ← Jobs-to-be-Done, не описание фич
## Quick Start (3 шага)     ← activation energy: первый шаг — 1 клик
## Database Guide
  ### [База 1]: [Имя]        ← каждое поле с примером заполнения
  ### [База 2]: [Имя]
  ...
## Power Tips               ← как выжать максимум из шаблона
## FAQ (5 вопросов)         ← objection handling
## How to Customize         ← IKEA effect: они настраивают = их продукт
```

Минимум 1200 слов. Меньше = Grade B.

---

## 5. Pinterest пин

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
- **5+ баз данных**, связанных через Relations
- **2+ формулы** (минимум: Overdue на дочерней + Progress% или Balance на главной)
- **2+ rollup** с цепочкой минимум 2 уровня
- **10+ realistic sample rows** в главной базе, 5+ в каждой дочерней
- Welcome страница 10+ блоков: Quick Start + Database Overview + Pro Tips + Views Guide
- user-guide.md 1200+ слов
- Листинг 250+ слов, все 8 секций, конкретные свойства в What's Inside
- Название: [Аудитория] OS / Hub / System (не Tracker, не Dashboard)
- Tagline: конкретная боль → конкретное решение, без buzzwords

**B** — публикуем только если ≥4 базы, фиксируем в NOTES и доработаем:
- 4 базы данных (не 5) — допустимо если есть 2 формулы + rollup-цепочка
- 8+ sample rows в главной базе
- Листинг 200+ слов
- user-guide.md 900+ слов

**C** — не публикуем, берём другую нишу:
- Менее 4 баз данных
- Меньше 2 формул
- Нет rollup-цепочки (только один уровень)
- Sample data: "Client 1", "Task A", "Example" — placeholder
- Менее 8 sample rows в главной базе
- Нет Welcome страницы или листинга

При C: пишем в NOTES причину → берём следующую нишу из TRENDS.md.

---

## 8. Нишевой гайд — глубина по типам шаблонов

### Freelance / Client Management
- Базы: Clients → Projects → Tasks
- Формулы: `Overdue` на Tasks, `Days Since Last Contact` на Clients
- Rollup: `Total Budget` на Clients (сумма Project.Budget), `Task Count` на Projects
- Views Owner добавляет: Active Clients (filtered), Projects Kanban, This Week Tasks, Overdue

### Content Creator
- Базы: Ideas → Content → Channels
- Формулы: `Days Until Publish`, статус-индикатор
- Rollup: `Published Count` на Channels, `Ideas Count`
- Views: Content Pipeline Kanban, Publishing Calendar, Ideas Backlog

### Finance / Budget
- Базы: Transactions → Categories → Months
- Формулы: `Balance = Income - Expenses`, `% of Budget Used`
- Rollup: Monthly totals из Transactions
- Views: По месяцам, По категориям, Overspent (filtered)

### Job Search
- Базы: Companies → Applications → Contacts → Interviews
- Формулы: `Days Since Applied`, `Stage` indicator
- Rollup: Response Rate (count), Interview Count
- Views: Pipeline Kanban, Follow-up Calendar, Rejected archive

### Student / Study
- Базы: Courses → Assignments → Exams
- Формулы: `Days Until Due`, `Completion %` per course
- Rollup: Assignment Count per course, completed count
- Views: Due This Week, Exam Calendar, Per Course filtered
