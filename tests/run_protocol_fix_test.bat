@echo off
REM Test the protocol generator fix
echo Testing Protocol Generator Fix...
echo.

REM Check venv
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Run: setup_venv.bat
    pause
    exit /b 1
)

REM Activate and run test
call venv\Scripts\activate
python tests/test_protocol_generator_fix.py

if errorlevel 1 (
    echo.
    echo [ERROR] Test failed!
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCESS] All tests passed!
    pause
)
