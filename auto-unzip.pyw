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
import json
import subprocess
from typing import List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from modules.config_load_config import load_config
from modules.config_save_config import save_config
from modules.config_dataclass import Config
from modules.notifications_show_startup import show_startup_toast
from modules.notifications_toast_backend import show_toast
from modules.workflow_process_archive import process_archive
from modules.watcher_directory_watcher import DirectoryWatcher
from modules.tray_tray_controller import TrayController
import queue
from modules.gui_options_window import create_and_show_options_window
from modules.qt_event_loop import integrate_qt_loop
from modules.add_folder import add_folder
from modules.graceful_exit import graceful_exit
from modules.confirmed_graceful_exit import confirmed_graceful_exit
from modules.reload_app import reload_app
from modules.perform_exec_restart import perform_exec_restart
from modules.read_pid_file import read_pid_file
from modules.write_pid_file import write_pid_file
from modules.kill_pid import kill_pid
from modules.enforce_single_instance import enforce_single_instance
from modules.install_signals import install_signals



class RestartHandler(FileSystemEventHandler):
    """Debounced project file change restarter.

    Watches for modifications to .py / .pyw files under the project root.
    Ignores changes in temporary / runtime folders (e.g. __pycache__).
    On first qualifying change after the debounce window, re-execs the process.
    """
    def __init__(self, project_root: str, min_interval: float = 1.5, initial_delay: float = 2.0):
        super().__init__()
        self.project_root = os.path.abspath(project_root)
        self.min_interval = min_interval
        self.initial_delay = initial_delay
        self._start_time = time.time()
        self._last_restart = 0.0
        self._pending = False
 
    def _should_consider(self, path: str) -> bool:
        if not path.endswith(('.py', '.pyw')):
            return False
        # ignore __pycache__ or hidden
        parts = path.lower().split(os.sep)
        if '__pycache__' in parts:
            return False
        # Exclude any file inside the 'testing' folder
        if 'testing' in parts:
            return False
        return True

    def on_modified(self, event):  # pragma: no cover
        try:
            changed = os.path.abspath(event.src_path)
        except Exception:
            return
        # Ignore early events right after startup to prevent immediate restart loop
        if (time.time() - self._start_time) < self.initial_delay:
            return
        if not self._should_consider(changed):
            return
        now = time.time()
        if now - self._last_restart < self.min_interval:
            # debounce; mark pending but do not restart yet
            self._pending = True
            return
        self._trigger_restart(changed)

    def _trigger_restart(self, changed: str):
        self._last_restart = time.time()
        self._pending = False
        print(f'[Auto-Unzip] Source changed ({changed}), restarting...')
        try:
            perform_exec_restart()
        except Exception as e:
            print(f'[Auto-Unzip] Restart failed: {e}')

    def poll(self):  # periodic check if a pending restart can now occur
        if self._pending and (time.time() - self._last_restart) >= self.min_interval:
            self._trigger_restart('pending-change')

def main():
    # Basic CLI handling (keep lightweight to avoid argparse dependency)
    argv_lower = [a.lower() for a in sys.argv[1:]]
    if ('-h' in argv_lower) or ('--help' in argv_lower):
        print("Auto-Unzip - automatic extraction service")
        print("Usage: python auto-unzip.pyw [options]")
        print()
        print("Options:")
        print("  -h, --help       Show this help and exit")
        print("  -v, --version    Show version and exit")
        print()
        print("The application has no runtime CLI options; configuration is managed via")
        print("the Options window (tray icon) and the config/settings.json file.")
        return
    if ('-v' in argv_lower) or ('--version' in argv_lower):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'config', 'version.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Auto-Unzip version {data.get('version', 'unknown')}")
        except Exception:
            print("Auto-Unzip version unknown (version.json unreadable)")
        return

    enforce_single_instance()

    # Load config once on main thread so all components share the same instance
    initial_cfg = load_config()
    first_launch = getattr(initial_cfg, '_was_new', False)
    if first_launch:
        try:
            from modules.startup_shortcut import create_startup_shortcut, remove_startup_shortcut
            if getattr(initial_cfg, 'launch_on_startup', True):
                create_startup_shortcut()
            else:
                remove_startup_shortcut()
        except Exception as e:
            print(f'[Auto-Unzip] Could not update startup shortcut: {e}')

    def app_logic():  # background (non-Qt) logic
        cfg = initial_cfg
        # Only show the generic startup toast here; welcome modal handled on Qt thread
        show_startup_toast()
        watcher = DirectoryWatcher(lambda: cfg.watch_folders, lambda p: process_archive(p, cfg), cfg.poll_interval_seconds)
        watcher.start()
        project_root = os.path.dirname(os.path.abspath(__file__))
        event_handler = None
        observer = None
        if getattr(cfg, 'enable_hot_reload', True):
            event_handler = RestartHandler(project_root=project_root)
            observer = Observer()
            observer.schedule(event_handler, path=project_root, recursive=True)
            observer.start()
        install_signals(watcher)
        try:
            while True:
                time.sleep(0.5)
                if event_handler:
                    try:
                        event_handler.poll()
                    except Exception:
                        pass
        except KeyboardInterrupt:
            pass
        finally:
            watcher.stop()
            if observer:
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
                ui_queue.put(lambda: create_and_show_options_window(cfg, confirmed_graceful_exit, reload_app))
            def _request_quit():
                # Must run on UI thread: enqueue dialog creation
                ui_queue.put(_confirm_and_quit)
            tray = TrayController(open_options=_open_options, request_quit=_request_quit)
            tray.start()
        def _confirm_and_quit():
            try:
                from PyQt6 import QtWidgets  # type: ignore
                res = QtWidgets.QMessageBox.question(None, 'Quit Auto-Unzip', 'Are you sure you want to quit?',
                                                     QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                                     QtWidgets.QMessageBox.StandardButton.No)
                if res == QtWidgets.QMessageBox.StandardButton.Yes:
                    graceful_exit()
            except Exception:
                graceful_exit()
        QtCore.QTimer.singleShot(0, _process_ui_queue)
        QtCore.QTimer.singleShot(0, init_tray)
        if first_launch:
            def _welcome_modal():
                try:
                    from PyQt6 import QtWidgets  # type: ignore
                    m = QtWidgets.QMessageBox()
                    m.setWindowTitle("Welcome to Auto-Unzip")
                    m.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    m.setText("Auto-Unzip is now monitoring your Downloads folder. You can change folders and settings via the tray icon (Options).")
                    m.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    # Ensure it shows even if no other windows yet
                    m.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
                    m.exec()
                except Exception:
                    show_toast("Auto-Unzip", "Welcome! Monitoring your Downloads folder. Tray icon > Options to adjust.")
            # Defer a little so the QApplication is fully initialized and tray starting
            QtCore.QTimer.singleShot(200, _welcome_modal)
    except Exception:
        pass

    integrate_qt_loop(app_logic)






if __name__ == '__main__':
    main()
