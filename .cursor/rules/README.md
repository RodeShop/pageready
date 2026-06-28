# Cursor Rules — Gumroad Factory

## Роли (вызов в Cursor чате)

| Роль | Файл | В чате | Зона |
|------|------|--------|------|
| Owner | `owner.mdc` | `@owner` | PROJECT_MAP, STATUS, публикация |
| Lead | `lead.mdc` | `@lead` | TRENDS, queue, TASK.md, verify |
| Mechanic | `mechanic.mdc` | `@mechanic` | scripts/ по тикету |

## Всегда активны (alwaysApply: true)

| Файл | Что делает |
|------|-----------|
| `economy.mdc` | Лимиты hot-файлов, порядок чтения, таблица исполнителей |
| `lead-no-code.mdc` | Lead не трогает scripts/, .mimocode/, *.py, *.bat |
| `structure.mdc` | Канон папок, лимиты файлов, ответственность Lead |

## Контекстные гарды

| Файл | Когда срабатывает |
|------|------------------|
| `docs-guard.mdc` | При работе с docs/** |
| `code-guard.mdc` | При работе с scripts/, *.py, *.bat |

---

**MiMo (фабрика):** `.mimocode/MIMO_FACTORY.md` — запускается через `mimo_loop.bat`, не через Cursor.
MiMo — не роль Cursor. Его инструктирует Lead через `docs/team/active/TASK.md`.
