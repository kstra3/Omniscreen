"""
Storage Management Module

Handles the organization and persistence of screenshots, following the
systematic archival methods of ancient Greek librarians at Alexandria.
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from PIL import Image
from config import get_config
from logger import get_logger


logger = get_logger(__name__)


class StorageManager:
    """
    Manages screenshot storage, organization, and history tracking.
    
    Like the keepers of the Library of Alexandria, this class ensures
    every screenshot is properly catalogued and preserved.
    """
    
    def __init__(self):
        """Initialize storage manager."""
        self.config = get_config()
        self.base_path = self.config.get_screenshot_path()
        self.db_path = self.config.get_history_db_path()
        
        # Ensure base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info(f"StorageManager initialized | Base path: {self.base_path}")
    
    def _init_database(self):
        """
        Initialize SQLite database for screenshot history.
        
        Creates the eternal scrolls where our history is written.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create screenshots table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS screenshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL UNIQUE,
                    window_name TEXT,
                    capture_mode TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    width INTEGER,
                    height INTEGER,
                    file_size INTEGER,
                    tags TEXT,
                    notes TEXT
                )
            """)
            
            # Create index for faster searches
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON screenshots(timestamp DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_window_name 
                ON screenshots(window_name)
            """)
            
            conn.commit()
            conn.close()
            
            logger.debug("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}", exc_info=True)
            raise
    
    def generate_filename(self, window_name: Optional[str] = None) -> str:
        """
        Generate filename based on configured pattern.
        
        The naming ceremony - every screenshot receives its proper name.
        
        Args:
            window_name: Name of captured window (if applicable)
        
        Returns:
            Generated filename
        """
        pattern = self.config.get("storage", "naming_pattern")
        format_ext = self.config.get("storage", "format")
        
        # Replace datetime placeholders
        filename = datetime.now().strftime(pattern)
        
        # Replace window name placeholder
        if window_name:
            # Sanitize window name for filename
            safe_name = "".join(c for c in window_name if c.isalnum() or c in (' ', '-', '_'))
            safe_name = safe_name.strip()[:50]  # Limit length
            filename = filename.replace("{window}", safe_name)
        else:
            filename = filename.replace("{window}", "screen")
        
        # Add extension
        filename = f"{filename}.{format_ext}"
        
        return filename
    
    def get_save_path(self, filename: str) -> Path:
        """
        Get full save path with organization structure.
        
        Args:
            filename: Base filename
        
        Returns:
            Full path including organized directory structure
        """
        organize_by = self.config.get("storage", "organize_by")
        
        if organize_by == "date":
            # Organize by date: YYYY/MM/DD/
            date_path = datetime.now().strftime("%Y/%m/%d")
            full_path = self.base_path / date_path
        elif organize_by == "application":
            # Extract application name from filename
            # Assumes filename contains window name
            parts = filename.split('_')
            app_name = parts[-1].replace('.png', '').replace('.jpg', '') if len(parts) > 1 else "unknown"
            full_path = self.base_path / app_name
        else:
            # No organization
            full_path = self.base_path
        
        # Ensure directory exists
        full_path.mkdir(parents=True, exist_ok=True)
        
        return full_path / filename
    
    def save_screenshot(self, image: Image.Image, window_name: Optional[str] = None, 
                       mode: str = "fullscreen") -> str:
        """
        Save screenshot to disk and add to history database.
        
        The sacred act of preservation.
        
        Args:
            image: PIL Image to save
            window_name: Name of captured window
            mode: Capture mode used
        
        Returns:
            Full path where screenshot was saved
        """
        try:
            # Generate filename and path
            filename = self.generate_filename(window_name)
            filepath = self.get_save_path(filename)
            
            # Handle duplicate filenames
            counter = 1
            original_filepath = filepath
            while filepath.exists():
                stem = original_filepath.stem
                suffix = original_filepath.suffix
                filepath = original_filepath.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Save image
            format_type = self.config.get("storage", "format").upper()
            if format_type == "JPG":
                format_type = "JPEG"
            
            image.save(filepath, format=format_type, quality=95, optimize=True)
            
            # Get file info
            file_size = filepath.stat().st_size
            width, height = image.size
            
            # Add to database
            self._add_to_history(
                filename=filepath.name,
                filepath=str(filepath),
                window_name=window_name,
                capture_mode=mode,
                width=width,
                height=height,
                file_size=file_size
            )
            
            logger.info(f"Screenshot saved | Path: {filepath} | Size: {file_size} bytes")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}", exc_info=True)
            raise
    
    def _add_to_history(self, filename: str, filepath: str, window_name: Optional[str],
                       capture_mode: str, width: int, height: int, file_size: int):
        """Add screenshot entry to history database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO screenshots 
                (filename, filepath, window_name, capture_mode, width, height, file_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (filename, filepath, window_name, capture_mode, width, height, file_size))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Screenshot added to history | File: {filename}")
            
        except sqlite3.IntegrityError:
            # Duplicate filepath, already exists
            logger.warning(f"Screenshot already in history: {filepath}")
        except Exception as e:
            logger.error(f"Failed to add screenshot to history: {e}", exc_info=True)
    
    def get_history(self, limit: int = 100, offset: int = 0, 
                   search_term: Optional[str] = None) -> List[Dict]:
        """
        Retrieve screenshot history from database.
        
        Consulting the scrolls of history.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip (for pagination)
            search_term: Optional search term for filtering
        
        Returns:
            List of screenshot record dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute("""
                    SELECT * FROM screenshots 
                    WHERE filename LIKE ? OR window_name LIKE ? OR tags LIKE ? OR notes LIKE ?
                    ORDER BY timestamp DESC 
                    LIMIT ? OFFSET ?
                """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", 
                      f"%{search_term}%", limit, offset))
            else:
                cursor.execute("""
                    SELECT * FROM screenshots 
                    ORDER BY timestamp DESC 
                    LIMIT ? OFFSET ?
                """, (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            history = [dict(row) for row in rows]
            
            logger.debug(f"Retrieved {len(history)} history records")
            return history
            
        except Exception as e:
            logger.error(f"Failed to retrieve history: {e}", exc_info=True)
            return []
    
    def delete_screenshot(self, screenshot_id: int) -> bool:
        """
        Delete a screenshot from both disk and database.
        
        Args:
            screenshot_id: Database ID of screenshot to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get filepath
            cursor.execute("SELECT filepath FROM screenshots WHERE id = ?", (screenshot_id,))
            row = cursor.fetchone()
            
            if not row:
                logger.warning(f"Screenshot not found in database: {screenshot_id}")
                conn.close()
                return False
            
            filepath = Path(row[0])
            
            # Delete file from disk
            if filepath.exists():
                filepath.unlink()
                logger.debug(f"Deleted file: {filepath}")
            
            # Delete from database
            cursor.execute("DELETE FROM screenshots WHERE id = ?", (screenshot_id,))
            conn.commit()
            conn.close()
            
            logger.info(f"Screenshot deleted | ID: {screenshot_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete screenshot: {e}", exc_info=True)
            return False
    
    def cleanup_old_screenshots(self):
        """
        Delete old screenshots based on auto-delete settings.
        
        The passing of time - removing what has served its purpose.
        """
        if not self.config.get("auto_delete", "enabled"):
            logger.debug("Auto-delete disabled, skipping cleanup")
            return
        
        try:
            days_to_keep = self.config.get("auto_delete", "days_to_keep")
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find old screenshots
            cursor.execute("""
                SELECT id, filepath FROM screenshots 
                WHERE timestamp < ?
            """, (cutoff_date,))
            
            old_screenshots = cursor.fetchall()
            deleted_count = 0
            
            for screenshot_id, filepath in old_screenshots:
                # Delete file
                file_path = Path(filepath)
                if file_path.exists():
                    file_path.unlink()
                    deleted_count += 1
                
                # Delete from database
                cursor.execute("DELETE FROM screenshots WHERE id = ?", (screenshot_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cleanup completed | Deleted {deleted_count} old screenshot(s)")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old screenshots: {e}", exc_info=True)
