"""
notifications_toast_backend.py
--------------------------------
Provides a minimal abstraction for showing toast notifications on Windows.
Uses win10toast if installed; otherwise falls back to printing to console.
All higher-level notification helper functions should import show_toast()
from this module so implementation can be swapped or enhanced easily.
"""

from __future__ import annotations
import threading

_toast_lock = threading.Lock()

try:  # pragma: no cover - optional dependency
	from win10toast import ToastNotifier  # type: ignore
	_notifier = ToastNotifier()
except Exception:  # pragma: no cover
	_notifier = None  # type: ignore


def show_toast(title: str, msg: str, duration: int = 5) -> None:
	"""Thread-safe toast display.

	Falls back to console printing if toast backend unavailable.
	"""
	with _toast_lock:
		if _notifier is not None:  # pragma: no cover - GUI interaction
			try:
				_notifier.show_toast(title, msg, duration=duration, threaded=True)
				return
			except Exception:
				pass
		print(f"[Auto-Unzip] {title}: {msg}")

