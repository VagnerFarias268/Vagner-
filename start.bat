@echo off
REM Quick start script for Windows (without venv)

echo.
echo ========================================
echo   Starting Vagner Sales Agent
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and configure it
    pause
    exit /b 1
)

echo Starting server...
echo Server will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Press CTRL+C to stop
echo.

REM Start with uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause

