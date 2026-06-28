@echo off
cd /d "C:\Users\hramo\gumroad"
chcp 65001 >nul 2>&1
title RodeShop - Setup Product

echo.
echo  ==========================================
echo   RodeShop - Setup Product
echo  ==========================================
echo.

:: Проверяем Chrome
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:9222/json/version' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel%==1 (
  echo  Chrome не запущен на порту 9222.
  echo  Сначала запусти: Запустить фабрику.bat
  echo.
  pause
  exit /b 1
)
echo  Chrome: OK
echo.

:: Ищем продукт - сначала в draft без notion_result (не опубликован)
set SLUG=
for /f "delims=" %%d in ('dir /b /ad "products\draft" 2^>nul') do (
    if exist "products\draft\%%d\spec.json" (
        if not exist "products\draft\%%d\notion_result.json" (
            set SLUG=%%d
        )
    )
)

:: Если не нашли неопубликованный - берем любой из draft
if "%SLUG%"=="" (
    for /f "delims=" %%d in ('dir /b /ad "products\draft" 2^>nul') do (
        if exist "products\draft\%%d\spec.json" (
            set SLUG=%%d
        )
    )
)

if "%SLUG%"=="" (
    echo  Нет продуктов в products\draft\
    echo  Сначала запусти MiMo в Cursor чтобы сгенерировать продукт.
    echo.
    pause
    exit /b
)

echo  Найден продукт: %SLUG%
echo.
set /p CONFIRM=Запустить для "%SLUG%"? [Enter = да / введи другой slug]:

if not "%CONFIRM%"=="" set SLUG=%CONFIRM%

echo.
echo  Запускаем setup_product.py для: %SLUG%
echo.

python scripts\setup_product.py %SLUG%

echo.
echo  ==========================================
echo   Готово! Проверь Gumroad и Notion.
echo  ==========================================
echo.
pause
