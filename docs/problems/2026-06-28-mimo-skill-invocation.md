# Тикет: добавить вызов скиллов в MIMO_FACTORY.md

**Дата:** 2026-06-28  
**Автор:** Lead  
**Статус:** closed  
**Исполнитель:** Mechanic (правка `.mimocode/MIMO_FACTORY.md`)

---

## Проблема

В `MIMO_FACTORY.md` три скилла указаны как "читай файл" — вместо запуска через `/`.
MiMo читает их пассивно, не переходит в режим скилла, не применяет принципы.

| Скилл | Где в MIMO_FACTORY.md | Как сейчас | Как должно быть |
|---|---|---|---|
| `copywriting` | Coder Mode (listing.md) | не упоминается | `/copywriting` |
| `marketing-psychology` | Coder Mode (listing.md) | не упоминается | `/marketing-psychology` |
| `design-lebedev` | Designer Mode | `Читай C:/Users/hramo/all skill/design_lebedev.md` | `/design-lebedev` |

Все три — полноценные SKILL.md с `name:` в заголовке. Запускаются через `/`.

---

## Фикс 1 — Coder Mode (listing.md + user-guide.md)

Найти секцию `## Coder Mode — обязательные файлы`  
Добавить ПЕРЕД списком файлов:

```markdown
### Перед написанием listing.md и user-guide.md — запусти скиллы:

/copywriting
Применяй: Benefits > Features, specificity, AIDA, Jobs-to-be-Done, CTA формула.

/marketing-psychology
Применяй: Loss aversion, Anchoring, Present bias, Contrast before/after, Social proof.

Полный гайд → `skills/MIMO_SKILL.md` раздел "4. ТЕКСТ — обязательные скиллы"
Без этих скиллов listing = Grade B (feature dump).
```

---

## Фикс 2 — Designer Mode

Найти секцию `## Designer Mode — скилл`  
Заменить:

```markdown
Читай:
1. `C:/Users/hramo/all skill/design_lebedev.md`
2. `skills/COVER_DIRECTIONS.md`
3. `skills/DESIGNER_SKILL.md`
```

На:

```markdown
Запусти скилл:

/design-lebedev
Применяй: function over form, distinctiveness, избегай AI-дефолты, типографика.

Затем читай для контекста:
- `skills/COVER_DIRECTIONS.md` — Direction D, System Cards, no emoji
- `skills/DESIGNER_SKILL.md` — параметры pillow_pin.py
```

---

## Проверка после фикса

1. Запустить MiMo на тестовую нишу (Developer Career OS rebuild — TASK-015)
2. В listing.md: anchoring + loss aversion + Job-to-be-Done headline
3. user-guide.md: 1200+ слов
4. Notion cover: Direction D, без AI-дефолтов
5. Lead делает verify

---

## Приоритет: HIGH

Влияет на качество текста и дизайна всех будущих продуктов.

---

## Решено (Lead verify 28.06)

**Mechanic:** `.mimocode/MIMO_FACTORY.md` — оба фикса применены ✅  
**Lead:** синхронизированы `skills/DESIGNER_SKILL.md`, `skills/COVER_DIRECTIONS.md` → `/design-lebedev`  
**Следующий шаг:** MiMo TASK-015 (Developer Career OS rebuild) — проверка качества текста на практике
