@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0환경설정.ps1" -Mode Setup
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
