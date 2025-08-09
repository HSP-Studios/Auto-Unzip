"""
qt_event_loop.py
-----------------
Provides integrate_qt_loop(run_fn) which, if PyQt6 is available, creates a
QApplication on the main thread, starts run_fn in a background thread (run_fn
MUST NOT create Qt widgets), then enters the Qt event loop. GUI creation must
be scheduled onto the main thread (e.g., via QTimer.singleShot). If PyQt6 is
not available, run_fn is executed synchronously.
"""
from __future__ import annotations
import threading
import sys
from typing import Callable

try:  # pragma: no cover
    from PyQt6 import QtWidgets  # type: ignore
except Exception:  # pragma: no cover
    QtWidgets = None  # type: ignore


def integrate_qt_loop(run_fn: Callable[[], None]):
    if QtWidgets is None:
        run_fn()
        return
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    try:
        # Prevent closing last window from exiting background logic
        app.setQuitOnLastWindowClosed(False)
    except Exception:
        pass
    t = threading.Thread(target=lambda: _run_wrapper(run_fn), daemon=True, name='AppLogicThread')
    t.start()
    app.exec()


def _run_wrapper(run_fn):  # pragma: no cover
    try:
        run_fn()
    except Exception as e:  # noqa
        print('[Auto-Unzip] Background logic error:', e, file=sys.stderr)
