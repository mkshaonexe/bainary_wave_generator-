@echo off
echo ====================================
echo   Theta Wave Generator Launcher
echo ====================================
echo.
echo Starting Theta Wave Binaural Beat Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show numpy >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    echo This may take a minute...
    echo.
    pip install --upgrade pip
    pip install numpy sounddevice
)

REM Run the application
echo.
echo Launching GUI...
echo.
python theta_wave_generator.py

pause

