"""
extract_archive.py
------------------
Defines extract_archive() which dispatches extraction based on file extension.
Supports .zip (extract_zip) and .7z (extract_7z).
"""
import os
from .extract_zip import extract_zip
from .extract_7z import extract_7z
from .extract_cab import extract_cab

def extract_archive(path: str, target_dir: str, progress_cb) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.zip':
        return extract_zip(path, target_dir, progress_cb)
    if ext == '.7z':
        return extract_7z(path, target_dir, progress_cb)
    if ext == '.cab':
        # CAB extraction does not support progress callback
        return extract_cab(path, target_dir)
    return False
