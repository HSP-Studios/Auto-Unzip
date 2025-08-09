"""
startup_unregister_startup.py
-----------------------------
Defines unregister_startup() which removes the registry Run key entry.
"""
try:
    import winreg  # type: ignore
except ImportError:  # pragma: no cover
    winreg = None  # type: ignore

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "AutoUnzipService"

def unregister_startup() -> None:
    if not winreg:
        return
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:  # type: ignore[attr-defined]
            winreg.DeleteValue(key, VALUE_NAME)  # type: ignore[attr-defined]
    except OSError:
        pass
