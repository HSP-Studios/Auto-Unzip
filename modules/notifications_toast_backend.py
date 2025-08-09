"""
notifications_toast_backend.py
--------------------------------
Provides a minimal abstraction for showing toast notifications on Windows.
Primary implementation uses Windows 10/11 native toast notifications via
winrt (Windows App SDK / UWP API surface). Falls back to console if unavailable.
All higher-level notification helper functions should import show_toast()
from this module so implementation can be swapped or enhanced easily.
"""

from __future__ import annotations
import threading
import time
import sys
import platform

# Implementation strategy:
# 1. Try winrt (pywinrt) toast notification manager for stable native toasts.
# 2. If not available, degrade to simple console logging.
# 3. Provide de-duplication window to reduce spam.

_toast_lock = threading.Lock()

_use_winrt = False
_winrt_toast = None

try:  # pragma: no cover
	if platform.system() == 'Windows':
		from winrt.windows.ui.notifications import ToastNotificationManager, ToastNotification  # type: ignore
		from winrt.windows.data.xml.dom import XmlDocument  # type: ignore
		APP_ID = "AutoUnzipApp"
		_notifier = ToastNotificationManager.create_toast_notifier(APP_ID)
		_use_winrt = True
	else:
		_notifier = None
except Exception:
	_notifier = None
	_use_winrt = False


_last_message_key = None
_last_message_time = 0.0
_SUPPRESS_REPEAT_SECONDS = 2.0

def show_toast(title: str, msg: str, duration: int = 5) -> None:
	"""Thread-safe toast display.

	Falls back to console printing if toast backend unavailable.
	"""
	global _notifier, _last_message_key, _last_message_time
	key = (title, msg)
	now = time.time()
	if key == _last_message_key and now - _last_message_time < _SUPPRESS_REPEAT_SECONDS:
		return
	_last_message_key = key
	_last_message_time = now

	with _toast_lock:
		if _use_winrt and _notifier is not None:  # pragma: no cover
			try:
				xml = f"""<toast><visual><binding template='ToastGeneric'>
					<text>{title}</text>
					<text>{msg}</text>
				</binding></visual></toast>"""
				doc = XmlDocument()
				doc.load_xml(xml)
				toast = ToastNotification(doc)
				_notifier.show(toast)
				return
			except Exception as e:
				print(f"[Auto-Unzip] Toast error, falling back to console: {e}", file=sys.stderr)
				_notifier = None
	print(f"[Auto-Unzip] {title}: {msg}")

