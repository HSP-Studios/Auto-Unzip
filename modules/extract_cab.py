import os
import shutil
import tempfile
import subprocess

def extract_cab(archive_path, extract_to):
    """
    Extracts a CAB (.cab) archive to the specified directory.
    Uses Windows built-in 'expand' command for extraction.
    """
    if not os.path.isfile(archive_path):
        print(f"CAB file not found: {archive_path}")
        return False
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    try:
        # Use Windows 'expand' command
        result = subprocess.run([
            'expand', archive_path, '-F:*', extract_to
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error extracting CAB file: {result.stderr}")
            return False
        print(f"Extracted CAB file to: {extract_to}")
        return True
    except Exception as e:
        print(f"Exception during CAB extraction: {e}")
        return False
