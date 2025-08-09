"""
extract_rar.py
--------------
Defines extract_rar() which extracts .rar archives using rarfile.
Requires 'unrar' tool to be installed and available in PATH.
"""
import rarfile
import os

def extract_rar(path: str, target_dir: str, progress_cb):
    try:
        with rarfile.RarFile(path) as rf:
            members = rf.infolist()
            total = sum(m.file_size for m in members) or 1
            extracted = 0
            for m in members:
                rf.extract(m, target_dir)
                extracted += m.file_size
                progress_cb(min(100.0, (extracted / total) * 100.0))
        progress_cb(100.0)
        return True
    except Exception:
        return False
