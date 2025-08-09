"""
tray_tray_controller.py
-----------------------
Defines TrayController for creating an optional system tray icon with pystray
(if installed). Provides menu actions to view watched folders, add a folder, or
quit the application.
"""
from __future__ import annotations
import threading
from typing import Callable, Any

try:
    import pystray  # type: ignore
    from PIL import Image, ImageDraw  # type: ignore
except ImportError:  # pragma: no cover
    pystray = None  # type: ignore
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore

class TrayController:
    def __init__(self, get_folders: Callable[[], list], add_folder: Callable[[str], None], on_quit: Callable[[], None]):
        self.get_folders = get_folders
        self.add_folder = add_folder
        self.on_quit = on_quit
        self._icon: Any = None
        self._thread: threading.Thread | None = None

    def _create_image(self):  # pragma: no cover
        if not Image or not ImageDraw:
            return None
        img = Image.new('RGB', (64, 64), color=(30, 30, 30))
        d = ImageDraw.Draw(img)
        for i in range(8):
            x = 8 + i * 6
            d.rectangle([x, 10, x + 3, 54], fill=(200, 200, 50))
        d.rectangle([0, 0, 63, 63], outline=(255, 215, 0))
        return img

    def _build_menu(self):  # pragma: no cover
        if not pystray:
            return None
        return pystray.Menu(
            pystray.MenuItem('Watched Folders', self._show_folders),
            pystray.MenuItem('Add Folder', self._prompt_add_folder),
            pystray.MenuItem('Quit', self._quit)
        )

    def _show_folders(self, icon, item):  # pragma: no cover
        print('[Auto-Unzip] Watched Folders:')
        for f in self.get_folders():
            print(' -', f)

    def _prompt_add_folder(self, icon, item):  # pragma: no cover
        new_path = input('Enter folder path to watch: ').strip()
        if new_path:
            self.add_folder(new_path)
            print(f'[Auto-Unzip] Added watch folder: {new_path}')

    def _quit(self, icon, item):  # pragma: no cover
        self.stop()
        self.on_quit()

    def start(self):  # pragma: no cover
        if not pystray:
            print('[Auto-Unzip] pystray not installed, skipping tray icon.')
            return
        if self._icon:
            return
        image = self._create_image()
        self._icon = pystray.Icon('auto_unzip', image, 'Auto-Unzip', self._build_menu())
        self._thread = threading.Thread(target=self._icon.run, daemon=True)
        self._thread.start()

    def stop(self):  # pragma: no cover
        if self._icon:
            try:
                self._icon.stop()
            except Exception:
                pass
            self._icon = None
