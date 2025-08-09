"""
auto-unzip.py
-------------
Main Script for Auto-Unzip
"""

import signal
import sys
import threading
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from modules.config_load_config import load_config
from modules.config_save_config import save_config
from modules.config_dataclass import Config
from modules.notifications_show_startup import show_startup_toast
from modules.workflow_process_archive import process_archive
from modules.watcher_directory_watcher import DirectoryWatcher
from modules.tray_tray_controller import TrayController
import queue
from modules.gui_options_window import create_and_show_options_window
from modules.qt_event_loop import integrate_qt_loop



class RestartHandler(FileSystemEventHandler):
    def __init__(self, script_path: str, min_interval: float = 2.0):
        super().__init__()
        self.script_path = os.path.abspath(script_path)
        self.min_interval = min_interval
        self._last_restart = 0.0

    def on_modified(self, event):
        try:
            changed = os.path.abspath(event.src_path)
        except Exception:
            return
        # Only act if the main script file itself changed
        if os.path.normcase(changed) != os.path.normcase(self.script_path):
            return
        now = time.time()
        if now - self._last_restart < self.min_interval:
            return
        self._last_restart = now
        print(f'[Auto-Unzip] Source changed ({changed}), restarting...')
        script = self.script_path
        os.execv(sys.executable, [sys.executable, script] + sys.argv[1:])

def main():
    # Load config once on main thread so all components share the same instance
    initial_cfg = load_config()

    def app_logic():  # background (non-Qt) logic
        cfg = initial_cfg
        show_startup_toast()
        watcher = DirectoryWatcher(lambda: cfg.watch_folders, lambda p: process_archive(p, cfg), cfg.poll_interval_seconds)
        watcher.start()
        event_handler = RestartHandler(script_path=sys.argv[0])
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(__file__), recursive=True)
        observer.start()
        _install_signals(watcher)
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            watcher.stop()
            observer.stop()
            observer.join()
            save_config(cfg)

    # Tray + options scheduling (Qt main thread)
    try:
        from PyQt6 import QtCore  # type: ignore
        ui_queue: "queue.Queue[callable]" = queue.Queue()

        def _process_ui_queue():
            from queue import Empty
            while True:
                try:
                    act = ui_queue.get_nowait()
                except Empty:
                    break
                try:
                    act()
                except Exception:
                    pass
            QtCore.QTimer.singleShot(50, _process_ui_queue)

        def init_tray():
            cfg = initial_cfg
            def _open_options():
                # enqueue creation for main thread processing
                ui_queue.put(lambda: create_and_show_options_window(cfg, _graceful_exit))
            tray = TrayController(open_options=_open_options)
            tray.start()
        QtCore.QTimer.singleShot(0, _process_ui_queue)
        QtCore.QTimer.singleShot(0, init_tray)
    except Exception:
        pass

    integrate_qt_loop(app_logic)


def _add_folder(path: str, cfg: Config):
    full = os.path.abspath(path)
    if full not in cfg.watch_folders and os.path.isdir(full):
        cfg.watch_folders.append(full)
        save_config(cfg)


def _graceful_exit():
    sys.exit(0)


def _install_signals(w: DirectoryWatcher):
    def handler(signum, frame):  # noqa: unused
        w.stop()
        sys.exit(0)
    for s in ('SIGINT', 'SIGTERM'):
        if hasattr(signal, s):
            try:
                signal.signal(getattr(signal, s), handler)
            except Exception:
                pass


if __name__ == '__main__':
    main()
