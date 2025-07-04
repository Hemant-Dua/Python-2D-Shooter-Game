@echo off
cd gameFiles

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python to proceed.
    pause
    exit /b
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run the game
echo Starting the game...
python main.py

pause