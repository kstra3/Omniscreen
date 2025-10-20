"""
Window Information Provider

Provides detailed window information for screenshot organization and naming.
"""

from typing import Optional, Dict, List
from utils.platform_utils import get_active_window_info, get_all_windows
from logger import get_logger


logger = get_logger(__name__)


class WindowInfoProvider:
    """
    Provides window information services.
    
    The all-seeing eye - gathering knowledge about windows in the system.
    """
    
    def __init__(self):
        """Initialize window info provider."""
        logger.debug("WindowInfoProvider initialized")
    
    def get_active_window(self) -> Optional[Dict]:
        """
        Get information about the currently active window.
        
        Returns:
            Window info dictionary or None
        """
        return get_active_window_info()
    
    def get_all_visible_windows(self) -> List[Dict]:
        """
        Get information about all visible windows.
        
        Returns:
            List of window info dictionaries
        """
        return get_all_windows()
    
    def find_window_by_name(self, name: str) -> Optional[Dict]:
        """
        Find a window by its name.
        
        Args:
            name: Window name to search for
        
        Returns:
            Window info dictionary or None if not found
        """
        windows = self.get_all_visible_windows()
        
        # Try exact match first
        for window in windows:
            if window.get('name', '').lower() == name.lower():
                return window
        
        # Try partial match
        for window in windows:
            if name.lower() in window.get('name', '').lower():
                return window
        
        logger.debug(f"Window not found: {name}")
        return None
    
    def sanitize_window_name(self, name: str) -> str:
        """
        Sanitize window name for use in filenames.
        
        Args:
            name: Window name to sanitize
        
        Returns:
            Sanitized name safe for filenames
        """
        # Remove invalid filename characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Limit length
        name = name[:50]
        
        # Remove leading/trailing whitespace
        name = name.strip()
        
        return name or "Unknown"
