"""
auto-unzip.py
-------------
Entry point that wires together the modular components. Only orchestration lives here.
"""
import signal
import sys
import threading
import os

from modules.config_load_config import load_config
from modules.config_save_config import save_config
from modules.config_dataclass import Config
from modules.notifications_show_startup import show_startup_toast
from modules.workflow_process_archive import process_archive
from modules.watcher_directory_watcher import DirectoryWatcher
from modules.tray_tray_controller import TrayController


def main():
    cfg = load_config()
    show_startup_toast()

    tray_controller = TrayController(
        get_folders=lambda: cfg.watch_folders,
        add_folder=lambda p: _add_folder(p, cfg),
        on_quit=_graceful_exit
    )
    tray_controller.start()

    watcher = DirectoryWatcher(lambda: cfg.watch_folders, lambda p: process_archive(p, cfg), cfg.poll_interval_seconds)
    watcher.start()

    _install_signals(watcher)
    try:
        while True:
            if hasattr(signal, 'pause'):
                signal.pause()  # type: ignore[attr-defined]
            else:
                threading.Event().wait(1)
    except KeyboardInterrupt:
        pass
    finally:
        watcher.stop()
        save_config(cfg)


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
