@echo off
echo Killing Chrome...
taskkill /f /im chrome.exe >nul 2>&1
ping -n 3 localhost >nul

echo Removing locks...
del /f /q "%LOCALAPPDATA%\Google\Chrome\User Data\SingletonLock" >nul 2>&1
del /f /q "%LOCALAPPDATA%\Google\Chrome\User Data\SingletonCookie" >nul 2>&1
del /f /q "%LOCALAPPDATA%\Google\Chrome\User Data\SingletonSocket" >nul 2>&1

echo Starting Chrome with debug port 9222...
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data" --profile-directory=Default --no-first-run

echo Done.
