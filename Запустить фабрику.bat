@echo off
setlocal EnableDelayedExpansion
cd /d "C:\Users\hramo\gumroad"
title RodeShop Factory

set PYTHON=C:\Users\hramo\AppData\Local\Programs\Python\Python311\python.exe
set PYTHONIOENCODING=utf-8
set LOG=factory.log
set CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe
set CHROME_PROFILE=C:\Users\hramo\gumroad\.chrome-factory

if not exist "!CHROME_PROFILE!" mkdir "!CHROME_PROFILE!"

call :log "=========================================="
call :log " RodeShop Factory - %date% %time%"
call :log "=========================================="

if not exist "!PYTHON!" (
    call :log "FAIL: Python not found"
    goto :end
)

:: ── [1/3] Chrome on port 9222 ────────────────────────────────
call :log "[1/3] Chrome factory profile..."

curl -s --max-time 2 http://localhost:9222/json/version >nul 2>&1
if !errorlevel! EQU 0 goto :chrome_ok

call :log "Starting Chrome (profile: .chrome-factory, port 9222)..."
if exist "!CHROME_PROFILE!\SingletonLock" del /f /q "!CHROME_PROFILE!\SingletonLock" >nul 2>&1
if exist "!CHROME_PROFILE!\SingletonSocket" del /f /q "!CHROME_PROFILE!\SingletonSocket" >nul 2>&1
start "" "!CHROME!" --remote-debugging-port=9222 --user-data-dir="!CHROME_PROFILE!" --no-first-run --no-default-browser-check https://www.notion.so

call :log "Waiting for Chrome to start..."
timeout /t 6 /nobreak >nul

set /a WAIT=0
:wait_chrome
curl -s --max-time 2 http://localhost:9222/json/version >nul 2>&1
if !errorlevel! EQU 0 goto :chrome_ok
set /a WAIT+=1
if !WAIT! LSS 15 (
    timeout /t 2 /nobreak >nul
    goto :wait_chrome
)

call :log "FAIL: Chrome not on port 9222 after 30 sec"
call :log "Try: close ALL Chrome windows, then re-run."
goto :end

:chrome_ok
call :log "Chrome: OK port 9222"

:: ── [2/3] Process existing queue ────────────────────────────
call :log "[2/3] Checking product queue..."

set SLUG=

:: Priority 1: spec.json exists but notion_result.json missing
for /f "delims=" %%D in ('dir /b /ad "products\draft" 2^>nul') do (
    if exist "products\draft\%%D\spec.json" (
        if not exist "products\draft\%%D\notion_result.json" (
            if "!SLUG!"=="" set SLUG=%%D
        )
    )
)

:: Priority 2: gumroad_result.json has published: false
if "!SLUG!"=="" (
    for /f "delims=" %%D in ('dir /b /ad "products\draft" 2^>nul') do (
        if exist "products\draft\%%D\spec.json" (
            if exist "products\draft\%%D\gumroad_result.json" (
                findstr /c:"\"published\": false" "products\draft\%%D\gumroad_result.json" >nul 2>&1
                if !errorlevel! EQU 0 (
                    if "!SLUG!"=="" set SLUG=%%D
                )
            )
        )
    )
)

if "!SLUG!"=="" (
    call :log "Queue empty — no pending products."
) else (
    call :log "Found: !SLUG! — running setup_product.py..."
    "!PYTHON!" scripts\setup_product.py !SLUG!
    set RESULT=!errorlevel!
    if !RESULT! EQU 0 (
        call :log "DONE: !SLUG!"
    ) else (
        call :log "ERROR code !RESULT! for !SLUG!"
    )
)

:: ── [3/3] Launch MiMo loop (rebuild wave or normal) ───────────
set REBUILD_MODE=normal
for /f %%A in ('"!PYTHON!" scripts\count_rebuild_queue.py 2^>nul') do set QUEUE_PENDING=%%A

if not "!QUEUE_PENDING!"=="" if not "!QUEUE_PENDING!"=="0" (
    set REBUILD_MODE=rebuild
    call :log "Rebuild Wave active: !QUEUE_PENDING! slug(s) in queue"
    call :log "Launching rebuild_loop.bat..."
    start "MiMo Rebuild Wave" cmd /k ""%~dp0rebuild_loop.bat""
) else (
    call :log "[3/3] Launching MiMo autonomous factory..."
    call :log "MiMo will generate products in a loop — Chrome stays open for Playwright."
    start "MiMo Factory" cmd /k ""%~dp0mimo_loop.bat""
)

call :log "MiMo window opened."
call :log "Mode: !REBUILD_MODE!"
call :log "Factory is running. You can close THIS window."

goto :end

:log
echo %~1
echo %~1 >> "%LOG%"
exit /b 0

:end
call :log "Main launcher finished."
echo.
echo  Chrome : port 9222 (factory profile)
echo  MiMo   : runs in separate window
echo  Log    : %CD%\factory.log
echo.
echo  You can close this window now.
echo.
timeout /t 10 /nobreak >nul
