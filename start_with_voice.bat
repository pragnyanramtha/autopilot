@echo off
REM Script to start both AI Brain (with voice) and Automation Engine

echo ========================================
echo Voice-Enabled AI Automation Assistant
echo ========================================
echo.
echo This script will start both components:
echo 1. AI Brain (with voice input support)
echo 2. Automation Engine (executes workflows)
echo.
echo IMPORTANT: Make sure you have set your GEMINI_API_KEY
echo Example: set GEMINI_API_KEY=your_key_here
echo.

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo WARNING: GEMINI_API_KEY is not set!
    echo Please set it first:
    echo    set GEMINI_API_KEY=your_api_key_here
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b
)

echo Starting Automation Engine in new window...
start "Automation Engine" cmd /k "cd /d %~dp0 && python -m automation_engine.main"

echo Waiting 2 seconds for engine to initialize...
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Starting AI Brain with Voice Input...
echo ========================================
echo.
echo Voice Commands:
echo   - Type 'voice' to enable voice mode
echo   - Say 'text mode' to switch back
echo   - Type 'test mic' to test microphone
echo   - Type 'help' for more info
echo.
python -m ai_brain.main

echo.
echo AI Brain stopped. Press any key to exit...
pause >nul
