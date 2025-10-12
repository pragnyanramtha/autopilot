@echo off
REM Unified Launcher - Single Terminal
title AI Automation Assistant
color 0A

echo.
echo ========================================
echo   AI Automation Assistant
echo   Unified Interface
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
    echo Create .env with: GEMINI_API_KEY=your_key
    pause
    exit /b 1
)

echo Starting...
echo.

REM Activate and run
call venv\Scripts\activate
python run.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start!
    echo.
    echo Install voice support (optional):
    echo   pip install SpeechRecognition pyaudio
    echo.
    pause
)
