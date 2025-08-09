"""
tray_tray_controller.py
-----------------------
Defines TrayController for creating an optional system tray icon with pystray
(if installed). Provides a single menu entry "Options" which opens the options
GUI window. The GUI itself will offer controls and a Quit button.
"""
from __future__ import annotations
import threading
import queue
from typing import Callable, Any, Optional

try:
    import pystray  # type: ignore
    from PIL import Image, ImageDraw  # type: ignore
except ImportError:  # pragma: no cover
    pystray = None  # type: ignore
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore

class TrayController:
    def __init__(self, open_options: Callable[[], None]):
        self.open_options = open_options
        self._icon: Any = None
        self._thread: Optional[threading.Thread] = None
        self._action_queue: "queue.Queue[Callable[[], None]]" = queue.Queue()
        self._running = False

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
            pystray.MenuItem('Options', self._open_options)
        )

    def _open_options(self, icon=None, item=None):  # pragma: no cover
        # Dispatch to main thread via queue to avoid GUI creation from tray thread
        self._action_queue.put(self.open_options)

    def start(self):  # pragma: no cover
        if not pystray:
            print('[Auto-Unzip] pystray not installed, skipping tray icon.')
            return
        if self._icon:
            return
        image = self._create_image()
        self._icon = pystray.Icon('auto_unzip', image, 'Auto-Unzip', self._build_menu())
        # Set click handler (left-click) if library supports
        try:
            self._icon.visible = True  # precreate
            self._icon.run_detached()
        except Exception:
            # fallback to thread run
            self._thread = threading.Thread(target=self._icon.run, daemon=True)
            self._thread.start()
        self._running = True
        # Start a pump thread to execute queued actions in main context
        t = threading.Thread(target=self._pump_actions, daemon=True)
        t.start()

    def _pump_actions(self):  # pragma: no cover
        while self._running:
            try:
                action = self._action_queue.get(timeout=0.5)
            except Exception:
                continue
            try:
                action()
            except Exception:
                pass

    def stop(self):  # pragma: no cover
        self._running = False
        if self._icon:
            try:
                self._icon.stop()
            except Exception:
                pass
            self._icon = None
