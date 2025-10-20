"""
Core Module

The heart of OmniScreen - where the magic of capturing moments happens.
Like the sacred fire of Hestia, this module keeps the core functionality burning.
"""

from .capture import ScreenCapture, CaptureMode
from .storage import StorageManager
from .clipboard import ClipboardManager
from .hotkey import HotkeyManager

__all__ = [
    'ScreenCapture',
    'CaptureMode',
    'StorageManager',
    'ClipboardManager',
    'HotkeyManager'
]
