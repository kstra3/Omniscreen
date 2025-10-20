"""
Utilities Module

Helper functions and platform-specific utilities.
The tools of Hephaestus, crafted for specific purposes.
"""

from .platform_utils import (
    get_active_window_info,
    get_all_windows,
    get_platform_name
)
from .notification import NotificationManager
from .window_info import WindowInfoProvider

__all__ = [
    'get_active_window_info',
    'get_all_windows',
    'get_platform_name',
    'NotificationManager',
    'WindowInfoProvider'
]
