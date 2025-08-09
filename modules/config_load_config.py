"""
config_load_config.py
---------------------
Provides load_config() to load settings from disk and return a Config instance
(or defaults if the file is missing or invalid).
"""
import json
import os
from .config_dataclass import Config
from .config_settings_file_path import get_settings_file_path
from .config_save_config import save_config

def load_config() -> Config:
    """Load configuration, creating or repairing as needed.

    Side-effects:
        - If the settings file did not exist and is created now, sets
          transient attribute _was_new = True on the returned Config.
        - If the settings file existed but was corrupt and got repaired,
          sets transient attribute _was_repaired = True.
    These attributes are NOT persisted; they exist only for the current run.
    """
    path = get_settings_file_path()
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Config(**data)
        except Exception:
            cfg = Config()
            save_config(cfg)
            setattr(cfg, '_was_repaired', True)
            return cfg
    # First launch: create file with defaults and mark
    cfg = Config()
    save_config(cfg)
    setattr(cfg, '_was_new', True)
    return cfg
