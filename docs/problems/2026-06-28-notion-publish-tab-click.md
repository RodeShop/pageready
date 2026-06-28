# [TICKET] Notion Publish tab — кнопка Publish не жмётся

**Приоритет:** high · **блокер pilot**  
**Статус:** closed (round 3)  
**Исполнитель:** Mechanic

---

## Симптом (pilot 28.06)

```
Switched to Publish tab
ERROR: No notion.site URL found
FATAL: exit 1
```

Cover upload **OK** в логе, Owner видит **gradient + старая иконка** — возможно false positive.  
Publish **FAIL**. Gumroad **не дошли** (fail loud — намеренно).

---

## Гипотеза

`button:has-text("Publish")` матчит **tab**, не action button.  
Или нужен второй клик «Publish to web» / confirm после tab.

---

## Фикс (`playwright_notion.py` → `publish_as_template`)

1. После Publish tab — исключить `[role="tab"]` из селекторов
2. Ждать появления `notion.site` в input (poll 15s)
3. Скрин `publish_no_public_url` — уже есть
4. Опционально: клик «Site settings» / duplicate toggle до extract URL

---

## Verify

```bash
python scripts/playwright_notion.py notion-developer-career-os
# Got public URL: https://....notion.site/...
# exit 0
```

---

## Owner evidence 28.06

- Notion: gradient cover, не Direction D 1920×800
- Share: «Only people invited»
- Gumroad: draft exists, thumb не залит (`published: false`)

**НЕ удалять** Notion page / Gumroad product — json на месте.

---

## Round 1 (Mechanic) — partial ✅

Publish action button + duplicate toggle — **кликаются** (Lead verify 28.06).

## Round 2 — блокер

После Publish в DOM **15s poll** не находит `notion.site` → exit 1.

```
Clicked Publish action button (page is now public)
Enabled "Allow duplicate as template"
ERROR: No notion.site URL found
```

**Fix:** искать URL в Copy link / `data-testid` / clipboard; расширить poll; скрин `publish_no_public_url`.

Cover: `[0] Cover button not found` на new tab — отдельно.

---

## Owner UI hint (28.06)

Скрипт, похоже, не тот таб/контрол:

1. Вкладка **Share** (не Publish?)
2. **General access** → сейчас «Only people invited»
3. Dropdown → **Anyone with the link** (или аналог)

Mechanic: проверить актуальный Notion UI — возможно нужен **Publish tab** + duplicate toggle, а не Share dropdown. Зафиксировать правильный flow в скрипте.

---

## Round 3 — Owner screenshot

Скрипт открывает **Publish tab** → «Publish to web» → синяя кнопка **Publish** внизу **ещё видна** = страница **не опубликована**.

Скрипт думает что кликнул (`Clicked Publish action button`), но UI остаётся на pre-publish.

**Fix:** кликать **синюю CTA** в panel «Publish to web» (scope dialog/modal), не tab. После клика — ждать Unpublished→Published / появление URL / «Allow duplicate as template».

---

## FAQ Owner: invited vs anyone — для Gumroad

**Покупателей по email не приглашаем** — так не масштабируется.

| Режим | Для продажи |
|-------|-------------|
| Only people invited | ❌ каждому buyer вручную email |
| Anyone with the link (Share) | ⚠️ кто **знает ссылку** — открывает. Ссылку даём **только в купленном файле** (user-guide) |
| **Publish** + duplicate as template | ✅ стандарт: buyer жмёт Duplicate → копия в **его** workspace |

**Покупка ≠ invite.** Buyer получает ссылку из Gumroad (файл после оплаты) → duplicate template. Без покупки ссылки нет — если не светишь её в **публичном** описании листинга.

**Важно:** `set_template_url` пишет link в Gumroad description — если description виден до покупки, link утекает. Link лучше только в **user-guide.md** (Content tab). Lead: проверить pipeline позже.

---

## Связано
