@echo off
echo ============================================================
echo MOCK ACTION TESTING (No API Calls)
echo ============================================================
echo.
echo This will test automation protocols without:
echo   - Making API calls to Gemini
echo   - Moving the mouse or clicking
echo   - Typing on the keyboard
echo.
echo Perfect for testing protocol structure and execution flow!
echo.
echo ============================================================
echo.

python tests/test_with_mock_actions.py

echo.
echo ============================================================
echo Test complete!
echo ============================================================
pause
