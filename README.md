# Gumroad Factory

Автономная фабрика цифровых продуктов для Gumroad.

**Продукты:** Notion Templates ($19–39) + AI Prompt Bundles ($19–29)

## Быстрый старт

### Запустить MiMo

Скопируй блок из `docs/team/agents/handoff/mimo.md` в новую сессию MiMo.
МиМо сам читает тренды, генерирует продукты и пишет листинги.

### Загрузить на Gumroad

1. Открой `products/ready/` — там готовые продукты
2. Открой `listings/<slug>.md` — там готовый текст листинга
3. Залей на Gumroad, перенеси папку в `products/published/`

## Пайплайн

```
TRENDS.md → queue/ → draft/ → [quality check] → ready/ → Gumroad → published/
```

## Агенты

| Агент | Запуск | Роль |
|-------|--------|------|
| MiMo | `handoff/mimo.md` | Генерирует продукты автономно |
| Lead | `@lead` в Cursor | Тренды, очередь, verify |
| Mechanic | `@mechanic` + тикет | Исправляет проблемы качества |

## Документация

- `docs/team/common/PROJECT_MAP.md` — карта проекта
- `docs/team/common/STATUS.md` — что сделано
- `research/TRENDS.md` — актуальные ниши
- `skills/NOTION_QUALITY.md` — чеклист качества
