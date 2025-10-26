@echo off
echo ===================================
echo Building Binaural Wave Generator
echo ===================================
echo.

echo Step 1: Installing PyInstaller...
pip install pyinstaller

echo.
echo Step 2: Building executable...
python -m PyInstaller --name=BinauralWaveGenerator --onefile --windowed theta_wave_generator.py

echo.
echo ===================================
echo Build Complete!
echo ===================================
echo.
echo Your executable is ready at:
echo   dist\BinauralWaveGenerator.exe
echo.
echo File size: ~23 MB
echo Ready to share and distribute!
echo.
pause

