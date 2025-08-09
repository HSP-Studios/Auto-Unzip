"""
startup_is_registered.py
------------------------
Defines is_registered() which returns True if the Run key entry exists.
"""
try:
    import winreg  # type: ignore
except ImportError:  # pragma: no cover
    winreg = None  # type: ignore

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "AutoUnzipService"

def is_registered() -> bool:
    if not winreg:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_READ) as key:  # type: ignore[attr-defined]
            winreg.QueryValueEx(key, VALUE_NAME)  # type: ignore[attr-defined]
            return True
    except OSError:
        return False
