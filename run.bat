@echo off
REM ForgeML Windows Batch Runner
REM Usage: run.bat [command]

if "%1"=="" (
    echo 🔥 ForgeML - Starting Development Server...
    python run.py dev
) else (
    python run.py %1
)