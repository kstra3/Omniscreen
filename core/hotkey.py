"""
Global Hotkey Management Module

Implements system-wide hotkey detection and handling, allowing users to
trigger screenshots from anywhere. Like the call of Athena's horn,
heard across all of Greece.
"""

from pynput import keyboard
from typing import Callable, Dict, Set, Optional
from logger import get_logger
import threading


logger = get_logger(__name__)


class HotkeyManager:
    """
    Manages global hotkey registration and detection.
    
    The ever-vigilant sentinel, listening for the user's command
    from any corner of the system.
    """
    
    def __init__(self):
        """Initialize hotkey manager."""
        self.listener: Optional[keyboard.Listener] = None
        self.hotkeys: Dict[frozenset, Callable] = {}
        self.current_keys: Set[keyboard.Key] = set()
        self.is_running = False
        
        logger.info("HotkeyManager initialized")
    
    def parse_hotkey_string(self, hotkey_str: str) -> frozenset:
        """
        Parse hotkey string into a set of keys.
        
        Examples:
            "ctrl+shift+s" -> {Key.ctrl, Key.shift, KeyCode(char='s')}
            "alt+f1" -> {Key.alt, Key.f1}
        
        Args:
            hotkey_str: Hotkey string (e.g., "ctrl+shift+s")
        
        Returns:
            Frozen set of keyboard keys
        """
        keys = []
        parts = hotkey_str.lower().split('+')
        
        for part in parts:
            part = part.strip()
            
            # Map common key names
            key_map = {
                'ctrl': keyboard.Key.ctrl,
                'control': keyboard.Key.ctrl,
                'shift': keyboard.Key.shift,
                'alt': keyboard.Key.alt,
                'cmd': keyboard.Key.cmd,
                'command': keyboard.Key.cmd,
                'super': keyboard.Key.cmd,
                'win': keyboard.Key.cmd,
                'windows': keyboard.Key.cmd,
                'tab': keyboard.Key.tab,
                'enter': keyboard.Key.enter,
                'return': keyboard.Key.enter,
                'esc': keyboard.Key.esc,
                'escape': keyboard.Key.esc,
                'space': keyboard.Key.space,
                'backspace': keyboard.Key.backspace,
                'delete': keyboard.Key.delete,
                'up': keyboard.Key.up,
                'down': keyboard.Key.down,
                'left': keyboard.Key.left,
                'right': keyboard.Key.right,
            }
            
            # Handle function keys
            if part.startswith('f') and len(part) > 1 and part[1:].isdigit():
                try:
                    f_num = int(part[1:])
                    if 1 <= f_num <= 12:
                        keys.append(getattr(keyboard.Key, f'f{f_num}'))
                        continue
                except:
                    pass
            
            if part in key_map:
                keys.append(key_map[part])
            elif len(part) == 1:
                # Single character
                keys.append(keyboard.KeyCode.from_char(part))
            else:
                logger.warning(f"Unknown key in hotkey: {part}")
        
        return frozenset(keys)
    
    def register_hotkey(self, hotkey_str: str, callback: Callable) -> bool:
        """
        Register a global hotkey with a callback function.
        
        The binding of keys to divine will.
        
        Args:
            hotkey_str: Hotkey string (e.g., "ctrl+shift+s")
            callback: Function to call when hotkey is pressed
        
        Returns:
            True if registration successful
        """
        try:
            keys = self.parse_hotkey_string(hotkey_str)
            self.hotkeys[keys] = callback
            logger.info(f"Hotkey registered: {hotkey_str} -> {callback.__name__}")
            return True
        except Exception as e:
            logger.error(f"Failed to register hotkey '{hotkey_str}': {e}", exc_info=True)
            return False
    
    def unregister_hotkey(self, hotkey_str: str) -> bool:
        """
        Unregister a hotkey.
        
        Args:
            hotkey_str: Hotkey string to unregister
        
        Returns:
            True if unregistration successful
        """
        try:
            keys = self.parse_hotkey_string(hotkey_str)
            if keys in self.hotkeys:
                del self.hotkeys[keys]
                logger.info(f"Hotkey unregistered: {hotkey_str}")
                return True
            else:
                logger.warning(f"Hotkey not found: {hotkey_str}")
                return False
        except Exception as e:
            logger.error(f"Failed to unregister hotkey '{hotkey_str}': {e}", exc_info=True)
            return False
    
    def _normalize_key(self, key) -> keyboard.Key:
        """Normalize key representation for comparison."""
        try:
            # Try to convert to KeyCode if it's a character
            if hasattr(key, 'char') and key.char:
                return keyboard.KeyCode.from_char(key.char.lower())
            return key
        except:
            return key
    
    def _on_press(self, key):
        """Handle key press event."""
        try:
            normalized_key = self._normalize_key(key)
            self.current_keys.add(normalized_key)
            
            # Check if current combination matches any registered hotkey
            current_combo = frozenset(self.current_keys)
            
            for hotkey_combo, callback in self.hotkeys.items():
                if current_combo == hotkey_combo:
                    logger.debug(f"Hotkey triggered: {hotkey_combo}")
                    # Execute callback in a separate thread to avoid blocking
                    threading.Thread(target=callback, daemon=True).start()
                    
        except Exception as e:
            logger.error(f"Error in key press handler: {e}", exc_info=True)
    
    def _on_release(self, key):
        """Handle key release event."""
        try:
            normalized_key = self._normalize_key(key)
            self.current_keys.discard(normalized_key)
        except Exception as e:
            logger.error(f"Error in key release handler: {e}", exc_info=True)
    
    def start(self):
        """
        Start listening for hotkeys.
        
        Awaken the sentinel to begin its eternal watch.
        """
        if self.is_running:
            logger.warning("HotkeyManager already running")
            return
        
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self.listener.start()
            self.is_running = True
            logger.info("HotkeyManager started - listening for hotkeys")
        except Exception as e:
            logger.error(f"Failed to start HotkeyManager: {e}", exc_info=True)
            raise
    
    def stop(self):
        """
        Stop listening for hotkeys.
        
        Release the sentinel from its duty.
        """
        if not self.is_running:
            return
        
        try:
            if self.listener:
                self.listener.stop()
                self.listener = None
            self.is_running = False
            self.current_keys.clear()
            logger.info("HotkeyManager stopped")
        except Exception as e:
            logger.error(f"Error stopping HotkeyManager: {e}", exc_info=True)
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
