# ТЗ — Gumroad Factory

**Дата:** 2026-06-27  
**Статус:** Финальное

---

## Цель

Автономная фабрика: МиМо генерирует Notion-шаблоны, Python-скрипты публикуют их в Notion и на Gumroad. Владелец тратит ~5 минут в день на один ручной шаг.

---

## Что продаём

**Notion Template** — готовое рабочее пространство для конкретной ниши.  
Покупатель платит $19–39, получает ссылку "Duplicate template", за 2 минуты разворачивает у себя.

Примеры: Freelance Client Tracker, Content Creator Dashboard, Job Search Planner, Startup OKR Tracker.

---

## Полный пайплайн

```
┌─────────────────────────────────────────────────────────────┐
│                     FACTORY LOOP                             │
│                                                              │
│  research/TRENDS.md                                          │
│        │                                                     │
│        ▼                                                     │
│  ① [GENERATOR] МиМо — фаза 1                                │
│     Читает нишу → генерирует spec.json + листинг + гайд     │
│        │                                                     │
│        ▼                                                     │
│  ② [REVIEWER] МиМо — фаза 2                                 │
│     Проверяет по skills/NOTION_QUALITY.md                    │
│     Оценка A/B → proceed │ C → refine (макс 2 итерации)     │
│        │                                                     │
│        ▼                                                     │
│  ③ python scripts/publish.py <slug>                          │
│     → создаёт страницу + базы в Notion (API)                │
│     → сохраняет Notion URL                                   │
│     → создаёт листинг на Gumroad (API)                       │
│     → сохраняет Gumroad URL                                  │
│     → обновляет STATUS.md                                    │
│        │                                                     │
│        ▼                                                     │
│  ④ [РУЧНОЙ ШАГ — 10 сек/шт]                                 │
│     Владелец открывает Notion → Share → Publish →            │
│     Allow template duplication → копирует ссылку →           │
│     python scripts/set_template_url.py <slug> <url>          │
│        │                                                     │
│        ▼                                                     │
│  ⑤ Листинг на Gumroad обновлён с реальной ссылкой            │
│     products/published/<slug>/  ← архив                     │
│                                                              │
│        ↓ следующая ниша из TRENDS.md                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Техническое ограничение (честно)

**Notion API не умеет:**
- Делать страницу публичной
- Создавать views (Board, Calendar, Gallery)

**Решение:**
- Views МиМо документирует в user-guide — покупатель добавляет сам за 1 минуту
- Публичность — один ручной клик на шаге ④ (10 секунд)
- Делаем батчами: МиМо нагенерировал 10 шаблонов → ты за 2 минуты делаешь все публичными

---

## Структура файлов продукта

```
products/
└── draft/<slug>/
    ├── spec.json          ← машиночитаемая структура шаблона
    ├── user-guide.md      ← инструкция для покупателя
    ├── listing.md         ← текст листинга для Gumroad
    └── quality-report.md  ← результат самопроверки МиМо

products/ready/<slug>/     ← после прохождения quality check
    ├── (те же файлы)
    ├── notion-page-id.txt ← после шага ③
    └── gumroad-product-id.txt

products/published/<slug>/ ← после шага ④
    ├── (все файлы)
    ├── notion-template-url.txt ← публичная ссылка
    └── gumroad-url.txt
```

### Формат spec.json

```json
{
  "title": "Freelance Client Tracker",
  "emoji": "💼",
  "target_audience": "Freelancers",
  "price": 29,
  "tagline": "Never lose track of a client again",
  "databases": [
    {
      "name": "Clients",
      "emoji": "👤",
      "properties": [
        {"name": "Name", "type": "title"},
        {"name": "Status", "type": "select",
         "options": [
           {"name": "Active", "color": "green"},
           {"name": "Prospect", "color": "yellow"},
           {"name": "Inactive", "color": "gray"}
         ]},
        {"name": "Email", "type": "email"},
        {"name": "Monthly Revenue", "type": "number", "format": "dollar"},
        {"name": "Projects", "type": "relation", "related_db": "Projects"}
      ],
      "sample_rows": [
        {"Name": "Acme Corp", "Status": "Active", "Email": "hi@acme.com", "Monthly Revenue": 2500},
        {"Name": "StartupXYZ", "Status": "Prospect", "Email": "founder@xyz.com", "Monthly Revenue": 0}
      ],
      "recommended_views": [
        {"name": "All Clients", "type": "table"},
        {"name": "By Status", "type": "board", "group_by": "Status"},
        {"name": "Active Only", "type": "table", "filter": "Status = Active"}
      ]
    }
  ],
  "welcome_page": {
    "sections": ["What this template does", "Quick start (3 steps)", "Database overview", "Pro tips"]
  }
}
```

---

## Скрипты

### `scripts/publish.py <slug>` — главный оркестратор

```
1. Читает products/ready/<slug>/spec.json
2. Вызывает notion_create.py → создаёт страницу + базы
3. Добавляет sample rows через API
4. Сохраняет notion-page-id.txt
5. Вызывает gumroad_create.py → создаёт листинг (draft)
6. Сохраняет gumroad-product-id.txt
7. Перемещает папку draft → ready
8. Обновляет STATUS.md
```

### `scripts/notion_create.py`

- Создаёт страницу под Factory Templates
- Создаёт все базы данных из spec.json
- Добавляет sample rows
- Создаёт Welcome-страницу с инструкцией
- Возвращает page_id

### `scripts/gumroad_create.py`

- Создаёт продукт в Gumroad (draft, не публичный)
- Загружает user-guide.pdf как файл продукта
- Устанавливает цену из spec.json
- Возвращает product_id

### `scripts/set_template_url.py <slug> <notion-public-url>`

- Обновляет Gumroad листинг: добавляет ссылку в описание
- Публикует листинг (is_published: true)
- Перемещает папку в published/
- Обновляет STATUS.md

---

## МиМо скилл

Файл: `skills/MIMO_SKILL.md`

Содержит:
- Как проектировать нишевую базу данных (примеры хороших vs плохих)
- Какие property types использовать для каких задач
- Как писать sample data (реалистично, не "Example 1")
- Формула идеального Gumroad-листинга
- Правила самооценки (A/B/C)
- Autocompact: после каждых 5 продуктов сохранить checkpoint в STATUS.md

---

## Мультиагентный цикл МиМо

МиМо работает в одной сессии, три фазы на каждый продукт:

```
[GENERATE] → создаёт spec.json + листинг + гайд
     ↓
[REVIEW]   → проверяет по NOTION_QUALITY.md → оценка A/B/C
     ↓ если C
[REFINE]   → дорабатывает (макс 2 попытки, потом берёт другую нишу)
     ↓ если A/B
[PUBLISH]  → запускает python scripts/publish.py <slug>
     ↓
[LOG]      → обновляет STATUS.md + TRENDS.md
     ↓
[NEXT]     → следующая ниша
```

**Autocompact:** после каждых 5 продуктов МиМо пишет в STATUS.md полный снимок состояния и сжимает контекст `/compact`.

---

## Продвижение (промоушен)

### Каналы и автоматизация

| Канал | Трафик | Автоматизация |
|-------|--------|---------------|
| **Pinterest** | Главный. 60–80% у топ-продавцов | Полная — API + Pillow |
| **Google SEO** | Накопительный, через блог | Полная — GitHub Pages |
| **Reddit** | Хороший, но бан за автопостинг | Черновик — ты постишь |
| **Gumroad Discover** | Слабый, бесплатный | Через теги |

### Pinterest pipeline

```
МиМо пишет pinterest-pin.md →
Python (Pillow) генерирует картинку 1000×1500px →
Pinterest API публикует пин →
Трафик идёт месяцами
```

**Регистрация:** при создании Pinterest developer account — выбрать тип бизнеса **"Другой"** (не "Интернет-магазин" — сайт не нужен).

**Что нужно:** Pinterest developer account → API ключ → добавить в `.env`

### SEO-блог GitHub Pages

```
МиМо пишет blog-post.md (600–800 слов) →
python blog_publish.py <slug> →
git commit → GitHub Pages →
Google индексирует за 1–3 дня
```

**Что нужно:** создать GitHub репо + Pages (5 минут, один раз)

### Reddit черновики

МиМо пишет `promotion/reddit/<slug>.md` — готовый пост для нужного сабреддита.  
Ты вставляешь и постишь за 30 секунд.

Целевые сабреддиты: r/Notion, r/productivity, r/freelance, r/entrepreneur, r/sidehustle

### Новые файлы МиМо на каждый продукт

```
products/draft/<slug>/
├── spec.json
├── user-guide.md
├── listing.md
├── pinterest-pin.md     ← заголовок + описание + хэштеги + концепт картинки
├── blog-post.md         ← SEO-статья 600–800 слов
└── reddit-draft.md      ← готовый пост для нужного сабреддита
```

### Новые скрипты промоушена

**`scripts/pinterest_publish.py <slug>`**
- Читает `products/ready/<slug>/pinterest-pin.md`
- Создаёт изображение через Pillow (фон + текст + брендинг)
- Постит через Pinterest API
- Возвращает URL пина

**`scripts/blog_publish.py <slug>`**
- Читает `products/ready/<slug>/blog-post.md`
- Коммитит в GitHub Pages репо
- Статья онлайн

**`scripts/promote.py <slug>`** — оркестратор:
- Запускает pinterest_publish.py
- Запускает blog_publish.py
- Сохраняет URLs в STATUS.md

### Дополнительно в .env

```
PINTEREST_ACCESS_TOKEN=
GITHUB_TOKEN=
GITHUB_BLOG_REPO=username/blog
```

---

## Порядок реализации (сегодня)

| # | Задача | Кто | Статус |
|---|--------|-----|--------|
| 1 | `scripts/notion_create.py` | Claude Code | — |
| 2 | `scripts/gumroad_create.py` | Claude Code | — |
| 3 | `scripts/publish.py` | Claude Code | — |
| 4 | `scripts/set_template_url.py` | Claude Code | — |
| 5 | `scripts/pinterest_publish.py` | Claude Code | — |
| 6 | `scripts/blog_publish.py` | Claude Code | — |
| 7 | `scripts/promote.py` | Claude Code | — |
| 8 | `skills/MIMO_SKILL.md` | Claude Code | — |
| 9 | Обновить `MIMO_FACTORY.md` (мультиагент + autocompact) | Claude Code | — |
| 10 | Pinterest developer account → API ключ в .env | Владелец | — |
| 11 | GitHub Pages блог → токен в .env | Владелец | — |
| 12 | Gumroad профиль: имя магазина, аватар | Владелец | — |
| 13 | Тест: МиМо → первый продукт end-to-end | МиМо | — |
| 14 | Ручной шаг: Share в Notion | Владелец | — |
| 15 | Листинг + пин + статья живые | ✓ | — |

---

## Что от тебя (один раз)

- [x] Notion API ключ
- [x] Gumroad API ключ
- [x] Страница Factory Templates создана
- [ ] Зарегистрироваться на Gumroad и заполнить профиль (имя магазина)
- [ ] Пройти ручной шаг ④ после первого теста

---

## Что МиМо делает полностью сам

- Исследует нишу (TRENDS.md)
- Проектирует шаблон (spec.json)
- Пишет user guide
- Пишет листинг для Gumroad
- Самопроверка качества
- Создаёт шаблон в Notion через API
- Публикует на Gumroad через API
- Ведёт STATUS.md
- Сжимает контекст после 5 продуктов
- Берёт следующую нишу

**Итого твоего времени:** ~5–10 секунд на публикацию шаблона в Notion (один клик).
