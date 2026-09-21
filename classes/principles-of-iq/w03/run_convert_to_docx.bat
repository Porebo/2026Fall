@echo off
setlocal
cd /d "%~dp0"

powershell.exe -ExecutionPolicy Bypass -File "%~dp0convert_to_docx.ps1"

if errorlevel 1 (
    echo.
    echo Conversion failed.
) else (
    echo.
    echo Conversion completed successfully.
)

pause
endlocal
