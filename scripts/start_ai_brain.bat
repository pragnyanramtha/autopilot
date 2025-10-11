@echo off
REM AI Brain Launcher - Checks venv and starts the AI Brain
echo ========================================
echo AI Automation Assistant - AI Brain
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

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo.
    echo Please create a .env file with your Gemini API key:
    echo GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

REM Check if API key is set in .env
findstr /C:"GEMINI_API_KEY=" .env >nul
if errorlevel 1 (
    echo [WARNING] GEMINI_API_KEY not found in .env file!
    echo.
    echo Please add your Gemini API key to .env file:
    echo GEMINI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo [OK] .env file found
echo.
echo Starting AI Brain...
echo.
echo TIP: Press Ctrl+C to stop the AI Brain
echo ========================================
echo.

REM Activate venv and run AI Brain
call venv\Scripts\activate.bat
python -m ai_brain.main

REM If python exits with error
if errorlevel 1 (
    echo.
    echo [ERROR] AI Brain failed to start!
    echo.
    echo Common issues:
    echo 1. Missing dependencies - run: pip install -r requirements.txt
    echo 2. Invalid API key - check your .env file
    echo 3. Python version - requires Python 3.10+
    echo.
    pause
)
