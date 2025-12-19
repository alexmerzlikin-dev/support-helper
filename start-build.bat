@echo off
echo Text Support Helper - Build
echo ====================================

REM
python -m venv venv 2>nul
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo Install requirements
pip install keyboard PyInstaller

echo.
echo Building exe...
python build.py

pause