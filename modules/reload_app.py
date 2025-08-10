"""
reload_app.py
-------------
Provides reload_app() to reload the application process cleanly.
"""
from modules.perform_exec_restart import perform_exec_restart
from modules.graceful_exit import graceful_exit

def reload_app():
    """Reload the entire application process cleanly."""
    try:
        perform_exec_restart()
    except Exception:
        graceful_exit()
