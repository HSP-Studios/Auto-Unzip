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
from modules.gui_options_window import create_and_show_options_window
from modules.qt_event_loop import integrate_qt_loop



class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print('[Auto-Unzip] Source changed, restarting...')
            os.execv(sys.executable, [sys.executable] + sys.argv)

def main():
    cfg_holder = {}

    # Background logic that must NOT create Qt widgets
    def app_logic():
        print('[Debug] app_logic starting in thread', threading.current_thread().name)
        cfg = load_config()
        cfg_holder['cfg'] = cfg
        print('[Debug] Config loaded; scheduling watcher. cfg id:', id(cfg))
        show_startup_toast()
        watcher = DirectoryWatcher(lambda: cfg.watch_folders, lambda p: process_archive(p, cfg), cfg.poll_interval_seconds)
        watcher.start()
        print('[Debug] DirectoryWatcher started')
        event_handler = RestartHandler()
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(__file__), recursive=True)
        observer.start()
        print('[Debug] Observer started; entering loop')
        _install_signals(watcher)
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            print('[Debug] app_logic shutting down')
            watcher.stop()
            observer.stop()
            observer.join()
            save_config(cfg)

    # Defer Qt GUI related objects to main thread if Qt available
    try:
        from PyQt6 import QtCore  # type: ignore
        print('[Debug] Qt available; scheduling tray init on main thread')
        def init_tray():  # runs on Qt main thread
            print('[Debug] init_tray running on thread', threading.current_thread().name)
            cfg = cfg_holder.get('cfg') or load_config()
            print('[Debug] init_tray using cfg id:', id(cfg))
            def _open_options():
                print('[Debug] _open_options invoked on', threading.current_thread().name)
                create_and_show_options_window(cfg, _graceful_exit)
            tray = TrayController(open_options=_open_options)
            tray.start()
            print('[Debug] TrayController started (visible may still be False initially)')
        QtCore.QTimer.singleShot(0, init_tray)
    except Exception as e:
        print('[Debug] Qt not available or tray scheduling failed:', e)

    print('[Debug] Calling integrate_qt_loop from thread', threading.current_thread().name)
    integrate_qt_loop(app_logic)
    print('[Debug] integrate_qt_loop returned (Qt loop exited)')


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
