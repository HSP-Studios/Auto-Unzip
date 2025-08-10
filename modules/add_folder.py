"""
add_folder.py
-------------
Provides _add_folder(path: str, cfg: Config) to add a folder to the config's watch list and save config.
"""
import os
from modules.config_save_config import save_config
from modules.config_dataclass import Config

def add_folder(path: str, cfg: Config):
    """Add a folder to the config's watch list if it exists and is not already present."""
    full = os.path.abspath(path)
    if full not in cfg.watch_folders and os.path.isdir(full):
        cfg.watch_folders.append(full)
        save_config(cfg)
