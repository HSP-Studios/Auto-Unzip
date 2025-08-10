"""
config_dataclass.py
-------------------
Defines the Config dataclass which holds application runtime settings like
watched folders, polling interval, and whether to delete archives after
extraction.
"""
from dataclasses import dataclass, field
from typing import List
from .config_default_downloads_folder import default_downloads_folder

@dataclass
class Config:
    watch_folders: List[str] = field(default_factory=lambda: [default_downloads_folder()])
    poll_interval_seconds: float = 2.0
    delete_archives_after_extract: bool = True
    enable_hot_reload: bool = True  # allow disabling automatic code reloads
    development: bool = False  # enables development mode features like hot reload toggle
