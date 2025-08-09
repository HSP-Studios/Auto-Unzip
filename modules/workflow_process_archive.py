"""
workflow_process_archive.py
---------------------------
Defines process_archive() which orchestrates:
- create target directory
- perform extraction with progress notifications
- issue completion notification
- optionally delete the original archive
"""
import os
from .config_dataclass import Config
from .extract_archive import extract_archive
from .notifications_show_progress import show_progress_toast
from .notifications_show_completion import show_completion_toast

def process_archive(archive_path: str, cfg: Config) -> None:
    archive_name = os.path.basename(archive_path)
    target_dir = os.path.join(os.path.dirname(archive_path), os.path.splitext(archive_name)[0])
    os.makedirs(target_dir, exist_ok=True)

    def _progress(p: float):
        show_progress_toast(archive_name, p)

    success = extract_archive(archive_path, target_dir, _progress)
    show_completion_toast(archive_name, success, target_dir)
    if success and cfg.delete_archives_after_extract:
        try:
            os.remove(archive_path)
        except OSError:
            pass
