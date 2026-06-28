# PIPELINE — Как работает конвейер

_Канон. Если расходится с board.html — править оба._

---

## Owner: два режима запуска

### A. Новый продукт с нуля (MiMo генерирует)

```
Двойной клик → Запустить фабрику.bat
```

Bat делает:
1. Chrome factory-профиль на порту **9222**
2. Если в `products/draft/` есть продукт без `notion_result.json` → `setup_product.py`
3. Запускает **mimo_loop.bat** — MiMo генерирует следующие ниши

**Не используй** для hotfix/rebuild уже существующего продукта — MiMo начнёт новую нишу.

---

### B. Опубликовать / пересобрать один продукт (без MiMo)

```
1. Запустить фабрику.bat   ← только Chrome :9222 (можно закрыть mimo окно если открылось)
2. Запустить продукт.bat   ← setup_product.py для конкретного slug
```

Или вручную:
```
start_chrome_debug.bat
python scripts/notion_create.py <slug>    ← только если пересоздаёшь Notion
python scripts/setup_product.py <slug>  ← cover + template + Gumroad + blog
```

**Rebuild/hotfix:** MiMo правит spec → `notion_create.py` (новая страница) → **обязательно** `setup_product.py`.  
Не останавливаться после notion_create. Не Share вручную.

---

### Остановка

`Остановить фабрику.bat` или файл `STOP` в корне. Chrome не закрывать во время Playwright.

---

## MiMo: автономный цикл (mimo_loop.bat)

Каждый цикл MiMo читает `.mimocode/MIMO_FACTORY.md` и:

```
ARCHITECT → выбор ниши (TRENDS.md)
    ↓
CODER     → spec.json, user-guide, listing, blog, quality-report
    ↓ (Grade A)
DESIGNER  → cover-design-brief.md + pillow_pin.py
    ↓
ARCHITECT → setup_product.py (полная публикация)
    ↓
LOG       → STATUS, TRENDS, board.html → сразу следующая ниша
```

---

## setup_product.py — что делает автоматически

| Шаг | Скрипт | Результат |
|-----|--------|-----------|
| 0 | `publish.py` / `notion_create.py` | Notion страница + базы + Gumroad draft |
| 1 | `playwright_notion.py` | **Upload notion-cover.png** + template public + views |
| 1b | `set_template_url.py` | Template URL в описании Gumroad |
| 2 | `pillow_pin.py` (если нет thumb) | gumroad-thumb.png + pinterest-pin.png |
| 3 | `playwright_gumroad.py` | Загрузка обложки + **Publish** на Gumroad |
| 4 | `promote.py` | Blog post → GitHub Pages |

**Playwright** подключается к Chrome `:9222`. Без Chrome — шаги 1 и 3 не работают.

---

## Что НЕ делает Owner (устарело)

- ~~Notion Share вручную~~
- ~~Gumroad thumbnail вручную~~
- ~~Ярлык RodeShop Setup~~
- ~~batch_activate.py~~
- ~~Добавление views в Notion~~

---

## Опционально позже (не блокирует конвейер)

| Когда | Owner | Статус |
|-------|-------|--------|
| Video Pipeline готов | TikTok + Reels — залить mp4 | план |
| Июль | Notion Marketplace — free lite | план |
| Pinterest API | ничего — promote.py автопост | ждём токен |

---

### Owner: Rebuild Wave (активен)

```
Запустить фабрику.bat
```

Если `docs/team/active/rebuild-queue.txt` имеет pending slug → **rebuild_loop.bat** (5 сек между циклами, без TRENDS).

MiMo: полный pipeline на slug → `# DONE` в queue → сразу следующий.

Когда все `# DONE` → автоматически normal mimo_loop.

---

## Gumroad лимит

**10 продуктов/день** — если лимит, setup_product падает на Gumroad publish.
MiMo продолжает генерировать draft; publish на следующий день.

---

## Rebuild Wave — пересборка live-продуктов

_Когда качество старого контента не тянет новый стандарт._

### Nuclear reset (0 buyers) — TASK-018, 28.06

**Owner решил:** wipe + CREATE заново быстрее fix rebuild.

| Объект | Действие |
|--------|----------|
| Gumroad продукты | **Удалить все 7** в dashboard |
| `gumroad_result.json` | **Удалить** draft+ready (CREATE заново) |
| `notion_result.json` | **Удалить** draft+ready |
| Notion OS pages | **0** в workspace |
| spec/listing/user-guide | **Оставить** в draft |

После wipe: `publish.py` (CREATE) → `setup_product.py`. Pilot 1 slug → масштаб.

### Rebuild (есть покупатели) — старый режим

_Не nuclear reset._

### Что УДАЛЯТЬ / что НЕ трогать (rebuild mode)

| Объект | Действие | Почему |
|--------|----------|--------|
| **Gumroad продукты** | **НЕ удалять** | Permalink и URL покупателей сохраняются. API обновляет тот же продукт по `gumroad_result.json` |
| **Gumroad картинки** | **Обновить** через `setup_product.py` | `playwright_gumroad.py` заливает новый `gumroad-thumb.png` |
| **Gumroad описание** | **Обновить** автоматом | `set_template_url.py` + API — новый listing + template link |
| **Notion дубли** | **Удалить вручную** | 2–3 страницы одного OS = мусор. Оставь 0 до rebuild, потом 1 |
| **Notion после rebuild** | Удалить **старые** версии | Когда новая опубликована и проверена (Publish tab!) |
| **`gumroad_result.json`** | **Сохранить** | Связь slug ↔ Gumroad product ID. Без него — риск дубля |
| **`products/ready/`** | Перезаписать из draft | После успешного setup |

### Gumroad «перенастраивать» не нужно

Связь уже в файлах:

```
products/draft/<slug>/gumroad_result.json
  → gumroad_product_id
  → gumroad_short_url  (rodeshop.gumroad.com/l/<slug>)
```

Rebuild = тот же slug → API **update**, не новый продукт.

---

### Порядок на один продукт

```
0. Mechanic закрыл notion-publish-false-success (Publish tab реально работает)
1. Owner: удалить в Notion ВСЕ старые страницы этого slug (дубли)
2. MiMo: spec + listing + user-guide + relations в sample_rows
3. python scripts/notion_create.py <slug>
4. python scripts/pillow_pin.py <slug>          ← новые картинки
5. python scripts/setup_product.py <slug>       ← template + Gumroad thumb + listing
6. Owner verify: Share → Publish → NOT "Only people invited"
7. draft/ → ready/ sync
8. Следующий slug (1–2 в день, лимит Gumroad)
```

**Hotfix одного продукта:** шаги 1–7. **Не** `Запустить фабрику.bat` (MiMo начнёт новую нишу).

---

### Очередь Rebuild Wave (7 live)

| # | Slug |
|---|------|
| 1 | `notion-developer-career-os` — пилот |
| 2 | `notion-freelance-client-tracker` |
| 3 | `notion-job-search-command-center` |
| 4 | `notion-study-knowledge-management` |
| 5 | `notion-personal-finance-tracker` |
| 6 | `notion-social-media-content-calendar` |
| 7 | `notion-startup-metrics-okr-tracker` |

`notion-content-creator-dashboard` — HOLD.

---

### Owner: чистка Notion

**Можно удалить:** все дубли OS-шаблонов (поиск по названию продукта).

**Не удаляй:** Gumroad, `gumroad_result.json`, личные страницы Notion.

**Gumroad:** продукты не удалять — только обновление через setup.
