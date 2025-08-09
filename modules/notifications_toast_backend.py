"""
notifications_toast_backend.py
------------------------------
Provides a cross-platform best-effort toast notification helper. On Windows it
uses win10toast if available, else falls back to print. For simplicity and to
avoid extra dependencies, we attempt dynamic import.
"""
from __future__ import annotations

try:
    from win10toast import ToastNotifier  # type: ignore
except Exception:  # pragma: no cover
    ToastNotifier = None  # type: ignore

_notifier = None

def _get_notifier():
    global _notifier
    if _notifier is None and ToastNotifier:
        try:
            _notifier = ToastNotifier()
        except Exception:
            _notifier = False
    return _notifier


def show_toast(title: str, msg: str, duration: float = 3.0):
    n = _get_notifier()
    if n:
        try:
            n.show_toast(title, msg, duration=duration, threaded=True)
            return
        except Exception:
            pass
    print(f"[Auto-Unzip] {title}: {msg}")
