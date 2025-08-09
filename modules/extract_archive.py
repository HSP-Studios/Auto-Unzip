"""
extract_archive.py
------------------
Defines extract_archive() which dispatches extraction based on file extension.
Supports .zip (extract_zip), .zipx (extract_zipx), .7z (extract_7z), .rar (extract_rar), .tar/.gz/.bz2/.tgz/.tbz (extract_tar_gz_bz2).
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
    return False
