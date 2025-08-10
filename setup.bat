@echo off
REM setup.bat - Auto-Unzip project setup script
REM Ensures Python, pip dependencies, and UnRAR tool are installed

REM Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.x from https://www.python.org/downloads/
    exit /b 1
) else (
    echo Python found.
)

REM Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Check for UnRAR tool in dependencies folder
if exist dependencies\unrarw64.exe (
    echo UnRAR found in dependencies folder.
) else (
    echo UnRAR not found. Please download from https://www.rarlab.com/rar_add.htm and place unrarw64.exe in dependencies\
)

REM Setup complete
echo Setup complete. You can now run Auto-Unzip.
