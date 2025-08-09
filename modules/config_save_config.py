"""
config_save_config.py
---------------------
Provides save_config() which persists the current Config to disk as JSON.
"""
import json
from .config_dataclass import Config
from .config_settings_file_path import get_settings_file_path

def save_config(cfg: Config) -> None:
    try:
        with open(get_settings_file_path(), 'w', encoding='utf-8') as f:
            json.dump(cfg.__dict__, f, indent=2)
    except Exception:
        pass
