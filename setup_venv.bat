@echo off
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat
echo To run tests, activate venv first, then run: python test_executor.py
