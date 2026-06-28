@echo off
cd /d "C:\Users\hramo\gumroad"

echo.
echo  RodeShop - Setup Product
echo  ========================
echo.

:: Step 1: Start Chrome with debug port
echo  Step 1: Starting Chrome with debug port...
call start_chrome_debug.bat
echo.

:: Step 2: Find latest draft
set SLUG=
for /f "delims=" %%d in ('dir /b /ad "products\draft" 2^>nul') do set SLUG=%%d

if "%SLUG%"=="" (
    echo  No products found in products\draft\
    echo  Run MiMo first to generate a product.
    pause
    exit /b 1
)

echo  Found product: %SLUG%
echo.
set /p CONFIRM=Press Enter to run setup for "%SLUG%" (or type a different slug):

if not "%CONFIRM%"=="" set SLUG=%CONFIRM%

echo.
echo  Running setup for: %SLUG%
echo.

C:\Users\hramo\AppData\Local\Programs\Python\Python311\python.exe scripts\setup_product.py %SLUG%

echo.
pause
