@echo off
REM Start both AI Brain and Automation Engine in separate windows
echo ========================================
echo AI Automation Assistant - Full System
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
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo [OK] .env file found
echo.
echo Starting both components in separate windows...
echo.
echo 1. Automation Engine (will open in new window)
echo 2. AI Brain (will open in new window)
echo.
echo TIP: Close both windows to stop the system
echo ========================================
echo.

REM Start Automation Engine in new window
start "Automation Engine" cmd /k "call venv\Scripts\activate.bat && python -m automation_engine.main"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start AI Brain in new window
start "AI Brain" cmd /k "call venv\Scripts\activate.bat && python -m ai_brain.main"

echo.
echo [OK] Both components started!
echo.
echo - Automation Engine: Running in separate window
echo - AI Brain: Running in separate window
echo.
echo You can now give commands in the AI Brain window.
echo.
pause
