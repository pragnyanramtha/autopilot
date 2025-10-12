@echo off
REM Quick launcher for AI Brain only
title AI Brain - Quick Start
color 0B

echo.
echo ========================================
echo   AI Automation Assistant
echo   AI Brain Only
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
echo Starting AI Brain...
echo.
echo TIP: Type 'help' for available commands
echo      Press Ctrl+C to exit
echo ========================================
echo.

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
