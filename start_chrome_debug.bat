@echo off
cd /d "C:\Users\hramo\gumroad"
set CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe
set CHROME_PROFILE=C:\Users\hramo\gumroad\.chrome-factory

if not exist "%CHROME_PROFILE%" mkdir "%CHROME_PROFILE%"

powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:9222/json/version' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel%==0 (
  echo Chrome factory: OK port 9222
  goto :done
)

echo Starting Chrome factory profile...
start "" "%CHROME%" --remote-debugging-port=9222 --user-data-dir="%CHROME_PROFILE%" --no-first-run --no-default-browser-check https://app.gumroad.com/products
timeout /t 6 /nobreak >nul
echo Debug port: http://localhost:9222

:done
