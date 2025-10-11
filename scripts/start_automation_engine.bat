@echo off
REM Automation Engine Launcher - Checks venv and starts the Automation Engine
echo ========================================
echo AI Automation Assistant - Automation Engine
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup_venv.bat first to create the virtual environment.
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo.
echo Starting Automation Engine...
echo.
echo TIP: Press Ctrl+C to stop the Automation Engine
echo WARNING: This will control your mouse and keyboard!
echo ========================================
echo.

REM Ask for dry-run mode
set /p DRYRUN="Run in DRY-RUN mode (safe testing)? [Y/n]: "
if /i "%DRYRUN%"=="n" (
    echo.
    echo [WARNING] Running in LIVE mode - will control your computer!
    echo Press Ctrl+C now to cancel, or
    pause
    call venv\Scripts\activate.bat
    python -m automation_engine.main
) else (
    echo.
    echo [SAFE] Running in DRY-RUN mode - will simulate actions only
    echo.
    call venv\Scripts\activate.bat
    python -m automation_engine.main --dry-run
)

REM If python exits with error
if errorlevel 1 (
    echo.
    echo [ERROR] Automation Engine failed to start!
    echo.
    echo Common issues:
    echo 1. Missing dependencies - run: pip install -r requirements.txt
    echo 2. Python version - requires Python 3.10+
    echo.
    pause
)
