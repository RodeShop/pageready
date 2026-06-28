@echo off
echo. > "%~dp0STOP"
echo.
echo  Сигнал отправлен. MiMo завершит текущий цикл и остановится.
echo  Окно фабрики закроется само после завершения.
echo.
timeout /t 3 /nobreak >nul
