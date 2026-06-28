# [TICKET] rebuild_loop не стартует — bat ломает Python -c

**Приоритет:** critical  
**Статус:** closed  
**Исполнитель:** Mechanic

---

## Симптом (Owner verify 28.06)

`Запустить фабрику.bat` → `factory.log`:
```
Found: notion-developer-career-os — running setup_product.py...
DONE: notion-developer-career-os
Mode: normal          ← rebuild_loop НЕ запустился
```

`rebuild-queue.txt` — **0 строк `# DONE`**, все 7 pending.  
MiMo wave не работал.

---

## Root cause

`Запустить фабрику.bat` строка ~97:

```bat
for /f %%A in ('"!PYTHON!" -c "... startswith('#')) if p.exists() ..."') do set QUEUE_PENDING=%%A
```

**`)` в `startswith('#')` закрывает `for /f ... in ('`** — Python не выполняется, `QUEUE_PENDING` пуст → запускается `mimo_loop.bat` вместо `rebuild_loop.bat`.

---

## Фикс

1. `scripts/count_rebuild_queue.py` — печатает число pending slug
2. В `Запустить фабрику.bat` и `rebuild_loop.bat`:
   ```bat
   for /f %%A in ('"!PYTHON!" scripts\count_rebuild_queue.py') do set QUEUE_PENDING=%%A
   ```
3. Убрать inline `python -c` с `#` и скобками

---

## Verify

```
Запустить фабрику.bat
factory.log → Mode: rebuild
Окно "MiMo Rebuild Wave" открыто
```

---

## Решено (Mechanic, 28.06)

- `scripts/count_rebuild_queue.py` — выводит кол-во pending строк (без `#`)
- `Запустить фабрику.bat` line 97: `python -c "...startswith('#')..."` → `scripts\count_rebuild_queue.py`
- `rebuild_loop.bat` line 22: то же самое

---

## Workaround (Owner, до фикса)

```
1. start_chrome_debug.bat
2. Двойной клик rebuild_loop.bat
```

Не `Запустить фабрику.bat` — он сейчас ломает выбор режима.
