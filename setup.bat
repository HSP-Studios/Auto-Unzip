@echo off
REM setup.bat - Installs Python, pip dependencies, and UnRAR tool for Auto-Unzip

REM Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Downloading and installing Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe -OutFile python-installer.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
) else (
    echo Python is already installed.
)

REM Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Download UnRAR tool if not present
where unrar >nul 2>nul
if %errorlevel% neq 0 (
    echo UnRAR not found. Please ensure dependencies\unrarw64.exe exists.
    if exist dependencies\unrarw64.exe (
        echo UnRAR found in dependencies folder.
    ) else (
        echo Download UnRAR manually from https://www.rarlab.com/rar_add.htm and place unrarw64.exe in dependencies\
    )
) else (
    echo UnRAR is already installed and in PATH.
)

REM Done
echo Setup complete. You can now run Auto-Unzip.
pause
