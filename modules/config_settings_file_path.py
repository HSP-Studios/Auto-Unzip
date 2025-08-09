"""
config_settings_file_path.py
----------------------------
Provides get_settings_file_path() which returns the file path where the
application stores its persistent JSON configuration.
"""
import os

def get_settings_file_path() -> str:
    """Return path to settings.json in a new top-level 'config' directory.

    Migration logic:
    - Old location was modules/settings.json (same directory as this file).
    - On first run after upgrade, if old file exists and new file does not,
      move (atomic rename) the file to the new location.
    - Ensure the 'config' directory exists.
    """
    # Project root = parent of the 'modules' directory (this file lives inside it)
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_dir = os.path.join(project_root, 'config')
    try:
        os.makedirs(config_dir, exist_ok=True)
    except Exception:
        # Directory creation failure will fall back to old path
        old_fallback = os.path.join(os.path.dirname(__file__), 'settings.json')
        return old_fallback

    new_path = os.path.join(config_dir, 'settings.json')
    old_path = os.path.join(os.path.dirname(__file__), 'settings.json')

    # Migrate existing file if needed
    if os.path.exists(old_path) and not os.path.exists(new_path):
        try:
            os.replace(old_path, new_path)  # atomic on same filesystem
        except Exception:
            # If move fails, continue using old path for this run
            return old_path

    return new_path
