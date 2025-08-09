"""
auto-unzip.py
-------------
Main Script for Auto-Unzip
"""

import signal
import sys
import threading
import os
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
    cfg = load_config()
    show_startup_toast()

    def _open_options():
        create_and_show_options_window(cfg, _graceful_exit)

    tray_controller = TrayController(open_options=_open_options)
    tray_controller.start()

    watcher = DirectoryWatcher(lambda: cfg.watch_folders, lambda p: process_archive(p, cfg), cfg.poll_interval_seconds)
    watcher.start()

    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(__file__), recursive=True)
    observer.start()

    _install_signals(watcher)

    def loop():
        try:
            while True:
                if hasattr(signal, 'pause'):
                    signal.pause()  # type: ignore[attr-defined]
                else:
                    threading.Event().wait(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            watcher.stop()
            observer.stop()
            observer.join()
            save_config(cfg)

    integrate_qt_loop(loop)


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
