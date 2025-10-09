@echo off
echo ============================================================
echo   Building Theta Wave Generator Standalone Executable
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Install build dependencies if needed
echo Checking build dependencies...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Run build script
echo.
echo Building executable...
echo This may take a few minutes...
echo.
python build_exe.py

echo.
echo ============================================================
echo Build process completed!
echo.
echo Your executable is ready in the 'dist' folder:
echo   dist\ThetaWaveGenerator.exe
echo.
echo Users can download and run this file directly!
echo No installation required!
echo ============================================================
echo.

pause

