@echo off
setlocal
cd /d "%~dp0"
cls

powershell.exe -ExecutionPolicy Bypass -File "%~dp0student_grades_examination.ps1" 2>&1 | clip

if errorlevel 1 (
    echo.
    echo Examination failed.
) else (
    echo.
    echo Examination completed. Results copied to the clipboard.
)

pause
endlocal
