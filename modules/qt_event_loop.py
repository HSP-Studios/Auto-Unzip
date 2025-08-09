"""
qt_event_loop.py
-----------------
Provides integrate_qt_loop(run_fn) which attempts to start a Qt event loop
on the main thread if PyQt6 is available. The provided run_fn is executed in a
worker thread to keep existing polling + tray logic functioning. If Qt is not
available, it simply calls run_fn synchronously.
"""
from __future__ import annotations
import threading
from typing import Callable

try:  # pragma: no cover
    from PyQt6 import QtWidgets  # type: ignore
except Exception:  # pragma: no cover
    QtWidgets = None  # type: ignore


def integrate_qt_loop(run_fn: Callable[[], None]):
    if QtWidgets is None:
        # No Qt, run normally
        run_fn()
        return

    # If a QApplication already exists, just run_fn in a thread
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    t = threading.Thread(target=run_fn, daemon=True)
    t.start()
    app.exec()
