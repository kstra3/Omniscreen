"""
GUI Module

The visual interface of OmniScreen, adorned with ancient Greek aesthetics.
The temple where users commune with the application.
"""

from .main_window import MainWindow
from .theme import GreekTheme
from .history import HistoryPanel
from .settings import SettingsDialog
from .region_selector import RegionSelector

__all__ = [
    'MainWindow',
    'GreekTheme',
    'HistoryPanel',
    'SettingsDialog',
    'RegionSelector'
]
