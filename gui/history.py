"""
History Panel

Displays screenshot history with search and management capabilities.
Like browsing the archives of the Great Library.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from pathlib import Path
from logger import get_logger


logger = get_logger(__name__)


class HistoryPanel(QWidget):
    """
    Screenshot history browser and manager.
    
    The Chronicle - where past captures are preserved and accessible.
    """
    
    def __init__(self, storage_manager):
        """
        Initialize history panel.
        
        Args:
            storage_manager: StorageManager instance
        """
        super().__init__()
        
        self.storage_manager = storage_manager
        self.current_search = ""
        
        self._setup_ui()
        self.load_history()
        
        logger.info("HistoryPanel initialized")
    
    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("OmniScreen - Screenshot History")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📜 Screenshot History")
        title.setProperty("heading", True)
        layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search screenshots...")
        self.search_input.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        
        btn_search = QPushButton("🔍 Search")
        btn_search.clicked.connect(self.perform_search)
        search_layout.addWidget(btn_search)
        
        layout.addLayout(search_layout)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.open_screenshot)
        layout.addWidget(self.history_list)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        btn_open = QPushButton("Open")
        btn_open.clicked.connect(self.open_selected)
        action_layout.addWidget(btn_open)
        
        btn_copy_path = QPushButton("Copy Path")
        btn_copy_path.clicked.connect(self.copy_path)
        action_layout.addWidget(btn_copy_path)
        
        btn_delete = QPushButton("Delete")
        btn_delete.clicked.connect(self.delete_selected)
        action_layout.addWidget(btn_delete)
        
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.load_history)
        action_layout.addWidget(btn_refresh)
        
        layout.addLayout(action_layout)
    
    def load_history(self, search_term: str = None):
        """
        Load screenshot history from database.
        
        Args:
            search_term: Optional search term to filter results
        """
        try:
            self.history_list.clear()
            
            # Get history from storage manager
            history = self.storage_manager.get_history(limit=100, search_term=search_term)
            
            for record in history:
                item = QListWidgetItem()
                
                # Format display text
                filename = record.get('filename', 'Unknown')
                timestamp = record.get('timestamp', 'N/A')
                window_name = record.get('window_name', 'N/A')
                
                text = f"{filename}\n{timestamp}"
                if window_name and window_name != 'None':
                    text += f"\nWindow: {window_name}"
                
                item.setText(text)
                item.setData(Qt.ItemDataRole.UserRole, record)
                
                self.history_list.addItem(item)
            
            logger.debug(f"Loaded {len(history)} history records")
            
        except Exception as e:
            logger.error(f"Failed to load history: {e}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Failed to load history: {e}")
    
    def on_search(self, text: str):
        """Handle search input change."""
        self.current_search = text
    
    def perform_search(self):
        """Perform search."""
        self.load_history(self.current_search if self.current_search else None)
    
    def open_screenshot(self, item: QListWidgetItem):
        """Open screenshot file."""
        try:
            record = item.data(Qt.ItemDataRole.UserRole)
            filepath = Path(record['filepath'])
            
            if filepath.exists():
                import os
                import platform
                
                system = platform.system()
                if system == "Windows":
                    os.startfile(filepath)
                elif system == "Darwin":
                    import subprocess
                    subprocess.run(['open', str(filepath)])
                else:
                    import subprocess
                    subprocess.run(['xdg-open', str(filepath)])
                
                logger.info(f"Opened screenshot: {filepath}")
            else:
                QMessageBox.warning(self, "File Not Found", 
                                  f"Screenshot file not found:\n{filepath}")
        except Exception as e:
            logger.error(f"Failed to open screenshot: {e}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Failed to open screenshot: {e}")
    
    def open_selected(self):
        """Open selected screenshot."""
        item = self.history_list.currentItem()
        if item:
            self.open_screenshot(item)
    
    def copy_path(self):
        """Copy selected screenshot path to clipboard."""
        item = self.history_list.currentItem()
        if item:
            try:
                record = item.data(Qt.ItemDataRole.UserRole)
                filepath = record['filepath']
                
                from core import ClipboardManager
                clipboard = ClipboardManager()
                clipboard.copy_text(filepath)
                
                logger.info(f"Copied path to clipboard: {filepath}")
            except Exception as e:
                logger.error(f"Failed to copy path: {e}", exc_info=True)
    
    def delete_selected(self):
        """Delete selected screenshot."""
        item = self.history_list.currentItem()
        if not item:
            return
        
        try:
            record = item.data(Qt.ItemDataRole.UserRole)
            filename = record['filename']
            
            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Delete screenshot:\n{filename}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                screenshot_id = record['id']
                if self.storage_manager.delete_screenshot(screenshot_id):
                    self.history_list.takeItem(self.history_list.row(item))
                    logger.info(f"Deleted screenshot: {filename}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete screenshot")
        
        except Exception as e:
            logger.error(f"Failed to delete screenshot: {e}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Failed to delete: {e}")
