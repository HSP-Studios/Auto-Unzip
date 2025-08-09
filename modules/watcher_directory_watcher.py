"""
watcher_directory_watcher.py
----------------------------
Defines DirectoryWatcher which polls watch folders for new archive files and
calls a callback for each new archive found. Polling keeps dependencies minimal.
"""
from __future__ import annotations
import os
import threading
import time
from typing import Callable, Iterable, Set

ARCHIVE_EXTENSIONS = {'.zip'}

class DirectoryWatcher:
    def __init__(self, get_folders: Callable[[], Iterable[str]], on_new_archive: Callable[[str], None], interval: float = 2.0):
        self.get_folders = get_folders
        self.on_new_archive = on_new_archive
        self.interval = interval
        self._seen: Set[str] = set()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        while not self._stop.is_set():
            for folder in list(self.get_folders()):
                try:
                    for entry in os.scandir(folder):
                        if not entry.is_file():
                            continue
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in ARCHIVE_EXTENSIONS:
                            full = os.path.abspath(entry.path)
                            if full not in self._seen:
                                self._seen.add(full)
                                self.on_new_archive(full)
                except FileNotFoundError:
                    continue
            time.sleep(self.interval)
