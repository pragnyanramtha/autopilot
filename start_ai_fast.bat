@echo off
REM Quick launcher for AI Brain with Ultra-Fast Model
title AI Brain - Ultra Fast Mode
color 0B

echo.
echo ========================================
echo   AI Automation Assistant
echo   ULTRA FAST MODE (gemini-2.0-flash-exp)
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
    echo Get your key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo [OK] .env file found
echo.
echo Starting AI Brain in ULTRA FAST mode...
echo Using model: gemini-2.0-flash-exp
echo.
echo TIP: Type 'help' for available commands
echo      Press Ctrl+C to exit
echo ========================================
echo.

REM Set environment variable for ultra-fast mode
SET USE_ULTRA_FAST_MODEL=true

REM Activate venv and run
call venv\Scripts\activate
python -m ai_brain.main

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start AI Brain!
    echo.
    echo Common issues:
    echo   1. Missing dependencies - run: pip install -r requirements.txt
    echo   2. Invalid API key - check your .env file
    echo   3. Python version - requires Python 3.10+
    echo.
    pause
)
