@echo off
setlocal
cd /d "%~dp0"
title MiMo Factory - RodeShop
set PYTHONIOENCODING=utf-8

echo.
echo  ===== MiMo Factory Loop =====
echo  Dir: %CD%
echo  Чтобы остановить: создай файл STOP в папке gumroad
echo  (или нажми Ctrl+C — но только между циклами)
echo.

:loop
:: Проверяем стоп-сигнал перед каждым циклом
if exist "STOP" (
    echo.
    echo  ========================================
    echo  [%time%] Файл STOP обнаружен.
    echo  Фабрика остановлена чисто.
    echo  Удали файл STOP чтобы запустить снова.
    echo  ========================================
    echo.
    del /f /q "STOP"
    goto :end
)

echo [%time%] Starting MiMo cycle...
mimo run "Read .mimocode/MIMO_FACTORY.md for full instructions. Then: 1) Check products/draft/ for any incomplete product (has spec.json but missing notion_result.json or gumroad_result.json) — if found, finish it first with setup_product.py. 2) Only if no incomplete products, pick the next niche from research/TRENDS.md and generate a new product. Work autonomously."
echo.
echo [%time%] MiMo cycle done.

:: Снова проверяем STOP после цикла (мог появиться во время работы)
if exist "STOP" (
    echo.
    echo  ========================================
    echo  Файл STOP обнаружен — выходим чисто.
    echo  ========================================
    del /f /q "STOP"
    goto :end
)

echo  Restarting in 15 seconds... (создай файл STOP чтобы остановить)
timeout /t 15 /nobreak >nul
goto :loop

:end
echo  Можно закрыть Chrome.
pause
