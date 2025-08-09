"""
notifications_show_completion.py
--------------------------------
Defines show_completion_toast() to print result to console only.
"""
def show_completion_toast(archive_name: str, success: bool, target_dir: str):
    title = "Auto-Unzip Success" if success else "Auto-Unzip Error"
    body = f"Extracted to {target_dir}" if success else f"Failed to extract {archive_name}"
    print(f"[Auto-Unzip] {title}: {body}")
