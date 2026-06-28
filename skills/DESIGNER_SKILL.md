# DESIGNER_SKILL — MiMo Designer Mode

## Обязательный скилл

/design-lebedev
Применяй: function over form, distinctiveness, без AI-дефолтов, типографика.

Затем читай:
1. `skills/COVER_DIRECTIONS.md` — **D System Cards, без emoji**
2. Этот файл

---

## Direction D — System Cards (утверждено)

- Фон `#eef1f5`, белые карточки = **3 главные базы** (Gumroad + Pinterest)
- Title + tagline (конкретная боль)
- **Notion cover:** strip-only — title + tagline + brand, **без cards** → `COVER_DIRECTIONS.md`
- **Запрещено:** emoji, стикеры, иконки-наклейки, gradient+emoji hero
- Signature: три карточки = «OS из частей» (только Gumroad/Pinterest)

---

## Процесс

```
1. cover-design-brief.md — tokens + 3 db names для карточек
2. Self-critique (Lebedev §2 Pass 2)
3. python scripts/pillow_pin.py <slug>
```

### cover-design-brief.md

```markdown
# Cover Design Brief — [Product]

**Direction:** D — System Cards (no emoji)

## Cards (top 3 databases)
1. [db1 name]
2. [db2 name]
3. [db3 name]

## Tokens
| bg | #eef1f5 |
| accent | [from cover_color] |

## Copy
- Title: [spec.title]
- Tagline: [spec.tagline — concrete, no buzzwords]
```

---

## Выходные файлы

```
products/draft/<slug>/
├── cover-design-brief.md
├── gumroad-thumb.png      1600×900
├── pinterest-pin.png      1000×1500
└── notion-cover.png       1920×800  ← Notion banner, Playwright upload
```

---

## Режим генерации

| | |
|---|---|
| Default | `python scripts/pillow_pin.py <slug>` |
| OpenAI | только если `OPENAI_API_KEY` + `ENABLE_GARDEN_IMAGEGEN=1` |

---

## Чеклист

- [ ] cover-design-brief.md с 3 card names
- [ ] design_lebedev critique — no AI defaults
- [ ] gumroad-thumb + pinterest-pin + **notion-cover.png**
- [ ] **Нет emoji** на всех трёх
- [ ] Tagline читается на thumb 400px width
