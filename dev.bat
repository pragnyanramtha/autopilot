@echo off
REM ========================================
REM   AI Automation Assistant - DEV MODE
REM   Developer Configuration Script
REM ========================================

REM ========================================
REM DEVELOPER CONFIGURATION
REM Edit these settings as needed
REM ========================================

REM AI Model Selection
REM Options: gemini-2.0-flash-exp (ultra-fast), gemini-2.5-flash, gemini-2.5-pro, gemini-1.5-flash, gemini-1.5-pro
SET DEV_ULTRA_FAST_MODEL=true
SET DEV_SIMPLE_MODEL=gemini-2.5-flash
SET DEV_COMPLEX_MODEL=gemini-2.5-pro

REM Temperature (0.0 - 1.0)
REM Lower = more focused, Higher = more creative
SET DEV_TEMPERATURE=0.7

REM Automation Settings
SET DEV_SAFETY_DELAY=100
SET DEV_DRY_RUN=false
SET DEV_VERBOSE=true
SET DEV_DEBUG_MODE=true

REM Safety Features
SET DEV_ENABLE_SAFETY_MONITOR=true
SET DEV_INTERRUPT_ON_MOUSE_MOVE=true

REM Social Media Strategy
REM Options: keyboard_shortcut, tab_navigation, smart
SET DEV_POSTING_STRATEGY=keyboard_shortcut

REM Voice Input
SET DEV_VOICE_ENABLED=true

REM Logging
SET DEV_LOG_LEVEL=DEBUG
SET DEV_LOG_FILE=dev_session.log

REM ========================================
REM END CONFIGURATION
REM ========================================

title AI Automation Assistant - DEVELOPER MODE
color 0E

echo.
echo ========================================
echo   AI AUTOMATION ASSISTANT
echo   DEVELOPER MODE
echo ========================================
echo.
echo [DEV] Configuration:
echo   Ultra-Fast Mode: %DEV_ULTRA_FAST_MODEL%
echo   Simple Model: %DEV_SIMPLE_MODEL%
echo   Complex Model: %DEV_COMPLEX_MODEL%
echo   Temperature: %DEV_TEMPERATURE%
echo   Dry Run: %DEV_DRY_RUN%
echo   Debug Mode: %DEV_DEBUG_MODE%
echo   Safety Delay: %DEV_SAFETY_DELAY%ms
echo   Posting Strategy: %DEV_POSTING_STRATEGY%
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

REM Create temporary dev config
echo [DEV] Creating temporary dev configuration...
python -c "import json; config = json.load(open('config.json')); config['gemini']['simple_model'] = '%DEV_SIMPLE_MODEL%'; config['gemini']['complex_model'] = '%DEV_COMPLEX_MODEL%'; config['gemini']['temperature'] = float('%DEV_TEMPERATURE%'); config['automation']['safety_delay_ms'] = int('%DEV_SAFETY_DELAY%'); config['automation']['enable_safety_monitor'] = '%DEV_ENABLE_SAFETY_MONITOR%' == 'true'; config['automation']['interrupt_on_mouse_move'] = '%DEV_INTERRUPT_ON_MOUSE_MOVE%' == 'true'; config['social_media']['posting_strategy'] = '%DEV_POSTING_STRATEGY%'; config['dev_mode'] = {'enabled': True, 'dry_run': '%DEV_DRY_RUN%' == 'true', 'verbose': '%DEV_VERBOSE%' == 'true', 'debug': '%DEV_DEBUG_MODE%' == 'true', 'log_level': '%DEV_LOG_LEVEL%', 'log_file': '%DEV_LOG_FILE%'}; json.dump(config, open('config.dev.json', 'w'), indent=2)"

if errorlevel 1 (
    echo [ERROR] Failed to create dev config!
    pause
    exit /b 1
)

echo [DEV] Starting in developer mode...
echo.

REM Activate and run with dev config
call venv\Scripts\activate
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Set environment variables for dev mode
SET DEV_MODE=1
SET CONFIG_FILE=config.dev.json
SET USE_ULTRA_FAST_MODEL=%DEV_ULTRA_FAST_MODEL%

REM Run with dev config
python run.py

REM Cleanup
if exist "config.dev.json" (
    echo.
    echo [DEV] Cleaning up temporary config...
    del config.dev.json
)

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start!
    echo.
    echo Troubleshooting:
    echo   1. Check your .env file has GEMINI_API_KEY
    echo   2. Verify model names are correct
    echo   3. Check logs in %DEV_LOG_FILE%
    echo.
    pause
)

echo.
echo [DEV] Session ended.
pause
