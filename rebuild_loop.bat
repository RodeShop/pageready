@echo off
setlocal
cd /d "%~dp0"
title MiMo Rebuild Wave - RodeShop
set PYTHONIOENCODING=utf-8
set PYTHON=C:\Users\hramo\AppData\Local\Programs\Python\Python311\python.exe

echo.
echo  ===== Rebuild Wave Loop =====
echo  Queue: docs\team\active\rebuild-queue.txt
echo  STOP: создай файл STOP в папке gumroad
echo.

:loop
if exist "STOP" (
    echo [%time%] STOP — выход.
    del /f /q "STOP"
    goto :end
)

:: Пустая очередь?
for /f %%A in ('"%PYTHON%" scripts\count_rebuild_queue.py 2^>nul') do set PENDING=%%A
if "%PENDING%"=="0" (
    echo [%time%] Rebuild queue empty — wave complete.
    goto :end
)

echo [%time%] Rebuild cycle — pending: %PENDING%
mimo run "REBUILD WAVE MODE. Read first: docs/team/active/rebuild-queue.txt, docs/team/active/TASK.md, .mimocode/MIMO_FACTORY.md.

RULES:
1. Process slugs IN FILE ORDER. Skip lines starting with #.
2. Pick the FIRST uncommented slug.
3. Full pipeline per slug: Coder (5+ DB, relations in sample_rows, /copywriting, /marketing-psychology, user-guide 1200+) -^> Designer (/design-lebedev, pillow_pin) -^> python scripts/setup_product.py ^<slug^>.
4. After setup_product SUCCESS: edit rebuild-queue.txt — prefix that slug line with '# DONE '.
5. IMMEDIATELY start the NEXT pending slug in the SAME session. Use /compact only if context full.
6. Do NOT read TRENDS.md. Do NOT create new niches until queue is all # DONE.
7. Chrome :9222 required for setup_product.

If blocked, write reason to docs/team/common/STATUS.md and stop."

echo [%time%] Cycle done.
if exist "STOP" (
    del /f /q "STOP"
    goto :end
)

echo  Next slug in 5 sec... (STOP to exit)
timeout /t 5 /nobreak >nul
goto :loop

:end
echo  Rebuild loop finished.
pause
