"""
Configuration Management Module

Manages application settings with persistence, inspired by the organized
record-keeping of ancient Greek scribes who maintained detailed scrolls.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict
from appdirs import user_config_dir, user_data_dir


class Config:
    """
    Configuration manager following the principle of 'Τάξις' (Order).
    Manages all application settings with proper defaults and persistence.
    """
    
    # Default configuration - The foundational pillars of OmniScreen
    DEFAULT_CONFIG = {
        "hotkeys": {
            "quick_capture": "ctrl+shift+s",
            "window_capture": "ctrl+shift+w",
            "region_capture": "ctrl+shift+r"
        },
        "storage": {
            "save_location": "",  # Will be set to user's Pictures/OmniScreen
            "naming_pattern": "%Y%m%d_%H%M%S_{window}",
            "organize_by": "date",  # Options: date, application, none
            "format": "png"  # Options: png, jpg, bmp
        },
        "auto_delete": {
            "enabled": False,
            "days_to_keep": 30,
            "check_interval_hours": 24
        },
        "clipboard": {
            "copy_on_capture": False,
            "save_and_copy": True
        },
        "notifications": {
            "enabled": True,
            "sound": True,
            "sound_file": "default"
        },
        "ui": {
            "theme": "greek_light",
            "font_family": "EB Garamond",
            "font_size": 12,
            "high_contrast": False,
            "language": "en"
        },
        "history": {
            "max_items": 1000,
            "thumbnail_size": 200
        },
        "background_service": {
            "enabled": True,
            "start_on_boot": False
        }
    }
    
    def __init__(self):
        """Initialize configuration with proper paths."""
        self.app_name = "OmniScreen"
        self.config_dir = Path(user_config_dir(self.app_name))
        self.data_dir = Path(user_data_dir(self.app_name))
        self.config_file = self.config_dir / "config.json"
        
        # Create directories if they don't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create configuration
        self.settings = self._load_config()
        
        # Set default save location if not specified
        if not self.settings["storage"]["save_location"]:
            self.settings["storage"]["save_location"] = str(
                Path.home() / "Pictures" / "OmniScreen"
            )
            self._ensure_save_location()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create with defaults.
        Like retrieving wisdom from the Library of Alexandria.
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to add any new settings
                return self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create new config file
            self.save()
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """
        Recursively merge loaded config with defaults.
        Ensures all keys exist while preserving user settings.
        """
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _ensure_save_location(self):
        """Ensure the screenshot save location exists."""
        save_path = Path(self.settings["storage"]["save_location"])
        save_path.mkdir(parents=True, exist_ok=True)
    
    def save(self):
        """
        Persist configuration to disk.
        Inscribe our settings into the eternal stone of storage.
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, *keys: str) -> Any:
        """
        Get a configuration value by path.
        
        Args:
            *keys: Sequence of keys to traverse (e.g., "storage", "format")
        
        Returns:
            The configuration value or None if not found
        """
        value = self.settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def set(self, *keys: str, value: Any):
        """
        Set a configuration value by path.
        
        Args:
            *keys: Sequence of keys to traverse, last key is the one to set
            value: The value to set
        """
        settings = self.settings
        for key in keys[:-1]:
            if key not in settings:
                settings[key] = {}
            settings = settings[key]
        settings[keys[-1]] = value
        self.save()
    
    def get_screenshot_path(self) -> Path:
        """Get the base path for screenshot storage."""
        return Path(self.settings["storage"]["save_location"])
    
    def get_logs_path(self) -> Path:
        """Get the path for log files."""
        logs_path = self.data_dir / "logs"
        logs_path.mkdir(parents=True, exist_ok=True)
        return logs_path
    
    def get_history_db_path(self) -> Path:
        """Get the path for the history database."""
        return self.data_dir / "history.db"
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.settings = self.DEFAULT_CONFIG.copy()
        self.save()


# Global configuration instance - The Oracle of OmniScreen
_config_instance = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
