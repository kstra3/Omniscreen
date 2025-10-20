"""
Test Suite for Hotkey Management Module

Tests global hotkey functionality.
"""

import unittest
from unittest.mock import Mock, patch
from core.hotkey import HotkeyManager


class TestHotkeyManager(unittest.TestCase):
    """Test cases for HotkeyManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hotkey_manager = HotkeyManager()
    
    def test_parse_hotkey_string(self):
        """Test hotkey string parsing."""
        # Test simple hotkey
        keys = self.hotkey_manager.parse_hotkey_string("ctrl+s")
        self.assertIsInstance(keys, frozenset)
        self.assertEqual(len(keys), 2)
        
        # Test complex hotkey
        keys = self.hotkey_manager.parse_hotkey_string("ctrl+shift+alt+f1")
        self.assertEqual(len(keys), 4)
        
        # Test with spaces
        keys = self.hotkey_manager.parse_hotkey_string("ctrl + shift + s")
        self.assertEqual(len(keys), 3)
    
    def test_register_hotkey(self):
        """Test hotkey registration."""
        callback = Mock()
        
        result = self.hotkey_manager.register_hotkey("ctrl+t", callback)
        
        self.assertTrue(result)
        self.assertEqual(len(self.hotkey_manager.hotkeys), 1)
    
    def test_unregister_hotkey(self):
        """Test hotkey unregistration."""
        callback = Mock()
        
        self.hotkey_manager.register_hotkey("ctrl+t", callback)
        result = self.hotkey_manager.unregister_hotkey("ctrl+t")
        
        self.assertTrue(result)
        self.assertEqual(len(self.hotkey_manager.hotkeys), 0)
    
    def test_multiple_hotkeys(self):
        """Test registering multiple hotkeys."""
        callback1 = Mock()
        callback2 = Mock()
        callback3 = Mock()
        
        self.hotkey_manager.register_hotkey("ctrl+a", callback1)
        self.hotkey_manager.register_hotkey("ctrl+b", callback2)
        self.hotkey_manager.register_hotkey("shift+c", callback3)
        
        self.assertEqual(len(self.hotkey_manager.hotkeys), 3)
    
    def test_parse_function_keys(self):
        """Test parsing function keys."""
        keys = self.hotkey_manager.parse_hotkey_string("f1")
        self.assertEqual(len(keys), 1)
        
        keys = self.hotkey_manager.parse_hotkey_string("ctrl+f12")
        self.assertEqual(len(keys), 2)
    
    def test_parse_special_keys(self):
        """Test parsing special keys."""
        special_keys = [
            "enter", "tab", "space", "esc", "backspace",
            "up", "down", "left", "right"
        ]
        
        for key in special_keys:
            keys = self.hotkey_manager.parse_hotkey_string(key)
            self.assertEqual(len(keys), 1)


class TestHotkeyManagerLifecycle(unittest.TestCase):
    """Test hotkey manager lifecycle."""
    
    @patch('core.hotkey.keyboard.Listener')
    def test_start_stop(self, mock_listener):
        """Test starting and stopping the hotkey manager."""
        manager = HotkeyManager()
        
        # Mock listener
        mock_listener_instance = Mock()
        mock_listener.return_value = mock_listener_instance
        
        # Start
        manager.listener = mock_listener_instance
        manager.start()
        self.assertTrue(manager.is_running)
        
        # Stop
        manager.stop()
        self.assertFalse(manager.is_running)


if __name__ == '__main__':
    unittest.main()
