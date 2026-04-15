@echo off
:: Reset-GPU.bat — Launch the GPU reset script as Administrator
:: Double-click this file or run from any terminal.

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath 'powershell.exe' -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0Reset-GPU.ps1\"'"
    exit /b
)

:: Already admin — run directly
powershell -ExecutionPolicy Bypass -File "%~dp0Reset-GPU.ps1"
pause
