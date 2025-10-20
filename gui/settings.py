"""
Settings Dialog

Configuration interface for OmniScreen settings.
The Oracle's chamber where destiny is configured.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QSpinBox, QGroupBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from pathlib import Path
from config import get_config
from logger import get_logger


logger = get_logger(__name__)


class SettingsDialog(QDialog):
    """
    Settings configuration dialog.
    
    The Council Chamber - where the rules of OmniScreen are set.
    """
    
    def __init__(self, parent=None):
        """Initialize settings dialog."""
        super().__init__(parent)
        
        self.config = get_config()
        
        self._setup_ui()
        self._load_settings()
        
        logger.info("SettingsDialog opened")
    
    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("OmniScreen Settings")
        self.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("⚙️ Settings")
        title.setProperty("heading", True)
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        
        # General tab
        tabs.addTab(self._create_general_tab(), "General")
        
        # Hotkeys tab
        tabs.addTab(self._create_hotkeys_tab(), "Hotkeys")
        
        # Storage tab
        tabs.addTab(self._create_storage_tab(), "Storage")
        
        # Notifications tab
        tabs.addTab(self._create_notifications_tab(), "Notifications")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        btn_save = QPushButton("Save")
        btn_save.setProperty("primary", True)
        btn_save.clicked.connect(self.save_settings)
        button_layout.addWidget(btn_save)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self) -> QWidget:
        """Create general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Clipboard group
        clipboard_group = QGroupBox("Clipboard")
        clipboard_layout = QVBoxLayout()
        
        self.cb_copy_on_capture = QCheckBox("Copy to clipboard on capture")
        clipboard_layout.addWidget(self.cb_copy_on_capture)
        
        self.cb_save_and_copy = QCheckBox("Save file and copy to clipboard")
        clipboard_layout.addWidget(self.cb_save_and_copy)
        
        clipboard_group.setLayout(clipboard_layout)
        layout.addWidget(clipboard_group)
        
        # UI group
        ui_group = QGroupBox("User Interface")
        ui_layout = QVBoxLayout()
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(8, 20)
        self.spin_font_size.setSuffix(" pt")
        font_layout.addWidget(self.spin_font_size)
        font_layout.addStretch()
        ui_layout.addLayout(font_layout)
        
        self.cb_high_contrast = QCheckBox("High contrast mode")
        ui_layout.addWidget(self.cb_high_contrast)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        layout.addStretch()
        return widget
    
    def _create_hotkeys_tab(self) -> QWidget:
        """Create hotkeys settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        hotkey_group = QGroupBox("Global Hotkeys")
        hotkey_layout = QVBoxLayout()
        
        # Quick capture
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("Quick Capture:"))
        self.edit_hotkey_quick = QLineEdit()
        self.edit_hotkey_quick.setPlaceholderText("e.g., ctrl+shift+s")
        quick_layout.addWidget(self.edit_hotkey_quick)
        hotkey_layout.addLayout(quick_layout)
        
        # Window capture
        window_layout = QHBoxLayout()
        window_layout.addWidget(QLabel("Window Capture:"))
        self.edit_hotkey_window = QLineEdit()
        self.edit_hotkey_window.setPlaceholderText("e.g., ctrl+shift+w")
        window_layout.addWidget(self.edit_hotkey_window)
        hotkey_layout.addLayout(window_layout)
        
        # Region capture
        region_layout = QHBoxLayout()
        region_layout.addWidget(QLabel("Region Capture:"))
        self.edit_hotkey_region = QLineEdit()
        self.edit_hotkey_region.setPlaceholderText("e.g., ctrl+shift+r")
        region_layout.addWidget(self.edit_hotkey_region)
        hotkey_layout.addLayout(region_layout)
        
        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)
        
        # Background service
        service_group = QGroupBox("Background Service")
        service_layout = QVBoxLayout()
        
        self.cb_background_service = QCheckBox("Enable background service")
        service_layout.addWidget(self.cb_background_service)
        
        self.cb_start_on_boot = QCheckBox("Start on system boot")
        service_layout.addWidget(self.cb_start_on_boot)
        
        service_group.setLayout(service_layout)
        layout.addWidget(service_group)
        
        layout.addStretch()
        return widget
    
    def _create_storage_tab(self) -> QWidget:
        """Create storage settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Save location
        location_group = QGroupBox("Save Location")
        location_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        self.edit_save_location = QLineEdit()
        path_layout.addWidget(self.edit_save_location)
        
        btn_browse = QPushButton("Browse...")
        btn_browse.clicked.connect(self.browse_save_location)
        path_layout.addWidget(btn_browse)
        
        location_layout.addLayout(path_layout)
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        # File naming
        naming_group = QGroupBox("File Naming")
        naming_layout = QVBoxLayout()
        
        naming_layout.addWidget(QLabel("Naming Pattern:"))
        self.edit_naming_pattern = QLineEdit()
        self.edit_naming_pattern.setPlaceholderText("%Y%m%d_%H%M%S_{window}")
        naming_layout.addWidget(self.edit_naming_pattern)
        
        help_label = QLabel("Available placeholders: %Y (year), %m (month), %d (day), "
                          "%H (hour), %M (minute), %S (second), {window} (window name)")
        help_label.setWordWrap(True)
        help_label.setStyleSheet("font-size: 10pt; font-style: italic;")
        naming_layout.addWidget(help_label)
        
        naming_group.setLayout(naming_layout)
        layout.addWidget(naming_group)
        
        # Organization
        org_group = QGroupBox("Organization")
        org_layout = QVBoxLayout()
        
        org_layout.addWidget(QLabel("Organize By:"))
        self.combo_organize = QComboBox()
        self.combo_organize.addItems(["Date", "Application", "None"])
        org_layout.addWidget(self.combo_organize)
        
        org_layout.addWidget(QLabel("Format:"))
        self.combo_format = QComboBox()
        self.combo_format.addItems(["png", "jpg", "bmp"])
        org_layout.addWidget(self.combo_format)
        
        org_group.setLayout(org_layout)
        layout.addWidget(org_group)
        
        # Auto-delete
        autodel_group = QGroupBox("Auto-Delete")
        autodel_layout = QVBoxLayout()
        
        self.cb_auto_delete = QCheckBox("Enable auto-delete old screenshots")
        autodel_layout.addWidget(self.cb_auto_delete)
        
        days_layout = QHBoxLayout()
        days_layout.addWidget(QLabel("Keep for:"))
        self.spin_days_to_keep = QSpinBox()
        self.spin_days_to_keep.setRange(1, 365)
        self.spin_days_to_keep.setSuffix(" days")
        days_layout.addWidget(self.spin_days_to_keep)
        days_layout.addStretch()
        autodel_layout.addLayout(days_layout)
        
        autodel_group.setLayout(autodel_layout)
        layout.addWidget(autodel_group)
        
        layout.addStretch()
        return widget
    
    def _create_notifications_tab(self) -> QWidget:
        """Create notifications settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        notif_group = QGroupBox("Notifications")
        notif_layout = QVBoxLayout()
        
        self.cb_notifications = QCheckBox("Enable notifications")
        notif_layout.addWidget(self.cb_notifications)
        
        self.cb_sound = QCheckBox("Play sound on capture")
        notif_layout.addWidget(self.cb_sound)
        
        notif_group.setLayout(notif_layout)
        layout.addWidget(notif_group)
        
        layout.addStretch()
        return widget
    
    def _load_settings(self):
        """Load current settings into UI."""
        # General
        self.cb_copy_on_capture.setChecked(
            self.config.get("clipboard", "copy_on_capture")
        )
        self.cb_save_and_copy.setChecked(
            self.config.get("clipboard", "save_and_copy")
        )
        self.spin_font_size.setValue(
            self.config.get("ui", "font_size")
        )
        self.cb_high_contrast.setChecked(
            self.config.get("ui", "high_contrast")
        )
        
        # Hotkeys
        self.edit_hotkey_quick.setText(
            self.config.get("hotkeys", "quick_capture")
        )
        self.edit_hotkey_window.setText(
            self.config.get("hotkeys", "window_capture")
        )
        self.edit_hotkey_region.setText(
            self.config.get("hotkeys", "region_capture")
        )
        self.cb_background_service.setChecked(
            self.config.get("background_service", "enabled")
        )
        self.cb_start_on_boot.setChecked(
            self.config.get("background_service", "start_on_boot")
        )
        
        # Storage
        self.edit_save_location.setText(
            self.config.get("storage", "save_location")
        )
        self.edit_naming_pattern.setText(
            self.config.get("storage", "naming_pattern")
        )
        
        organize_by = self.config.get("storage", "organize_by")
        index = {"date": 0, "application": 1, "none": 2}.get(organize_by, 0)
        self.combo_organize.setCurrentIndex(index)
        
        format_type = self.config.get("storage", "format")
        self.combo_format.setCurrentText(format_type)
        
        self.cb_auto_delete.setChecked(
            self.config.get("auto_delete", "enabled")
        )
        self.spin_days_to_keep.setValue(
            self.config.get("auto_delete", "days_to_keep")
        )
        
        # Notifications
        self.cb_notifications.setChecked(
            self.config.get("notifications", "enabled")
        )
        self.cb_sound.setChecked(
            self.config.get("notifications", "sound")
        )
    
    def browse_save_location(self):
        """Browse for save location."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Save Location",
            self.edit_save_location.text()
        )
        
        if directory:
            self.edit_save_location.setText(directory)
    
    def save_settings(self):
        """Save settings and close dialog."""
        try:
            # General
            self.config.set("clipboard", "copy_on_capture", 
                          value=self.cb_copy_on_capture.isChecked())
            self.config.set("clipboard", "save_and_copy",
                          value=self.cb_save_and_copy.isChecked())
            self.config.set("ui", "font_size",
                          value=self.spin_font_size.value())
            self.config.set("ui", "high_contrast",
                          value=self.cb_high_contrast.isChecked())
            
            # Hotkeys
            self.config.set("hotkeys", "quick_capture",
                          value=self.edit_hotkey_quick.text())
            self.config.set("hotkeys", "window_capture",
                          value=self.edit_hotkey_window.text())
            self.config.set("hotkeys", "region_capture",
                          value=self.edit_hotkey_region.text())
            self.config.set("background_service", "enabled",
                          value=self.cb_background_service.isChecked())
            self.config.set("background_service", "start_on_boot",
                          value=self.cb_start_on_boot.isChecked())
            
            # Storage
            self.config.set("storage", "save_location",
                          value=self.edit_save_location.text())
            self.config.set("storage", "naming_pattern",
                          value=self.edit_naming_pattern.text())
            
            organize_map = {0: "date", 1: "application", 2: "none"}
            self.config.set("storage", "organize_by",
                          value=organize_map[self.combo_organize.currentIndex()])
            self.config.set("storage", "format",
                          value=self.combo_format.currentText())
            
            self.config.set("auto_delete", "enabled",
                          value=self.cb_auto_delete.isChecked())
            self.config.set("auto_delete", "days_to_keep",
                          value=self.spin_days_to_keep.value())
            
            # Notifications
            self.config.set("notifications", "enabled",
                          value=self.cb_notifications.isChecked())
            self.config.set("notifications", "sound",
                          value=self.cb_sound.isChecked())
            
            logger.info("Settings saved")
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Failed to save settings: {e}")
