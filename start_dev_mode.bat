@echo off
REM Developer Mode - Starts both AI Brain and Automation Engine with verbose output
title AI Automation - Developer Mode Launcher
color 0E

echo.
echo ========================================
echo   AI AUTOMATION ASSISTANT
echo   DEVELOPER MODE
echo ========================================
echo.

REM Check venv
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Run: setup_venv.bat
    pause
    exit /b 1
)

REM Check .env
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo.
    echo Create a .env file with your Gemini API key:
    echo GEMINI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo [OK] .env file found
echo.
echo Starting Developer Mode...
echo.
echo This will open TWO windows:
echo   1. Automation Engine (LEFT) - Shows execution details
echo   2. AI Brain (RIGHT) - Your command interface
echo.
echo TIP: Arrange windows side-by-side to see both
echo.
pause

REM Start Automation Engine in new window (LEFT side)
echo Starting Automation Engine...
start "Automation Engine [DEV]" cmd /k "title Automation Engine [DEV] && color 0A && call venv\Scripts\activate && echo ============================================================ && echo   AUTOMATION ENGINE - DEVELOPER MODE && echo ============================================================ && echo. && echo Registered actions will be shown below... && echo Press Ctrl+C to stop && echo ============================================================ && echo. && python -m automation_engine.main"

REM Wait a moment for automation engine to start
timeout /t 3 /nobreak >nul

REM Start AI Brain in new window (RIGHT side)
echo Starting AI Brain...
start "AI Brain [DEV]" cmd /k "title AI Brain [DEV] && color 0B && SET USE_ULTRA_FAST_MODEL=true && call venv\Scripts\activate && echo ============================================================ && echo   AI BRAIN - DEVELOPER MODE (Ultra Fast) && echo ============================================================ && echo. && echo Using ultra-fast models (no pro in dev mode) && echo. && echo TIP: Try simple commands first: && echo   - search for pragnyan ramtha && echo   - type hello world && echo   - click at 500 300 && echo. && echo ============================================================ && echo. && python -m ai_brain.main"

echo.
echo ============================================================
echo   DEVELOPER MODE STARTED
echo ============================================================
echo.
echo Two windows have been opened:
echo   1. Automation Engine - Shows what's being executed
echo   2. AI Brain - Where you give commands
echo.
echo Arrange them side-by-side to see the full workflow!
echo.
echo To stop: Close both windows or press Ctrl+C in each
echo.
echo ============================================================
echo.
pause
