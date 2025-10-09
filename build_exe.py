"""
Build script to create standalone executable for Theta Wave Generator
This creates a single .exe file that users can download and run directly
"""

import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Build the standalone executable"""
    
    print("=" * 60)
    print("Building Theta Wave Generator Executable")
    print("=" * 60)
    print()
    
    # Clean previous builds
    if os.path.exists('build'):
        print("Cleaning build directory...")
        shutil.rmtree('build')
    if os.path.exists('dist'):
        print("Cleaning dist directory...")
        shutil.rmtree('dist')
    
    print("Starting PyInstaller build process...")
    print()
    
    # PyInstaller options
    PyInstaller.__main__.run([
        'theta_wave_generator.py',           # Main script
        '--name=ThetaWaveGenerator',          # Name of the exe
        '--onefile',                          # Single exe file
        '--windowed',                         # No console window (GUI only)
        '--clean',                            # Clean PyInstaller cache
        '--noconfirm',                        # Replace output directory without asking
        '--add-data=README.md;.',            # Include README
        '--add-data=QUICK_START.txt;.',      # Include quick start guide
        '--hidden-import=numpy',              # Ensure numpy is included
        '--hidden-import=sounddevice',        # Ensure sounddevice is included
        '--hidden-import=tkinter',            # Ensure tkinter is included
        '--collect-all=sounddevice',          # Collect all sounddevice files
        '--collect-all=numpy',                # Collect all numpy files
        '--optimize=2',                       # Optimize bytecode
    ])
    
    print()
    print("=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print()
    print(f"Executable location: dist\\ThetaWaveGenerator.exe")
    print(f"File size: {os.path.getsize('dist/ThetaWaveGenerator.exe') / (1024*1024):.1f} MB")
    print()
    print("Users can now download and run ThetaWaveGenerator.exe directly!")
    print("No Python installation or dependencies required.")
    print()
    
if __name__ == "__main__":
    build_executable()

