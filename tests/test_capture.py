"""
Test Suite for Screenshot Capture Module

Tests the core screenshot capture functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
from core.capture import ScreenCapture, CaptureMode


class TestScreenCapture(unittest.TestCase):
    """Test cases for ScreenCapture class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.capture = ScreenCapture()
    
    @patch('core.capture.mss.mss')
    def test_capture_fullscreen(self, mock_mss):
        """Test fullscreen capture."""
        # Mock MSS screenshot
        mock_screenshot = Mock()
        mock_screenshot.size = (1920, 1080)
        mock_screenshot.bgra = b'\x00' * (1920 * 1080 * 4)
        
        mock_sct = Mock()
        mock_sct.monitors = [
            {},  # All monitors combined
            {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
        ]
        mock_sct.grab.return_value = mock_screenshot
        mock_mss.return_value = mock_sct
        
        # Create new capture instance with mock
        capture = ScreenCapture()
        capture.sct = mock_sct
        
        # Test capture
        image, window_name = capture.capture_fullscreen()
        
        self.assertIsInstance(image, Image.Image)
        self.assertIsNone(window_name)
        self.assertEqual(image.size, (1920, 1080))
    
    def test_get_monitors(self):
        """Test getting monitor information."""
        monitors = self.capture.get_monitors()
        
        self.assertIsInstance(monitors, list)
        self.assertGreater(len(monitors), 0)
        
        for monitor in monitors:
            self.assertIn('index', monitor)
            self.assertIn('left', monitor)
            self.assertIn('top', monitor)
            self.assertIn('width', monitor)
            self.assertIn('height', monitor)
    
    def test_capture_mode_enum(self):
        """Test CaptureMode enum."""
        self.assertEqual(CaptureMode.FULLSCREEN.value, "fullscreen")
        self.assertEqual(CaptureMode.WINDOW.value, "window")
        self.assertEqual(CaptureMode.REGION.value, "region")
    
    @patch('core.capture.mss.mss')
    def test_capture_region(self, mock_mss):
        """Test region capture."""
        # Mock MSS screenshot
        mock_screenshot = Mock()
        mock_screenshot.size = (800, 600)
        mock_screenshot.bgra = b'\x00' * (800 * 600 * 4)
        
        mock_sct = Mock()
        mock_sct.grab.return_value = mock_screenshot
        mock_mss.return_value = mock_sct
        
        capture = ScreenCapture()
        capture.sct = mock_sct
        
        # Test region capture
        image, window_name = capture.capture_region(100, 100, 800, 600)
        
        self.assertIsInstance(image, Image.Image)
        self.assertIsNone(window_name)
        self.assertEqual(image.size, (800, 600))
    
    def test_capture_region_invalid_dimensions(self):
        """Test region capture with invalid dimensions."""
        with self.assertRaises(ValueError):
            self.capture.capture_region(0, 0, 0, 0)
        
        with self.assertRaises(ValueError):
            self.capture.capture_region(0, 0, -100, 100)


class TestCaptureIntegration(unittest.TestCase):
    """Integration tests for capture functionality."""
    
    def test_capture_dispatch(self):
        """Test capture method dispatches correctly."""
        capture = ScreenCapture()
        
        # Test that capture method works with different modes
        # (We won't actually capture, just verify the method exists and accepts params)
        
        self.assertTrue(hasattr(capture, 'capture'))
        self.assertTrue(callable(capture.capture))


if __name__ == '__main__':
    unittest.main()
