# ROADMAP — RodeShop Development Plan

_Обновлено: 28.06.2026 · порядок выполнения сверху вниз_

---

## Сейчас — Июль неделя 1

### 0. Hotfix live продуктов 🔴

| # | Задача | Кто | Статус |
|---|--------|-----|--------|
| 0.1 | **Developer Career OS** — rollup, Jobs, cover, relations | MiMo | TASK-015 |
| 0.2 | **Agency Client OS** — 6 баз, формулы, user-guide 1200+ | MiMo | TASK-013 |
| 0.3 | Gumroad publish Agency (лимит 10/день) | MiMo | 29.06 |

### 1. Video Pipeline — TikTok + Reels ⚡

| # | Задача | Кто |
|---|--------|-----|
| 1.1 | `scripts/generate_video.py` (moviepy + ElevenLabs) | Mechanic |
| 1.2 | `video-script.md` в Coder Mode MiMo | Lead → MiMo |
| 1.3 | Owner: 4-5 клипов → `assets/notion-clips/` | Owner |
| 1.4 | Owner: 2-3 трека → `assets/music/` + `ELEVENLABS_API_KEY` | Owner |
| 1.5 | Каждый продукт → `tiktok-video.mp4` | авто |
| 1.6 | **Instagram Reels** — тот же файл, +0 мин | Owner |

Детали: `docs/team/common/VIDEO_PIPELINE.md`

**Почему сейчас:** Notion-шаблоны органически взлетают на TikTok (#NotionTemplate, #StudyWithMe). Faceless screencast = 38% новых монетизируемых каналов 2025.

---

## Июль неделя 2–3 — Органический трафик

### 2. Notion Marketplace — бесплатная приманка ✅

| # | Задача | Кто |
|---|--------|-----|
| 2.1 | Lite-версия каждого OS (2-3 базы, sample data) | MiMo |
| 2.2 | Publish free на Notion Marketplace (без Stripe) | Owner |
| 2.3 | Внутри lite → CTA «Full OS on Gumroad $19» | MiMo |
| 2.4 | Чеклист lite vs full в `skills/MIMO_SKILL.md` | Lead |

**Воронка:** человек уже в Notion → дублирует free → видит ссылку → Gumroad.

### 3. Freemium в TikTok-описании ✅

| # | Задача | Кто |
|---|--------|-----|
| 3.1 | В bio/описании Reels — ссылка на free lite (Notion Marketplace) | Owner |
| 3.2 | Gumroad email capture (Follow / wishlist) | Owner |
| 3.3 | Последовательность: hook video → free lite → upsell full OS | Lead docs |

**Не делаем:** автозаливку TikTok (риск бана).

### 4. Pinterest API (ожидание)

- Dev app одобрение → `promote.py` автопост 2-3 пина/день

---

## Август — Масштаб

### 5. Bundle под брендом RodeShop ✅

| # | Задача | Кто |
|---|--------|-----|
| 5.1 | Правило: 3+ OS в одной категории → bundle | Lead |
| 5.2 | MiMo генерирует bundle listing ($39 vs 3×$19) | MiMo |
| 5.3 | Первый кандидат: **Developer + Agency + Freelance** ($39) | — |

### 6. Конвейер продуктов

- YouTube Creator OS → Remote Team OS → trend research
- 20+ продуктов live
- A/B thumbnail стили
- Анализ конверсии по нишам

---

## Фаза 1 — выполнено ✅

- [x] MiMo автономная генерация
- [x] Playwright Notion + Gumroad
- [x] 8 продуктов (7 published)
- [x] Pinterest pins (Pillow)
- [x] GitHub Pages blog
- [x] Новый стандарт: 5+ баз, $19, OS naming

---

## Не делаем

- Twitter/X, Reddit автопостинг — бан
- Автозаливка TikTok/Reels — бан
- Цены > $24 на старте без отзывов
- Etsy — только после 20 продуктов и данных по конверсии
