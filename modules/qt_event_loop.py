"""
qt_event_loop.py
-----------------
Provides integrate_qt_loop(run_fn) which ensures a Qt event loop exists on the
main thread, then runs run_fn synchronously ON the main thread (so any Qt
widgets inside run_fn are created on the correct thread). If Qt is not
available, it falls back to calling run_fn directly.
"""
from __future__ import annotations
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
    created = False
    if app is None:
        app = QtWidgets.QApplication([])
        created = True
    # Run the logic synchronously on the main thread
    run_fn()
    if created:
        # Only start the event loop if we created it
        app.exec()
