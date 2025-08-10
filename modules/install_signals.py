"""
install_signals.py
------------------
Provides install_signals() to install signal handlers for graceful shutdown.
"""
import sys
import signal
from modules.watcher_directory_watcher import DirectoryWatcher

def install_signals(w: DirectoryWatcher):
    def handler(signum, frame):
        w.stop()
        sys.exit(0)
    for s in ('SIGINT', 'SIGTERM'):
        if hasattr(signal, s):
            try:
                signal.signal(getattr(signal, s), handler)
            except Exception:
                pass
