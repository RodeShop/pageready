# PROJECT_MAP — RodeShop Gumroad Factory

> Читай этот файл первым. Здесь вся структура проекта.

---

## Что это

Автономная фабрика Notion OS-шаблонов. Продаёт через Gumroad по $19.
Стратегия: тяжёлые системы (5-6 связанных баз) по доступной цене — overdeliver через объём.

**Gumroad:** rodeshop.gumroad.com  
**GitHub Pages (блог):** rodeshop.github.io/pageready/

---

## Команда и роли

| Роль | Cursor rule | Зона ответственности |
|------|-------------|----------------------|
| **Owner** | `@owner` | Финальный просмотр, заливка видео в TikTok, контроль дохода |
| **Lead** | `@lead` | Тренды, очередь, архитектура, verify продуктов |
| **MiMo** | `@mimo` | Автономная генерация продуктов в цикле |
| **Mechanic** | `@mechanic` | Баги, качество, тикеты в `docs/problems/` |

**Правило:** Owner не даёт MiMo инструкции напрямую — только через `docs/team/active/TASK.md`.

---

## Карта файлов

```
gumroad/
│
├── PROJECT_MAP.md          ← ты здесь (читай первым)
├── ROADMAP.md              ← план развития (видео, Pinterest, новые форматы)
│
├── Запустить фабрику.bat   ← Chrome + mimo_loop.bat (Owner)
├── Остановить фабрику.bat  ← создаёт STOP файл (Owner)
├── mimo_loop.bat           ← MiMo цикл (mimo run в петле)
├── factory.log             ← лог запусков
│
├── .mimocode/
│   └── MIMO_FACTORY.md     ← главные инструкции для MiMo
│
├── skills/
│   ├── MIMO_SKILL.md       ← стандарты качества, ценообразование, листинг
│   ├── NOTION_BLOCKS.md    ← формат spec.json (Welcome блоки, базы данных)
│   ├── NOTION_QUALITY.md   ← чеклист проверки качества (Mechanic)
│   └── DESIGNER_SKILL.md   ← инструкции по thumbnail/pin генерации
│
├── research/
│   └── TRENDS.md           ← очередь ниш, исследования, сделанные продукты
│
├── products/
│   ├── queue/              ← ниши ожидают генерации (<slug>.md каждая)
│   ├── draft/<slug>/       ← MiMo генерирует сюда
│   ├── ready/<slug>/       ← готово к публикации (Lead проверил)
│   └── published/<slug>/   ← опубликовано Owner
│
├── listings/
│   └── <slug>.md           ← листинги для Gumroad (копия из draft)
│
├── docs/
│   ├── team/
│   │   ├── active/
│   │   │   └── TASK.md     ← текущая задача для MiMo (Lead пишет)
│   │   ├── common/
│   │   │   ├── STATUS.md   ← текущий снимок состояния (MiMo обновляет)
│   │   │   ├── VIDEO_PIPELINE.md ← план видео генерации (запланировано)
│   │   │   └── ROADMAP.md  ← план развития
│   │   └── agents/
│   │       └── EXECUTOR_RULES.md ← hard rules для всех агентов
│   └── problems/
│       └── <ticket>.md     ← баг-тикеты (Mechanic закрывает)
│
├── scripts/
│   ├── setup_product.py    ← главный координатор pipeline
│   ├── publish.py          ← Notion API + Gumroad API
│   ├── playwright_notion.py ← Share/Publish + Board/Calendar views
│   ├── playwright_gumroad.py ← cover upload + file upload + publish
│   ├── pillow_pin.py       ← генерация thumbnail + pinterest pin
│   └── promote.py          ← blog post + Pinterest
│
└── assets/                 ← (создать) музыка и Notion клипы для видео
    ├── music/              ← royalty-free MP3 треки
    └── notion-clips/       ← скринкасты Notion (Owner записывает 1 раз)
```

---

## Pipeline (полная цепочка)

```
Owner:     Запустить фабрику.bat  (один раз)
           ↓
MiMo loop: Architect → Coder → Designer → setup_product.py → LOG → следующая ниша
           ↓
Lead:      verify (по запросу / hotfix)
```

**Автоматизировано полностью (Owner = 0 мин на продукт):**
- Notion API + Playwright: страница, базы, **template public**, views
- Gumroad API + Playwright: draft, thumbnail, **publish**
- Pillow: обложки (обновление дизайна — см. `skills/COVER_DIRECTIONS.md`)
- GitHub Pages: blog post

**Опционально позже (Owner):**
- TikTok/Reels — когда Video Pipeline готов
- Notion Marketplace free lite — июль

Канон: `docs/team/common/PIPELINE.md`

---

## Стандарт качества (обязательный минимум)

| Параметр | Требование |
|---|---|
| Баз данных | **5 минимум** (6 для $24) |
| Формулы | **2+** (Overdue + Progress% как база) |
| Rollup chains | **2 уровня** (Tasks→Projects→Clients) |
| Sample rows | **10+** в главной базе, 5+ в дочерних |
| user-guide.md | **1200+ слов** |
| Цена | **$19** (5 баз) / **$24** (6+ баз) |
| Нейминг | **"X OS" / "X Hub" / "X System"** |

Grade A = публикуем. Grade B = доработать. Grade C = пропускаем нишу.

---

## Текущий статус

Смотри: `docs/team/common/STATUS.md`

**Быстро:** 8 продуктов live, MiMo работает, следующий — Agency Client OS.

---

## Запланировано (следующее)

Смотри: `ROADMAP.md`

1. **Video Pipeline** — TikTok/Reels видео к каждому продукту (moviepy + ElevenLabs)
2. **Pinterest API** — ждём одобрения dev app
3. **Trend Research** — при 10 продуктах обновить TRENDS.md
