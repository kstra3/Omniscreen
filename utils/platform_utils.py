"""
Platform-Specific Utilities

Provides platform-specific functionality for Windows, macOS, and Linux.
Like the different city-states of ancient Greece, each with unique customs.
"""

import platform
from typing import Optional, Dict, List
from logger import get_logger


logger = get_logger(__name__)


def get_platform_name() -> str:
    """
    Get the current platform name.
    
    Returns:
        'windows', 'macos', or 'linux'
    """
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    else:
        return "unknown"


# Platform-specific imports
_platform = get_platform_name()

if _platform == "windows":
    try:
        import win32gui
        import win32process
        import win32api
        _has_win32 = True
    except ImportError:
        logger.warning("pywin32 not available - window detection limited")
        _has_win32 = False

elif _platform == "macos":
    try:
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
            kCGWindowName,
            kCGWindowOwnerName,
            kCGWindowBounds
        )
        from AppKit import NSWorkspace
        _has_quartz = True
    except ImportError:
        logger.warning("pyobjc not available - window detection limited")
        _has_quartz = False

elif _platform == "linux":
    try:
        from Xlib import display, X
        from Xlib.error import XError
        _has_xlib = True
    except ImportError:
        logger.warning("python-xlib not available - window detection limited")
        _has_xlib = False


def get_active_window_info() -> Optional[Dict]:
    """
    Get information about the currently active window.
    
    The Oracle's vision - seeing which window holds the user's focus.
    
    Returns:
        Dictionary with window info:
        {
            'name': str,
            'process': str,
            'rect': {'left': int, 'top': int, 'width': int, 'height': int}
        }
        Returns None if unable to get window info.
    """
    try:
        if _platform == "windows":
            return _get_active_window_windows()
        elif _platform == "macos":
            return _get_active_window_macos()
        elif _platform == "linux":
            return _get_active_window_linux()
        else:
            logger.warning(f"Window detection not supported on {_platform}")
            return None
    except Exception as e:
        logger.error(f"Failed to get active window info: {e}", exc_info=True)
        return None


def _get_active_window_windows() -> Optional[Dict]:
    """Get active window info on Windows."""
    if not _has_win32:
        return None
    
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return None
        
        # Get window title
        title = win32gui.GetWindowText(hwnd)
        
        # Get process name
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            handle = win32api.OpenProcess(0x0400 | 0x0010, False, pid)
            exe_path = win32process.GetModuleFileNameEx(handle, 0)
            process_name = exe_path.split('\\')[-1].replace('.exe', '')
            win32api.CloseHandle(handle)
        except:
            process_name = "Unknown"
        
        # Get window rect
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        
        return {
            'name': title or process_name,
            'process': process_name,
            'rect': {
                'left': left,
                'top': top,
                'width': right - left,
                'height': bottom - top
            }
        }
    except Exception as e:
        logger.error(f"Windows window detection error: {e}", exc_info=True)
        return None


def _get_active_window_macos() -> Optional[Dict]:
    """Get active window info on macOS."""
    if not _has_quartz:
        return None
    
    try:
        # Get active application
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.activeApplication()
        app_name = active_app['NSApplicationName']
        
        # Get window list
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )
        
        # Find active window
        for window in window_list:
            if window.get(kCGWindowOwnerName) == app_name:
                bounds = window.get(kCGWindowBounds, {})
                name = window.get(kCGWindowName, app_name)
                
                return {
                    'name': name,
                    'process': app_name,
                    'rect': {
                        'left': int(bounds.get('X', 0)),
                        'top': int(bounds.get('Y', 0)),
                        'width': int(bounds.get('Width', 800)),
                        'height': int(bounds.get('Height', 600))
                    }
                }
        
        # Fallback if no window found
        return {
            'name': app_name,
            'process': app_name,
            'rect': {'left': 0, 'top': 0, 'width': 800, 'height': 600}
        }
        
    except Exception as e:
        logger.error(f"macOS window detection error: {e}", exc_info=True)
        return None


def _get_active_window_linux() -> Optional[Dict]:
    """Get active window info on Linux."""
    if not _has_xlib:
        return None
    
    try:
        d = display.Display()
        root = d.screen().root
        
        # Get active window
        net_active = d.intern_atom('_NET_ACTIVE_WINDOW')
        active_window_id = root.get_full_property(net_active, X.AnyPropertyType)
        
        if not active_window_id:
            return None
        
        window_id = active_window_id.value[0]
        window = d.create_resource_object('window', window_id)
        
        # Get window name
        net_wm_name = d.intern_atom('_NET_WM_NAME')
        wm_name = d.intern_atom('WM_NAME')
        
        try:
            name_prop = window.get_full_property(net_wm_name, 0)
            if name_prop:
                name = name_prop.value.decode('utf-8')
            else:
                name_prop = window.get_full_property(wm_name, 0)
                name = name_prop.value.decode('utf-8') if name_prop else "Unknown"
        except:
            name = "Unknown"
        
        # Get window geometry
        geom = window.get_geometry()
        
        # Get absolute position
        coords = window.translate_coords(root, 0, 0)
        
        return {
            'name': name,
            'process': name,  # Process name harder to get on Linux
            'rect': {
                'left': coords.x,
                'top': coords.y,
                'width': geom.width,
                'height': geom.height
            }
        }
        
    except Exception as e:
        logger.error(f"Linux window detection error: {e}", exc_info=True)
        return None


def get_all_windows() -> List[Dict]:
    """
    Get information about all visible windows.
    
    The panorama - seeing all windows in the realm.
    
    Returns:
        List of window info dictionaries
    """
    try:
        if _platform == "windows":
            return _get_all_windows_windows()
        elif _platform == "macos":
            return _get_all_windows_macos()
        elif _platform == "linux":
            return _get_all_windows_linux()
        else:
            return []
    except Exception as e:
        logger.error(f"Failed to get all windows: {e}", exc_info=True)
        return []


def _get_all_windows_windows() -> List[Dict]:
    """Get all windows on Windows."""
    if not _has_win32:
        return []
    
    windows = []
    
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                rect = win32gui.GetWindowRect(hwnd)
                left, top, right, bottom = rect
                windows.append({
                    'name': title,
                    'rect': {
                        'left': left,
                        'top': top,
                        'width': right - left,
                        'height': bottom - top
                    }
                })
    
    try:
        win32gui.EnumWindows(enum_callback, None)
    except:
        pass
    
    return windows


def _get_all_windows_macos() -> List[Dict]:
    """Get all windows on macOS."""
    if not _has_quartz:
        return []
    
    windows = []
    
    try:
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )
        
        for window in window_list:
            name = window.get(kCGWindowName)
            bounds = window.get(kCGWindowBounds, {})
            
            if name and bounds:
                windows.append({
                    'name': name,
                    'rect': {
                        'left': int(bounds.get('X', 0)),
                        'top': int(bounds.get('Y', 0)),
                        'width': int(bounds.get('Width', 0)),
                        'height': int(bounds.get('Height', 0))
                    }
                })
    except:
        pass
    
    return windows


def _get_all_windows_linux() -> List[Dict]:
    """Get all windows on Linux."""
    if not _has_xlib:
        return []
    
    windows = []
    
    try:
        d = display.Display()
        root = d.screen().root
        
        # Get window list
        net_client_list = d.intern_atom('_NET_CLIENT_LIST')
        window_ids = root.get_full_property(net_client_list, X.AnyPropertyType)
        
        if not window_ids:
            return []
        
        for window_id in window_ids.value:
            try:
                window = d.create_resource_object('window', window_id)
                
                # Get window name
                net_wm_name = d.intern_atom('_NET_WM_NAME')
                name_prop = window.get_full_property(net_wm_name, 0)
                name = name_prop.value.decode('utf-8') if name_prop else "Unknown"
                
                # Get geometry
                geom = window.get_geometry()
                coords = window.translate_coords(root, 0, 0)
                
                windows.append({
                    'name': name,
                    'rect': {
                        'left': coords.x,
                        'top': coords.y,
                        'width': geom.width,
                        'height': geom.height
                    }
                })
            except:
                continue
    except:
        pass
    
    return windows
