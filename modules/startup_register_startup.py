"""
startup_register_startup.py
---------------------------
Defines register_startup() which creates a registry Run key entry to auto-start
the script on user login. Safe no-op if winreg is unavailable.
"""
import os
try:
    import winreg  # type: ignore
except ImportError:  # pragma: no cover
    winreg = None  # type: ignore

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "AutoUnzipService"

def register_startup(script_path: str) -> None:
    if not winreg:
        return
    try:
        full = os.path.abspath(script_path)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:  # type: ignore[attr-defined]
            winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, f'"{full}"')  # type: ignore[attr-defined]
    except OSError:
        pass
