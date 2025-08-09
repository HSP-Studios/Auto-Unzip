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
        print('[Debug][qt_event_loop] PyQt6 not available; running function directly')
        run_fn()
        return
    app = QtWidgets.QApplication.instance()
    if app is None:
        print('[Debug][qt_event_loop] Creating QApplication on thread', threading.current_thread().name)
        app = QtWidgets.QApplication([])
    else:
        print('[Debug][qt_event_loop] Reusing existing QApplication on thread', threading.current_thread().name)
    print('[Debug][qt_event_loop] Spawning background thread for run_fn')
    t = threading.Thread(target=lambda: _run_wrapper(run_fn), daemon=True, name='AppLogicThread')
    t.start()
    print('[Debug][qt_event_loop] Entering app.exec() on', threading.current_thread().name)
    rc = app.exec()
    print('[Debug][qt_event_loop] app.exec() exited with code', rc)


def _run_wrapper(run_fn):  # pragma: no cover
    try:
        print('[Debug][qt_event_loop] run_fn starting in thread', threading.current_thread().name)
        run_fn()
    except Exception as e:  # noqa
        print('[Debug][qt_event_loop] run_fn exception:', e, file=sys.stderr)
    finally:
        print('[Debug][qt_event_loop] run_fn finished')
