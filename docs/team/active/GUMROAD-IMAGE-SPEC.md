# Gumroad + Factory — карта изображений

**Slug pilot:** `notion-developer-career-os`  
**Owner запрос:** пересмотр Gumroad-дизайна · варианты на выбор

---

## Сколько файлов на 1 продукт

| # | Файл | Размер (source) | Aspect | Куда | Формат |
|---|------|-----------------|--------|------|--------|
| 1 | `gumroad-cover.png` | **1920×1080** (min 1280×720) | 16:9 | Gumroad **Cover** — hero на странице продукта | PNG |
| 2 | `gumroad-thumb.png` | **1200×1200** (min 600×600) | 1:1 | Gumroad **Thumbnail** — Library, Discover, Profile | PNG |
| 3 | `notion-cover.png` | 3000×1200 | 5:2 strip | Notion page cover (strip-only, без cards) | PNG |
| 4 | `pinterest-pin.png` | 1000×1500 | 2:3 | Pinterest (позже) | PNG |

**Итого для Gumroad: 2 разных файла.** Сейчас один `gumroad-thumb.png` 1600×900 заливается в оба поля — Thumbnail квадратный остаётся пустым/обрезанным.

---

## Gumroad UI (из edit page)

| Секция | Требование Gumroad | Наш source |
|--------|-------------------|------------|
| **Cover** | horizontal, ≥1280×720, JPG/PNG/GIF | `gumroad-cover.png` |
| **Thumbnail** | **square**, ≥600×600 | `gumroad-thumb.png` |
| **Content** | `user-guide.md` (не картинка) | без изменений |

Upload: `playwright_gumroad.py` — Cover input (accept mov/mp4) + Thumbnail label Upload.

---

## Notion — отдельно

Notion cover **не** Direction D с cards → strip-only (`COVER_DIRECTIONS.md`). Не смешивать с Gumroad.

---

## Варианты для выбора (28.06)

Папка: `assets/gumroad-variants/notion-developer-career-os/`

| ID | Имя | Signature (Lebedev) |
|----|-----|---------------------|
| **A** | Module rail | 6 модулей компактной сеткой 2×3 — меньше «пустоты» |
| **B** | Split proof | Title слева, 3 cards крупнее справа, accent bar |
| **C** | Type stack | Крупная типографика + tagline; модули pill-row внизу |

Каждый вариант: `-cover-1920x1080.png` + `-thumb-1200x1200.png`.

После выбора Owner → обновить `pillow_pin.py` + `COVER_DIRECTIONS.md` + Lead verify.

---

## Design skill

Активирован: `/design-lebedev` (`design_lebedev.md`) — Pass 1 plan + Pass 2 critique в `cover-variant-exploration.md`.
