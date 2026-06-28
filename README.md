# Gumroad Factory — как запускать

## Проблема которую мы починили

Старый bat использовал **твой обычный Chrome** — debug-порт 9222 не поднимался (лог: `FAIL: Chrome not on port 9222`).

Теперь фабрика использует **отдельный профиль** `.chrome-factory` — порт 9222 работает всегда.

---

## Как это работает (план)

```
┌─────────────────────────────────────────────────────────────┐
│  ОДИН РАЗ: настройка                                         │
│  1. Двойной клик "RodeShop Factory"                           │
│  2. Откроется ОТДЕЛЬНОЕ окно Chrome (не твой обычный)        │
│  3. Войди в Gumroad + Notion в этом окне (один раз)           │
│  4. Сессия сохранится — больше не нужно                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  КАЖДЫЙ ПРОДУКТ: кнопка "RodeShop Factory"                   │
│  Chrome (9222) → setup_product.py →                         │
│    Notion API (страница + DB)                               │
│    Playwright (Share + views)                               │
│    Gumroad (thumbnail + publish)                            │
│    Blog post                                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  БЕСКОНЕЧНЫЙ ЦИКЛ: MiMo в Cursor (один раз запустить)        │
│  Скопируй handoff из docs/team/agents/handoff/mimo.md         │
│  MiMo сам: TRENDS → spec.json → setup_product.py → repeat   │
└─────────────────────────────────────────────────────────────┘
```

---

## Что делать прямо сейчас

### Шаг 1 — один раз
1. Двойной клик **RodeShop Factory** на рабочем столе
2. Откроется Chrome с профилем фабрики (может выглядеть как «новый» браузер)
3. **Войди в Gumroad** (app.gumroad.com) и **Notion** (notion.so) в этом окне
4. Bat сам запустит `setup_product.py` для `notion-freelance-client-tracker`

### Шаг 2 — проверка
- Notion: шаблон опубликован, 3 базы, Board/Calendar views
- Gumroad: https://rodeshop.gumroad.com/l/notion-freelance-client-tracker — live
- Лог: `C:\Users\hramo\gumroad\factory.log`

### Шаг 3 — бесконечный цикл (когда продукт #1 готов)
1. Открой Cursor → новая сессия MiMo
2. Вставь блок из `docs/team/agents/handoff/mimo.md`
3. MiMo генерирует продукты сам; перед каждым setup — Chrome должен быть открыт (кнопка RodeShop Factory)

---

## Два компонента — не путать

| | RodeShop Factory (ярлык) | MiMo (Cursor) |
|---|---|---|
| **Роль** | Публикует готовые файлы | Генерирует новые продукты |
| **Запуск** | Двойной клик | Handoff в чат Cursor |
| **Частота** | На каждый продукт | Один раз → бесконечный цикл |

**Ярлык не запускает MiMo** — это технически невозможно (MiMo = AI в Cursor).

---

## Текущий статус продукта #1

| Шаг | Статус |
|---|---|
| spec.json (3 DB + formula + rollup) | ✅ |
| Notion API (страница + sample data + relations) | ✅ |
| Gumroad draft | ✅ |
| Playwright (Share + views + publish) | ⏳ ждёт логин в factory Chrome |
| Blog post | ⏳ |

---

## Логи

- `factory.log` — что делал bat
- `setup_run.log` — последний запуск setup (если есть)
- `debug_screenshots/` — скриншоты если Playwright застрял
