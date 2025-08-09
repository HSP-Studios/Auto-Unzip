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
import time
import sys

# Some environments experience crashes with threaded Win32 toast callbacks.
# We'll avoid threaded=True and implement a lightweight rate limiter +
# auto-disable on repeated exceptions.

_toast_lock = threading.Lock()

try:  # pragma: no cover - optional dependency
	from win10toast import ToastNotifier  # type: ignore
	_notifier = ToastNotifier()
except Exception:  # pragma: no cover
	_notifier = None  # type: ignore


_failure_count = 0
_DISABLE_AFTER = 3
_last_message_key = None
_last_message_time = 0.0
_SUPPRESS_REPEAT_SECONDS = 2.0

def show_toast(title: str, msg: str, duration: int = 5) -> None:
	"""Thread-safe toast display.

	Falls back to console printing if toast backend unavailable.
	"""
	global _failure_count, _notifier, _last_message_key, _last_message_time
	key = (title, msg)
	now = time.time()
	if key == _last_message_key and now - _last_message_time < _SUPPRESS_REPEAT_SECONDS:
		return  # suppress rapid duplicates
	_last_message_key = key
	_last_message_time = now

	with _toast_lock:
		if _notifier is not None and _failure_count < _DISABLE_AFTER:  # pragma: no cover
			try:
				# Use non-threaded to reduce WNDPROC issues; block briefly then return.
				_notifier.show_toast(title, msg, duration=duration, threaded=False)
				return
			except Exception as e:  # pragma: no cover
				_failure_count += 1
				if _failure_count >= _DISABLE_AFTER:
					_notifier = None
					print('[Auto-Unzip] Disabling toast backend after repeated errors.', file=sys.stderr)
	print(f"[Auto-Unzip] {title}: {msg}")

