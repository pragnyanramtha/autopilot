@echo off

echo Starting backend server...
start "Backend" cmd /c "call venv\Scripts\activate && python server.py"

echo Starting frontend development server...
start "Frontend" cmd /c "cd frontend && npm start"

echo Both servers are starting in separate windows.
