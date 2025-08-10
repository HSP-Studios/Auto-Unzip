"""
startup_shortcut.py
------------------
Creates or removes a shortcut to Auto-Unzip in the current user's Windows Startup folder.
"""
import os
import sys
import winshell
import pythoncom
from win32com.client import Dispatch

def get_startup_folder():
    # Get current user's Startup folder
    return winshell.startup()

def create_startup_shortcut():
    startup_dir = get_startup_folder()
    target = sys.executable
    script = os.path.abspath(sys.argv[0])
    shortcut_path = os.path.join(startup_dir, 'Auto-Unzip.lnk')
    pythoncom.CoInitialize()
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.Arguments = f'"{script}"'
    shortcut.WorkingDirectory = os.path.dirname(script)
    shortcut.IconLocation = script
    shortcut.save()

def remove_startup_shortcut():
    shortcut_path = os.path.join(get_startup_folder(), 'Auto-Unzip.lnk')
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
