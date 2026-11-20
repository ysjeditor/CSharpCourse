@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0환경설정.ps1" -Mode Launch
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" echo 문제가 계속되면 setup.bat을 실행해 환경을 검사하세요.
pause
exit /b %RESULT%
