"""
extract_zipx.py
---------------
Defines extract_zipx() which extracts .zipx archives using zipfile (if possible).
Note: Python's zipfile can open some .zipx files if they use standard compression.
For advanced .zipx features, third-party tools may be needed.
"""
import zipfile
import os

def extract_zipx(path: str, target_dir: str, progress_cb):
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            members = zf.infolist()
            total = sum(m.file_size for m in members) or 1
            extracted = 0
            for m in members:
                zf.extract(m, target_dir)
                extracted += m.file_size
                progress_cb(min(100.0, (extracted / total) * 100.0))
        progress_cb(100.0)
        return True
    except Exception:
        return False
