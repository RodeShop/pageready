# TASK-022 — Preview 4 cover directions (D/E/F/G)

**Slug:** `notion-developer-career-os`  
**Owner:** нужны **по 1 превью** каждого направления, чтобы выбрать стиль  
**Маршрут:** `@coder`

---

## Промпт для Coder (копипаст)

```
Роль: @coder · Designer preview · slug notion-developer-career-os

ОБЯЗАТЕЛЬНО активируй скилл /design-lebedev (Pass 1 → Pass 2 → код).
Читай:
- products/draft/notion-developer-career-os/cover-variant-exploration.md (D/E/F/G)
- docs/team/active/GUMROAD-IMAGE-SPEC.md
- products/draft/notion-developer-career-os/spec.json

## Задача

Сгенерировать **4 направления × 2 файла = 8 PNG** (только превью, не production):

assets/gumroad-variants/notion-developer-career-os/round-2/
  variant-D-cover-1920x1080.png
  variant-D-thumb-1200x1200.png
  variant-E-cover-1920x1080.png
  variant-E-thumb-1200x1200.png
  variant-F-cover-1920x1080.png
  variant-F-thumb-1200x1200.png
  variant-G-cover-1920x1080.png
  variant-G-thumb-1200x1200.png

## Направления (из brief)

| ID | Имя | Signature |
|----|-----|-----------|
| D | Database view | Notion table с sample rows (DevTracker, chips Status/Tech) |
| E | Relation map | 6 баз как hub+spokes, синие линии связей |
| F | Editorial proof | Крупный type + 3 proof lines, zero cards |
| G | Gumroad meta | Fake Gumroad product page + Discover card (pink #ff90e8 CTA) |

## Контент

- title: Developer Career OS
- tagline: The system that shows your career growth before the interviewer asks
- brand: RodeShop · $19
- 6 databases: Projects, Jobs, Skills, Learning, Networking, Achievements
- Без emoji

## Техника

Создай scripts/generate_cover_variants.py (≤200 строк) ИЛИ расширь pillow_pin.py флагом --variant D|E|F|G.
Предпочтение: отдельный скрипт для превью, production pillow_pin не ломать.

Шрифты: Segoe UI / Arial на Windows — НЕ load_default() без fallback.
8px grid. Tagline полностью видна. Cover и thumb — **разные layouts** под aspect ratio.

## Запрещено

- notion-cover.png — не трогать
- playwright_*.py — не трогать
- Round 1 layouts A/B/C
- AI-defaults (Lebedev §1)
- Один PNG на оба поля Gumroad
- Gumroad logo/trademark — только stylized visual language

## Acceptance

- [ ] 8 PNG в round-2/
- [ ] tagline не обрезана
- [ ] thumb читается как preview 600×600
- [ ] G выглядит как Gumroad page/card, не generic template
- [ ] STATUS: что сгенерировано + как перегенерить

После: @lead verify → Owner выбирает D/E/F/G
```

---

## Owner

Открыть `assets/gumroad-variants/notion-developer-career-os/round-2/` → выбрать **D / E / F / G**.

## После выбора

Lead → Coder/Mechanic: вшить winner в `pillow_pin.py` → upload.
