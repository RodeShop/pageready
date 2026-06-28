# PILOT — один slug до конца (Lead verify)

**Slug:** `notion-developer-career-os`  
**Правило:** без ✅ на всех gate → **запрещено** `# DONE` и следующий slug.

---

## Gate 0 — Lead verify draft (ДО Notion/Gumroad)

Lead читает файлы, **не верит** MiMo self-assessment.

| # | Проверка | Как | Минимум |
|---|---|---|---|
| 1 | Базы | `spec.json` → `databases` length | ≥ 5 |
| 2 | Relations | sample_rows содержат relation-поля | да |
| 3 | user-guide | word count | ≥ 1200 |
| 4 | quality-report | Grade | A |
| 5 | listing | exists, не placeholder | да |
| 6 | price | spec vs gumroad_result | совпадает |

**Fail** → вернуть MiMo Coder, **не** запускать `notion_create`.

### Career OS (28.06)

| # | Результат |
|---|---|
| 1 | ✅ 6 баз |
| 2 | ✅ relations в sample_rows |
| 3 | ⚠️ ~1800 слов по report; файл ~1.9k слов — **OK** |
| 4 | ✅ Grade A |
| 5 | ✅ listing.md |
| 6 | ✅ $19 |

**Gate 0: PASS** — можно Playwright.

---

## Gate 1 — notion_create

```bash
python scripts/notion_create.py notion-developer-career-os
```

| # | Проверка |
|---|---|
| 1 | `notion_result.json` создан |
| 2 | 6 ключей в `databases` |
| 3 | Лог: `Linked N rows via relations`, N > 0 |

---

## Gate 2 — Designer

```bash
python scripts/pillow_pin.py notion-developer-career-os
```

| # | Проверка |
|---|---|
| 1 | `notion-cover.png` = **3000×1200 strip-only** (no cards) |
| 2 | `gumroad-thumb.png` exists |

---

## Gate 3 — setup_product (Chrome :9222)

```bash
python scripts/setup_product.py notion-developer-career-os
```

**Exit code MUST be 0.** Иначе STOP, смотреть `setup.log` (после Mechanic) / `debug_screenshots/`.

### Owner verify (обязательно)

| # | Notion | Gumroad |
|---|---|---|
| 1 | Cover **strip-only** (не gradient, не cards) | Thumb Direction D |
| 2 | Share → **Publish**, не private | Description с `notion.site` |
| 3 | Skill Count > 0 в Projects | Save changes нажато |
| 4 | 6 баз с sample data | user-guide в Content |

**Все ✅** → `# DONE notion-developer-career-os` в rebuild-queue.

---

## Что пошло не так (28.06)

- MiMo: `notion_create` + `pillow_pin` ✅
- Playwright: cover ❌, publish ❌ (`app.notion.com` остался)
- Gumroad thumb: ❌ (WARNING, скрипт не упал)
- MiMo поставил `# DONE` без Gate 3 — **Lead ошибка**

---

### Career OS Gate 2–3 (28.06 verify)

| # | Результат |
|---|---|
| Gate 2 | ✅ strip cover 3000×1200, thumb 1600×900 (Direction D) |
| Playwright | ✅ round 4 strip-only uploaded |
| json | ✅ `delicious-cucumber-254.notion.site`, Gumroad published |
| Owner visual | ✅ strip cover принят Owner |

**Gate 3: PASS** (28.06) — pilot #1 закрыт.
