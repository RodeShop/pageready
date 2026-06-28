# COVER DESIGN — RodeShop (УТВЕРЖДЕНО)

**Выбор Owner:** 28.06.2026  
**Направление:** **D — System Cards**  
**Запрет:** emoji, стикеры, иконки-наклейки — удешевляет.

**Скилл:** `/design-lebedev` (запускай через `/`, не просто читай файл)

---

## Direction D — System Cards (финал)

| Token | Значение |
|-------|----------|
| bg | `#eef1f5` cool gray |
| card | `#ffffff` + shadow `0 2px 8px rgba(0,0,0,0.08)` |
| ink | `#121212` title |
| muted | `#64748b` tagline |
| accent | из `spec.cover_color` → SCHEMES accent |

### Layout Gumroad thumb (1600×900)

```
┌─────────────────────────────────────────────┐
│  [Title — bold, top center]                 │
│  [Tagline — concrete pain, gray]            │
│                                             │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│   │ DB name │ │ DB name │ │ DB name │      │  ← 3 главные базы из spec
│   │         │ │         │ │         │      │
│   └─────────┘ └─────────┘ └─────────┘      │
│                                             │
│              RodeShop · $19                 │
└─────────────────────────────────────────────┘
```

- **Без emoji** anywhere
- Карточки = названия первых 3 баз из `spec.databases`
- Tagline = `spec.tagline` (конкретная боль)

### Layout Pinterest pin (1000×1500)

Та же система, вертикально: title → tagline → 3 cards stacked → RodeShop · price

### Layout Notion cover (3000×1200) — **strip-only** ✅ Owner 28.06

**Notion cover ≠ Gumroad thumb.** Cover strip на экране ~250px; полный Direction D с cards даёт гигант + дубль списка баз ниже.

| Параметр | Значение |
|----------|----------|
| Canvas | 3000×1200 (5:2) |
| Safe zone | y=480..720, x=900..2100 |
| Контент | title 48px · tagline 22px · accent rule · RodeShop 18px |
| Центрирование | по CX=1500 |
| **Запрещено** | 3 cards, emoji, edge-to-edge layout |

```
[======== plain #eef1f5 ========]
        Title (bold)
        tagline (muted)
        ── accent ──
        RodeShop
[======== plain #eef1f5 ========]
```

Gumroad thumb + Pinterest pin — **полный Direction D с cards** (без изменений).

Файл: `notion-cover.png` · генерация: `pillow_pin.py` · upload: `playwright_notion.py`

История fixes: `docs/problems/2026-06-28-notion-cover-strip-safezone.md`

### Gumroad thumb (1600×900) — без изменений

Gumroad показывает **600px wide** — source 1600×900 достаточен.  
Проблема не в размере, а в **upload** (`playwright_gumroad.py` — тикет Mechanic).

---

## Designer Mode workflow

1. `/design-lebedev`
2. Write `cover-design-brief.md` (tokens + 3 db names for cards)
3. `python scripts/pillow_pin.py <slug>` → 3 файла:
   - `gumroad-thumb.png`
   - `pinterest-pin.png`
   - `notion-cover.png`
4. Critique: нет emoji? карточки читаются? tagline конкретный?

---

## Mechanic

Тикет: `docs/problems/2026-06-28-cover-redesign.md`
