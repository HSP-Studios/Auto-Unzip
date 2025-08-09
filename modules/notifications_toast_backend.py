"""
notifications_toast_backend.py
--------------------------------
Provides a minimal abstraction for showing toast notifications on Windows.
Primary implementation uses winotify (Windows 10 toast helper) for stable
notifications. Falls back to console if unavailable.
All higher-level notification helper functions should import show_toast()
from this module so implementation can be swapped or enhanced easily.
"""

from __future__ import annotations
import threading
import time
import sys
import platform

# Implementation strategy:
# 1. Try winotify for toast notifications.
# 2. If not available, degrade to console logging.
# 3. Provide de-duplication window to reduce spam.

_toast_lock = threading.Lock()

_use_winotify = False

try:  # pragma: no cover
	if platform.system() == 'Windows':
		from winotify import Notification  # type: ignore
		_use_winotify = True
	else:
		Notification = None  # type: ignore
except Exception:
	Notification = None  # type: ignore


_last_message_key = None
_last_message_time = 0.0
_SUPPRESS_REPEAT_SECONDS = 2.0

def show_toast(title: str, msg: str, duration: int = 5) -> None:
	"""Thread-safe toast display.

	Falls back to console printing if toast backend unavailable.
	"""
	global _last_message_key, _last_message_time
	key = (title, msg)
	now = time.time()
	if key == _last_message_key and now - _last_message_time < _SUPPRESS_REPEAT_SECONDS:
		return
	_last_message_key = key
	_last_message_time = now

	with _toast_lock:
		if _use_winotify and Notification is not None:  # pragma: no cover
			try:
				n = Notification(app_id="Auto-Unzip", title=title, msg=msg)
				n.show()
				return
			except Exception as e:
				print(f"[Auto-Unzip] Toast error, falling back to console: {e}", file=sys.stderr)
	print(f"[Auto-Unzip] {title}: {msg}")

