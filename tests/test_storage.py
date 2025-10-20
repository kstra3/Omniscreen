"""
Test Suite for Storage Management Module

Tests screenshot storage and organization functionality.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
from core.storage import StorageManager
from config import Config


class TestStorageManager(unittest.TestCase):
    """Test cases for StorageManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config = Config()
        self.config.settings["storage"]["save_location"] = self.test_dir
        self.config.settings["storage"]["naming_pattern"] = "test_%Y%m%d_%H%M%S"
        self.config.settings["storage"]["organize_by"] = "none"
        self.config.settings["storage"]["format"] = "png"
        
        # Patch the config
        import config as config_module
        self.original_config = config_module._config_instance
        config_module._config_instance = self.config
        
        self.storage = StorageManager()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original config
        import config as config_module
        config_module._config_instance = self.original_config
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_generate_filename(self):
        """Test filename generation."""
        filename = self.storage.generate_filename()
        
        self.assertTrue(filename.startswith("test_"))
        self.assertTrue(filename.endswith(".png"))
    
    def test_generate_filename_with_window(self):
        """Test filename generation with window name."""
        filename = self.storage.generate_filename("Chrome")
        
        self.assertIn("Chrome", filename)
        self.assertTrue(filename.endswith(".png"))
    
    def test_save_screenshot(self):
        """Test screenshot saving."""
        # Create test image
        image = Image.new('RGB', (100, 100), color='red')
        
        # Save screenshot
        filepath = self.storage.save_screenshot(image, "TestWindow", "fullscreen")
        
        # Verify file was created
        self.assertTrue(Path(filepath).exists())
        
        # Verify file is an image
        saved_image = Image.open(filepath)
        self.assertEqual(saved_image.size, (100, 100))
    
    def test_get_history(self):
        """Test history retrieval."""
        # Save a screenshot first
        image = Image.new('RGB', (100, 100), color='blue')
        self.storage.save_screenshot(image, "TestApp", "window")
        
        # Get history
        history = self.storage.get_history(limit=10)
        
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        # Verify record structure
        record = history[0]
        self.assertIn('filename', record)
        self.assertIn('filepath', record)
        self.assertIn('timestamp', record)
    
    def test_organize_by_date(self):
        """Test date-based organization."""
        self.config.settings["storage"]["organize_by"] = "date"
        storage = StorageManager()
        
        filename = "test.png"
        path = storage.get_save_path(filename)
        
        # Should have year/month/day structure
        path_str = str(path)
        self.assertRegex(path_str, r'\d{4}[\\/]\d{2}[\\/]\d{2}')


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.settings["storage"]["save_location"] = self.test_dir
        
        import config as config_module
        self.original_config = config_module._config_instance
        config_module._config_instance = self.config
        
        self.storage = StorageManager()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import config as config_module
        config_module._config_instance = self.original_config
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_search_history(self):
        """Test history search."""
        # Add some test data
        image = Image.new('RGB', (50, 50), color='green')
        self.storage.save_screenshot(image, "SearchTest", "fullscreen")
        
        # Search
        results = self.storage.get_history(search_term="SearchTest")
        
        self.assertGreater(len(results), 0)
        self.assertIn("SearchTest", results[0]['window_name'])


if __name__ == '__main__':
    unittest.main()
