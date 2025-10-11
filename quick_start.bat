@echo off
REM Quick Start - Interactive launcher with checks
title AI Automation Assistant - Quick Start
color 0A

:MENU
cls
echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║     AI AUTOMATION ASSISTANT - QUICK START             ║
echo  ╚════════════════════════════════════════════════════════╝
echo.

REM Check venv
if exist "venv\Scripts\python.exe" (
    echo  [√] Virtual environment: OK
) else (
    echo  [X] Virtual environment: NOT FOUND
    echo      Run setup_venv.bat first!
    echo.
    pause
    exit /b 1
)

REM Check .env
if exist ".env" (
    echo  [√] .env file: OK
) else (
    echo  [X] .env file: NOT FOUND
    echo      Create .env with: GEMINI_API_KEY=your_key
    echo.
    pause
    exit /b 1
)

REM Check API key
findstr /C:"GEMINI_API_KEY=" .env >nul
if errorlevel 1 (
    echo  [X] API key: NOT SET
    echo      Add GEMINI_API_KEY to .env file
    echo.
    pause
    exit /b 1
) else (
    echo  [√] API key: SET
)

echo.
echo  ════════════════════════════════════════════════════════
echo.
echo  What would you like to do?
echo.
echo  [1] Start AI Brain only
echo  [2] Start Automation Engine only (DRY-RUN)
echo  [3] Start Automation Engine only (LIVE)
echo  [4] Start BOTH (Full System)
echo  [5] Run Tests
echo  [6] Check System Status
echo  [0] Exit
echo.
echo  ════════════════════════════════════════════════════════
echo.

set /p choice="Enter your choice (0-6): "

if "%choice%"=="1" goto START_BRAIN
if "%choice%"=="2" goto START_ENGINE_DRY
if "%choice%"=="3" goto START_ENGINE_LIVE
if "%choice%"=="4" goto START_BOTH
if "%choice%"=="5" goto RUN_TESTS
if "%choice%"=="6" goto CHECK_STATUS
if "%choice%"=="0" goto EXIT
goto MENU

:START_BRAIN
cls
echo Starting AI Brain...
call start_ai_brain.bat
goto MENU

:START_ENGINE_DRY
cls
echo Starting Automation Engine (DRY-RUN mode)...
call venv\Scripts\activate.bat
python -m automation_engine.main --dry-run
pause
goto MENU

:START_ENGINE_LIVE
cls
echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║                    WARNING!                            ║
echo  ║  This will control your mouse and keyboard!           ║
echo  ║  Press Ctrl+C to stop at any time.                    ║
echo  ╚════════════════════════════════════════════════════════╝
echo.
pause
call venv\Scripts\activate.bat
python -m automation_engine.main
pause
goto MENU

:START_BOTH
cls
echo Starting Full System...
call start_both.bat
goto MENU

:RUN_TESTS
cls
echo Running tests...
call venv\Scripts\activate.bat
python test_complex_workflows.py
echo.
pause
goto MENU

:CHECK_STATUS
cls
echo.
echo  ════════════════════════════════════════════════════════
echo  SYSTEM STATUS CHECK
echo  ════════════════════════════════════════════════════════
echo.

REM Check Python version
call venv\Scripts\activate.bat
python --version
echo.

REM Check installed packages
echo  Checking key packages...
python -c "import google.generativeai; print('  [√] google-generativeai')" 2>nul || echo   [X] google-generativeai
python -c "import pyautogui; print('  [√] pyautogui')" 2>nul || echo   [X] pyautogui
python -c "import mss; print('  [√] mss')" 2>nul || echo   [X] mss
python -c "import PIL; print('  [√] pillow')" 2>nul || echo   [X] pillow
python -c "import rich; print('  [√] rich')" 2>nul || echo   [X] rich
python -c "import dotenv; print('  [√] python-dotenv')" 2>nul || echo   [X] python-dotenv
echo.

REM Check API key
echo  Checking API key...
python -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('GEMINI_API_KEY'); print('  [√] API key loaded (' + key[:20] + '...)') if key else print('  [X] API key not found')"
echo.

echo  ════════════════════════════════════════════════════════
echo.
pause
goto MENU

:EXIT
cls
echo.
echo  Thank you for using AI Automation Assistant!
echo.
timeout /t 2 /nobreak >nul
exit /b 0
