"""
extract_zip.py
--------------
Defines extract_zip() which extracts the contents of a .zip archive while
invoking a progress callback based on cumulative file sizes.
"""
import zipfile

def extract_zip(path: str, target_dir: str, progress_cb):
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
