"""
gui_options_window.py
---------------------
Defines create_and_show_options_window() which builds and shows the PyQt6
options GUI (700x500, non-resizable) with scrollable sections for General and
Advanced settings. Provides simple controls bound to the Config object.
"""
from __future__ import annotations
import sys
from typing import Callable

try:
    from PyQt6 import QtWidgets, QtCore  # type: ignore
except ImportError:  # pragma: no cover
    QtWidgets = None  # type: ignore
    QtCore = None  # type: ignore

from .config_dataclass import Config
from .config_save_config import save_config
from .config_settings_file_path import get_settings_file_path

_window_ref = None  # prevent GC

def create_and_show_options_window(cfg: Config, on_quit: Callable[[], None], on_reload: Callable[[], None] | None = None):
    global _window_ref
    if QtWidgets is None:
        print('[Auto-Unzip] PyQt6 not installed. Install with pip install PyQt6.')
        return

    # If window already exists just raise and focus it
    if _window_ref is not None:
        try:
            _window_ref.show()
            _window_ref.raise_()
            _window_ref.activateWindow()
        except Exception:
            pass
        return

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    class OptionsWindow(QtWidgets.QWidget):
        def closeEvent(self, event):  # type: ignore
            # Just hide; do not quit app. User can reopen from tray.
            self.hide()
            event.ignore()

    window = OptionsWindow()
    window.setWindowTitle('Auto-Unzip Options')
    window.setFixedSize(700, 500)

    layout = QtWidgets.QVBoxLayout(window)

    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    inner = QtWidgets.QWidget()
    inner_layout = QtWidgets.QVBoxLayout(inner)

    # General Section
    general_group = QtWidgets.QGroupBox('General')
    general_layout = QtWidgets.QFormLayout(general_group)

    delete_checkbox = QtWidgets.QCheckBox('Delete archives after extraction')
    delete_checkbox.setChecked(cfg.delete_archives_after_extract)
    def _toggle_delete(state):
        cfg.delete_archives_after_extract = state == QtCore.Qt.CheckState.Checked
        save_config(cfg)
    delete_checkbox.stateChanged.connect(_toggle_delete)  # type: ignore
    general_layout.addRow(delete_checkbox)

    # Poll interval
    poll_spin = QtWidgets.QDoubleSpinBox()
    poll_spin.setRange(0.5, 60.0)
    poll_spin.setSingleStep(0.5)
    poll_spin.setValue(cfg.poll_interval_seconds)
    def _poll_changed(val: float):
        cfg.poll_interval_seconds = float(val)
        save_config(cfg)
    poll_spin.valueChanged.connect(_poll_changed)  # type: ignore
    general_layout.addRow('Poll Interval (s):', poll_spin)

    # Watched folders list
    folders_list = QtWidgets.QListWidget()
    folders_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)  # allow multi-select
    for f in cfg.watch_folders:
        folders_list.addItem(f)
    add_btn = QtWidgets.QPushButton('Add Folder')
    remove_btn = QtWidgets.QPushButton('Remove Selected')
    def _add_folder():
        dlg = QtWidgets.QFileDialog(window)
        dlg.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)  # type: ignore
        if dlg.exec():  # type: ignore
            paths = dlg.selectedFiles()  # type: ignore
            if paths:
                path = paths[0]
                # Normalize path to Windows-style backslashes uniformly
                try:
                    import pathlib
                    path = str(pathlib.PureWindowsPath(path))
                except Exception:
                    pass
                if path not in cfg.watch_folders:
                    cfg.watch_folders.append(path)
                    folders_list.addItem(path)
                    save_config(cfg)
    def _remove_selected():
        # Collect selected items first (can't modify while iterating selection)
        selected = list(folders_list.selectedItems())
        if not selected:
            return
        removed_any = False
        for item in selected:
            path = item.text()
            if path in cfg.watch_folders:
                try:
                    cfg.watch_folders.remove(path)
                except ValueError:
                    pass
                row = folders_list.row(item)
                folders_list.takeItem(row)
                removed_any = True
        if removed_any:
            save_config(cfg)
    remove_btn.clicked.connect(_remove_selected)  # type: ignore
    add_btn.clicked.connect(_add_folder)  # type: ignore
    general_layout.addRow('Watched Folders:', folders_list)
    btn_row = QtWidgets.QHBoxLayout()
    btn_row.addWidget(add_btn)
    btn_row.addWidget(remove_btn)
    btn_row.addStretch(1)
    general_layout.addRow(btn_row)

    inner_layout.addWidget(general_group)

    # Advanced Section
    advanced_group = QtWidgets.QGroupBox('Advanced')
    advanced_layout = QtWidgets.QVBoxLayout(advanced_group)
    open_cfg_btn = QtWidgets.QPushButton('Open Configuration File')
    def _open_config_file():
        try:
            path = get_settings_file_path()
            # Use platform-specific open
            if sys.platform.startswith('win'):
                import os
                os.startfile(path)  # type: ignore
            elif sys.platform == 'darwin':
                import subprocess
                subprocess.Popen(['open', path])
            else:
                import subprocess
                subprocess.Popen(['xdg-open', path])
        except Exception as e:
            try:
                from PyQt6 import QtWidgets  # type: ignore
                QtWidgets.QMessageBox.warning(window, 'Error', f'Could not open config file: {e}')
            except Exception:
                print(f'[Auto-Unzip] Could not open config file: {e}')
    open_cfg_btn.clicked.connect(_open_config_file)  # type: ignore
    advanced_layout.addWidget(open_cfg_btn)
    advanced_layout.addWidget(QtWidgets.QLabel('Configuration file opens in your default editor.'))
    inner_layout.addWidget(advanced_group)

    inner_layout.addStretch(1)
    scroll.setWidget(inner)
    layout.addWidget(scroll)

    # Bottom buttons
    button_bar = QtWidgets.QHBoxLayout()
    quit_btn = QtWidgets.QPushButton('Quit')
    reload_btn = QtWidgets.QPushButton('Reload App')
    def _reload():
        if on_reload:
            on_reload()
    reload_btn.clicked.connect(_reload)  # type: ignore
    def _quit():
        reply = QtWidgets.QMessageBox.question(window, 'Quit Auto-Unzip', 'Are you sure you want to quit?',
                                               QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                               QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            on_quit()
            window.close()
    quit_btn.clicked.connect(_quit)  # type: ignore
    button_bar.addStretch(1)
    button_bar.addWidget(reload_btn)
    button_bar.addWidget(quit_btn)
    layout.addLayout(button_bar)

    window.show()
    window.raise_()
    window.activateWindow()
    try:
        # For Windows specifically, ensure focus
        window.setWindowState(window.windowState() & ~QtCore.Qt.WindowState.WindowMinimized | QtCore.Qt.WindowState.WindowActive)
    except Exception:
        pass
    _window_ref = window
    app.processEvents()
