def extract_archive(path: str, target_dir: str, progress_cb) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.zip':
        return extract_zip(path, target_dir, progress_cb)
    if ext == '.zipx':
        return extract_zipx(path, target_dir, progress_cb)
    if ext == '.7z':
        return extract_7z(path, target_dir, progress_cb)
    if ext == '.rar':
        return extract_rar(path, target_dir, progress_cb)
    return False

"""
extract_archive.py
------------------
Dispatches extraction based on file extension.
Supports: .zip, .zipx, .7z, .rar, .tar, .gz, .bz2, .tgz, .tbz, .cab
"""
import os
from .extract_zip import extract_zip
from .extract_zipx import extract_zipx
from .extract_7z import extract_7z
from .extract_rar import extract_rar
from .extract_tar_gz_bz2 import extract_tar_gz_bz2

"""
extract_archive.py
------------------
Dispatches extraction based on file extension.
Supports: .zip, .zipx, .7z, .rar, .tar, .gz, .bz2, .tgz, .tbz, .cab
"""
import os
from .extract_zip import extract_zip
from .extract_zipx import extract_zipx
from .extract_7z import extract_7z
from .extract_rar import extract_rar
from .extract_tar_gz_bz2 import extract_tar_gz_bz2

def extract_archive(path: str, target_dir: str, progress_cb) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.zip':
        return extract_zip(path, target_dir, progress_cb)
    if ext == '.zipx':
        return extract_zipx(path, target_dir, progress_cb)
    if ext == '.7z':
        return extract_7z(path, target_dir, progress_cb)
    if ext == '.rar':
        return extract_rar(path, target_dir, progress_cb)
    if ext in ['.tar', '.gz', '.bz2', '.tgz', '.tbz', '.tar.gz', '.tar.bz2']:
        return extract_tar_gz_bz2(path, target_dir, progress_cb)
    if ext == '.cab':
        from .extract_cab import extract_cab
        # CAB extraction does not support progress callback
        return extract_cab(path, target_dir)
    return False
def extract_archive(path: str, target_dir: str, progress_cb) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.zip':
        return extract_zip(path, target_dir, progress_cb)
    if ext == '.zipx':
        return extract_zipx(path, target_dir, progress_cb)
    if ext == '.7z':
        return extract_7z(path, target_dir, progress_cb)
    if ext == '.rar':
        return extract_rar(path, target_dir, progress_cb)
<<<<<<< HEAD
    if ext in ['.tar', '.gz', '.bz2', '.tgz', '.tbz', '.tar.gz', '.tar.bz2']:
        return extract_tar_gz_bz2(path, target_dir, progress_cb)
    if ext == '.cab':
        # CAB extraction does not support progress callback
        return extract_cab(path, target_dir)
=======
    if ext in ['.tar', '.gz', '.bz2', '.tgz', '.tbz', '.tar.gz', '.tar.bz2']:
        return extract_tar_gz_bz2(path, target_dir, progress_cb)
>>>>>>> feature/tar-gz-bz2-support
    return False
