"""
extract_tar_gz_bz2.py
---------------------
Defines extract_tar_gz_bz2() which extracts .tar, .gz, .bz2, .tgz, .tbz archives using tarfile/gzip/bz2.
"""
import tarfile
import os

def extract_tar_gz_bz2(path: str, target_dir: str, progress_cb):
    try:
        # Handle .tar, .tgz, .tbz, .tar.gz, .tar.bz2
        if tarfile.is_tarfile(path):
            with tarfile.open(path, 'r:*') as tf:
                members = tf.getmembers()
                total = len(members)
                for idx, m in enumerate(members):
                    tf.extract(m, target_dir)
                    percent = ((idx + 1) / total) * 100.0
                    progress_cb(percent)
            progress_cb(100.0)
            return True
        # Handle .gz, .bz2 (single file)
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.gz', '.bz2']:
            import shutil
            import gzip
            import bz2
            base = os.path.basename(path)
            out_path = os.path.join(target_dir, base.replace(ext, ''))
            os.makedirs(target_dir, exist_ok=True)
            if ext == '.gz':
                with gzip.open(path, 'rb') as f_in, open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            elif ext == '.bz2':
                with bz2.open(path, 'rb') as f_in, open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            progress_cb(100.0)
            return True
        return False
    except Exception:
        return False
