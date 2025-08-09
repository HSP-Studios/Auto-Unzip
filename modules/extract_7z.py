"""
extract_7z.py
-------------
Defines extract_7z() which extracts .7z archives using py7zr and reports progress.
"""
import py7zr
import os

def extract_7z(path: str, target_dir: str, progress_cb):
    try:
        with py7zr.SevenZipFile(path, mode='r') as archive:
            all_files = archive.getnames()
            total = len(all_files)
            if total == 0:
                return False
            for idx, name in enumerate(all_files):
                archive.extract(target_dir, targets=[name])
                percent = ((idx + 1) / total) * 100.0
                progress_cb(percent)
        progress_cb(100.0)
        return True
    except Exception:
        return False
