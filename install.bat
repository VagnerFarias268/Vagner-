@echo off
REM Installation script for Windows

echo.
echo ========================================
echo   Installing Vagner Sales Agent
echo ========================================
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Installing dependencies...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Edit .env with your API keys
echo 3. Run: python scripts\init_kb.py
echo 4. Run: start.bat
echo.

pause

