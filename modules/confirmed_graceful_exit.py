"""
confirmed_graceful_exit.py
-------------------------
Provides confirmed_graceful_exit() as a wrapper for graceful_exit, used by options window.
"""
from modules.graceful_exit import graceful_exit

def confirmed_graceful_exit():
    """Wrapper for graceful exit, used by options window for API consistency."""
    graceful_exit()
