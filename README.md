# Auto-Unzip

Background Windows helper that automatically extracts new `.zip`, `.zipx`, `.7z`, `.rar`, `.tar`, `.gz`, `.bz2`, `.tgz`, `.tbz` files appearing in watched folders (Downloads by default), shows status in the console, and optionally deletes the original archive after successful extraction. Provides a tray icon (if `pystray` + `Pillow` installed) to list or add watched folders and quit.

## Features
* Automatic discovery of new ZIP, ZIPX, 7Z, RAR, TAR, GZ, BZ2, TGZ, TBZ archives via lightweight polling
* Console notifications (startup, progress updates, completion/error)
* System tray icon with minimal menu (optional if dependencies missing)
* Modular, one-function-per-file design for clarity
* Config persisted to `modules/settings.json` (watched folders, poll interval, delete flag)
* Safe fallbacks: if tray libs missing, prints to console

## Project Structure (key modules)
```
auto-unzip.py                # Entry point (orchestration only)
modules/
  config_dataclass.py        # Config dataclass
  config_default_downloads_folder.py
  config_settings_file_path.py
  config_load_config.py
  config_save_config.py
  notifications_get_notifier.py
  notifications_show_startup.py
  notifications_show_progress.py
  notifications_show_completion.py
  extract_zip.py
  extract_zipx.py            # ZIPX extraction
  extract_7z.py              # 7z extraction
  extract_rar.py             # RAR extraction
  extract_tar_gz_bz2.py      # NEW: TAR/GZ/BZ2/TGZ/TBZ extraction
  extract_archive.py         # Dispatches to all formats
  watcher_directory_watcher.py
  workflow_process_archive.py
  tray_tray_controller.py
  startup_register_startup.py
  startup_unregister_startup.py
  startup_is_registered.py
```

Each file exposes exactly one public function or class per the development rules.

## Installation
```
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

RAR support requires the `unrar` tool to be installed and available in your PATH.

## Run
```
py .\auto-unzip.py
```
You should see a startup message in the console and a tray icon (if pystray + Pillow available). Drop a `.zip`, `.zipx`, `.7z`, `.rar`, `.tar`, `.gz`, `.bz2`, `.tgz`, or `.tbz` into your Downloads folder; extraction will begin immediately into a folder named after the archive (without extension).

## Adding Watch Folders
Use the tray menu -> "Add Folder" and input a path, or edit `modules/settings.json` while the app is stopped and restart.

## Startup Registration (Optional)
To auto-run at login, you can call the helper manually (e.g. add to `main()`):
```python
from modules.startup_register_startup import register_startup
register_startup(__file__)
```
Corresponding removal: `from modules.startup_unregister_startup import unregister_startup`.

## Extending Archive Support
Add a new extractor (e.g., `extract_cab.py`) and update `extract_archive.py` to dispatch based on extension. Consider Python bindings for other formats.

## Configuration Fields
* `watch_folders`: list of absolute paths
* `poll_interval_seconds`: scan interval
* `delete_archives_after_extract`: bool

## Notes
* Polling was chosen over filesystem events to minimize dependencies; swap in `watchdog` easily if desired.
* Progress for all formats is approximate (based on file count or file sizes).
* Multiple rapid console prints approximate a progress bar.

## License
See `LICENSE`.
