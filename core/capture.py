"""
Screenshot Capture Module

Implements the core screenshot functionality, capturing the essence of
moments like Perseus capturing the reflection of Medusa in his shield.
"""

import mss
import mss.tools
from enum import Enum
from typing import Optional, Tuple, List
from PIL import Image
import io
from logger import get_logger
from utils.platform_utils import get_active_window_info, get_all_windows


logger = get_logger(__name__)


class CaptureMode(Enum):
    """
    Screenshot capture modes - The three paths of Heracles.
    """
    FULLSCREEN = "fullscreen"  # Capture entire screen - see all like Zeus from Olympus
    WINDOW = "window"          # Capture specific window - focus like Athena
    REGION = "region"          # Capture custom region - precision like Apollo's arrow


class ScreenCapture:
    """
    Main screenshot capture engine.
    
    Uses the power of MSS (Modern Screenshot System) for fast, efficient
    captures across all platforms. Like Argus Panoptes with his hundred eyes,
    this class sees all screens.
    """
    
    def __init__(self):
        """Initialize the capture engine."""
        self.sct = mss.mss()
        logger.info(f"ScreenCapture initialized | Monitors detected: {len(self.sct.monitors) - 1}")
    
    def get_monitors(self) -> List[dict]:
        """
        Get information about all connected monitors.
        
        Returns:
            List of monitor dictionaries with position and size info
            (Index 0 is all monitors combined, 1+ are individual monitors)
        """
        # MSS returns monitor 0 as all monitors combined
        monitors = []
        for i, monitor in enumerate(self.sct.monitors):
            if i == 0:
                continue  # Skip the combined monitor
            monitors.append({
                'index': i,
                'left': monitor['left'],
                'top': monitor['top'],
                'width': monitor['width'],
                'height': monitor['height']
            })
        logger.debug(f"Retrieved {len(monitors)} monitor(s)")
        return monitors
    
    def capture_fullscreen(self, monitor: int = 0) -> Tuple[Image.Image, Optional[str]]:
        """
        Capture the entire screen or a specific monitor.
        
        The grand vista - like viewing the Parthenon from the Acropolis.
        
        Args:
            monitor: Monitor index (0 for all monitors, 1+ for specific monitor)
        
        Returns:
            Tuple of (PIL Image, window_name) - window_name is None for fullscreen
        """
        try:
            logger.debug(f"Capturing fullscreen | Monitor: {monitor}")
            
            # Capture the specified monitor
            screenshot = self.sct.grab(self.sct.monitors[monitor])
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            
            logger.info(f"Fullscreen captured successfully | Size: {img.size}")
            return img, None
            
        except Exception as e:
            logger.error(f"Failed to capture fullscreen: {e}", exc_info=True)
            raise
    
    def capture_window(self, window_name: Optional[str] = None) -> Tuple[Image.Image, Optional[str]]:
        """
        Capture a specific window.
        
        Focus on the chosen - like the Oracle focusing on a specific prophecy.
        
        Args:
            window_name: Name of window to capture (None for active window)
        
        Returns:
            Tuple of (PIL Image, window_name)
        """
        try:
            # Get window information
            if window_name:
                logger.debug(f"Capturing specific window: {window_name}")
                # TODO: Implement window search by name
                # For now, fall back to active window
                window_info = get_active_window_info()
            else:
                logger.debug("Capturing active window")
                window_info = get_active_window_info()
            
            if not window_info or 'rect' not in window_info:
                logger.warning("Could not get window info, falling back to fullscreen")
                return self.capture_fullscreen()
            
            rect = window_info['rect']
            name = window_info.get('name', 'Unknown')
            
            logger.debug(f"Window rect: {rect}")
            
            # Capture the window region
            monitor = {
                'left': rect['left'],
                'top': rect['top'],
                'width': rect['width'],
                'height': rect['height']
            }
            
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            
            logger.info(f"Window captured successfully | Name: {name} | Size: {img.size}")
            return img, name
            
        except Exception as e:
            logger.error(f"Failed to capture window: {e}", exc_info=True)
            raise
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> Tuple[Image.Image, Optional[str]]:
        """
        Capture a specific screen region.
        
        Precision targeting - like Artemis drawing her bow at the exact target.
        
        Args:
            x: Left coordinate
            y: Top coordinate
            width: Region width
            height: Region height
        
        Returns:
            Tuple of (PIL Image, None) - no window name for region captures
        """
        try:
            logger.debug(f"Capturing region | x={x}, y={y}, w={width}, h={height}")
            
            # Validate region
            if width <= 0 or height <= 0:
                raise ValueError(f"Invalid region dimensions: {width}x{height}")
            
            monitor = {
                'left': x,
                'top': y,
                'width': width,
                'height': height
            }
            
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            
            logger.info(f"Region captured successfully | Size: {img.size}")
            return img, None
            
        except Exception as e:
            logger.error(f"Failed to capture region: {e}", exc_info=True)
            raise
    
    def capture(self, mode: CaptureMode, **kwargs) -> Tuple[Image.Image, Optional[str]]:
        """
        Universal capture method - dispatch to appropriate capture function.
        
        The crossroads where all paths converge.
        
        Args:
            mode: Capture mode (FULLSCREEN, WINDOW, or REGION)
            **kwargs: Mode-specific arguments
                - monitor: int (for FULLSCREEN)
                - window_name: str (for WINDOW)
                - x, y, width, height: int (for REGION)
        
        Returns:
            Tuple of (PIL Image, optional window_name)
        """
        logger.debug(f"Capture requested | Mode: {mode.value}")
        
        if mode == CaptureMode.FULLSCREEN:
            monitor = kwargs.get('monitor', 0)
            return self.capture_fullscreen(monitor)
        
        elif mode == CaptureMode.WINDOW:
            window_name = kwargs.get('window_name')
            return self.capture_window(window_name)
        
        elif mode == CaptureMode.REGION:
            x = kwargs.get('x')
            y = kwargs.get('y')
            width = kwargs.get('width')
            height = kwargs.get('height')
            
            if None in (x, y, width, height):
                raise ValueError("Region capture requires x, y, width, and height")
            
            return self.capture_region(x, y, width, height)
        
        else:
            raise ValueError(f"Unknown capture mode: {mode}")
    
    def __del__(self):
        """Clean up MSS instance."""
        try:
            if hasattr(self, 'sct'):
                self.sct.close()
                logger.debug("ScreenCapture cleaned up")
        except:
            pass
