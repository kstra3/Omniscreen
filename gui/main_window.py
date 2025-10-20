"""
Main GUI Window

The central temple of OmniScreen - where users interact with the divine
power of screenshot capture.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSystemTrayIcon, QMenu, QStatusBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QAction, QPixmap
from pathlib import Path
from logger import get_logger
from config import get_config
from core import ScreenCapture, CaptureMode, StorageManager, ClipboardManager
from utils import NotificationManager
from .history import HistoryPanel
from .settings import SettingsDialog
from .region_selector import RegionSelector


logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """
    The main application window - The Parthenon of OmniScreen.
    
    Provides the primary interface for screenshot operations and settings.
    """
    
    # Signals
    capture_requested = pyqtSignal(CaptureMode)
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.config = get_config()
        self.capture_engine = ScreenCapture()
        self.storage_manager = StorageManager()
        self.clipboard_manager = ClipboardManager()
        self.notification_manager = NotificationManager()
        
        self.history_panel = None
        self.region_selector = None
        
        self._setup_ui()
        self._setup_tray_icon()
        self._connect_signals()
        
        logger.info("MainWindow initialized")
    
    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("OmniScreen - Screenshot Master")
        self.setMinimumSize(600, 400)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title with Greek styling
        title = QLabel("⚡ OMNISCREEN ⚡")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Καλώς ἦλθες - Welcome to Ancient Screenshot Mastery")
        subtitle.setProperty("subheading", True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Capture buttons
        capture_layout = QVBoxLayout()
        capture_layout.setSpacing(15)
        
        # Full screen button
        btn_fullscreen = QPushButton("📸 Capture Full Screen")
        btn_fullscreen.setProperty("primary", True)
        btn_fullscreen.clicked.connect(lambda: self.initiate_capture(CaptureMode.FULLSCREEN))
        btn_fullscreen.setToolTip("Capture the entire screen (Ctrl+Shift+S)")
        capture_layout.addWidget(btn_fullscreen)
        
        # Window button
        btn_window = QPushButton("🖼️ Capture Active Window")
        btn_window.clicked.connect(lambda: self.initiate_capture(CaptureMode.WINDOW))
        btn_window.setToolTip("Capture the currently active window (Ctrl+Shift+W)")
        capture_layout.addWidget(btn_window)
        
        # Region button
        btn_region = QPushButton("✂️ Capture Region")
        btn_region.clicked.connect(lambda: self.initiate_capture(CaptureMode.REGION))
        btn_region.setToolTip("Select a region to capture (Ctrl+Shift+R)")
        capture_layout.addWidget(btn_region)
        
        layout.addLayout(capture_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        
        btn_history = QPushButton("📜 History")
        btn_history.clicked.connect(self.show_history)
        action_layout.addWidget(btn_history)
        
        btn_settings = QPushButton("⚙️ Settings")
        btn_settings.clicked.connect(self.show_settings)
        action_layout.addWidget(btn_settings)
        
        layout.addLayout(action_layout)
        
        # Add stretch to push everything up
        layout.addStretch()
        
        # Status bar with Greek border
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to capture - Ἕτοιμος")
        
        # Menu bar
        self._setup_menu_bar()
    
    def _setup_menu_bar(self):
        """Set up the menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        action_capture = QAction("&Quick Capture", self)
        action_capture.setShortcut("Ctrl+Shift+S")
        action_capture.triggered.connect(lambda: self.initiate_capture(CaptureMode.FULLSCREEN))
        file_menu.addAction(action_capture)
        
        file_menu.addSeparator()
        
        action_exit = QAction("E&xit", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)
        
        # View menu
        view_menu = menu_bar.addMenu("&View")
        
        action_history = QAction("&History", self)
        action_history.setShortcut("Ctrl+H")
        action_history.triggered.connect(self.show_history)
        view_menu.addAction(action_history)
        
        # Tools menu
        tools_menu = menu_bar.addMenu("&Tools")
        
        action_settings = QAction("&Settings", self)
        action_settings.setShortcut("Ctrl+,")
        action_settings.triggered.connect(self.show_settings)
        tools_menu.addAction(action_settings)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        action_about = QAction("&About", self)
        action_about.triggered.connect(self.show_about)
        help_menu.addAction(action_about)
    
    def _setup_tray_icon(self):
        """Set up system tray icon."""
        try:
            self.tray_icon = QSystemTrayIcon(self)
            
            # Try to load icon (fallback to default if not found)
            icon_path = Path(__file__).parent.parent / "assets" / "icons" / "icon.png"
            if icon_path.exists():
                self.tray_icon.setIcon(QIcon(str(icon_path)))
            else:
                # Use a simple text-based icon
                from PyQt6.QtGui import QPixmap, QPainter, QFont
                pixmap = QPixmap(64, 64)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                painter.setFont(QFont("Arial", 32))
                painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "📸")
                painter.end()
                self.tray_icon.setIcon(QIcon(pixmap))
            
            # Tray menu
            tray_menu = QMenu()
            
            action_show = tray_menu.addAction("Show OmniScreen")
            action_show.triggered.connect(self.show)
            
            tray_menu.addSeparator()
            
            action_fullscreen = tray_menu.addAction("Capture Full Screen")
            action_fullscreen.triggered.connect(lambda: self.initiate_capture(CaptureMode.FULLSCREEN))
            
            action_window = tray_menu.addAction("Capture Window")
            action_window.triggered.connect(lambda: self.initiate_capture(CaptureMode.WINDOW))
            
            action_region = tray_menu.addAction("Capture Region")
            action_region.triggered.connect(lambda: self.initiate_capture(CaptureMode.REGION))
            
            tray_menu.addSeparator()
            
            action_quit = tray_menu.addAction("Quit")
            action_quit.triggered.connect(self.quit_application)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("OmniScreen - Screenshot Tool")
            
            # Tray icon activation
            self.tray_icon.activated.connect(self.on_tray_activated)
            
            self.tray_icon.show()
            
            # Store reference in QApplication for notifications
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                app.tray_icon = self.tray_icon
            
            logger.info("System tray icon initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup tray icon: {e}", exc_info=True)
    
    def _connect_signals(self):
        """Connect internal signals."""
        self.capture_requested.connect(self.perform_capture)
    
    def initiate_capture(self, mode: CaptureMode):
        """
        Initiate a screenshot capture.
        
        Args:
            mode: Capture mode to use
        """
        logger.info(f"Initiating capture | Mode: {mode.value}")
        
        if mode == CaptureMode.REGION:
            # Show region selector
            self.show_region_selector()
        else:
            # Minimize window for cleaner capture
            self.hide()
            # Small delay to ensure window is hidden
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(200, lambda: self.capture_requested.emit(mode))
    
    def perform_capture(self, mode: CaptureMode, **kwargs):
        """
        Perform the actual screenshot capture.
        
        Args:
            mode: Capture mode
            **kwargs: Additional arguments for specific modes
        """
        try:
            # Capture screenshot
            image, window_name = self.capture_engine.capture(mode, **kwargs)
            
            # Save screenshot
            should_save = not self.config.get("clipboard", "copy_on_capture") or \
                         self.config.get("clipboard", "save_and_copy")
            
            filepath = None
            if should_save:
                filepath = self.storage_manager.save_screenshot(
                    image, window_name, mode.value
                )
            
            # Copy to clipboard if enabled
            if self.config.get("clipboard", "copy_on_capture") or \
               self.config.get("clipboard", "save_and_copy"):
                self.clipboard_manager.copy_image(image)
            
            # Show notification
            if filepath:
                self.notification_manager.notify_capture_success(filepath)
                self.status_bar.showMessage(f"Screenshot saved: {Path(filepath).name}")
            else:
                self.notification_manager.show_notification(
                    "Screenshot Captured",
                    "Copied to clipboard"
                )
                self.status_bar.showMessage("Screenshot copied to clipboard")
            
            logger.info(f"Capture successful | Mode: {mode.value} | File: {filepath}")
            
        except Exception as e:
            error_msg = f"Capture failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.notification_manager.notify_capture_error(error_msg)
            self.status_bar.showMessage(error_msg)
        
        finally:
            # Restore window
            self.show()
    
    def show_region_selector(self):
        """Show the region selector overlay."""
        try:
            self.region_selector = RegionSelector()
            self.region_selector.region_selected.connect(self.on_region_selected)
            self.region_selector.show_fullscreen()
        except Exception as e:
            logger.error(f"Failed to show region selector: {e}", exc_info=True)
    
    def on_region_selected(self, x: int, y: int, width: int, height: int):
        """Handle region selection."""
        self.perform_capture(
            CaptureMode.REGION,
            x=x, y=y, width=width, height=height
        )
    
    def show_history(self):
        """Show the history panel."""
        if not self.history_panel:
            self.history_panel = HistoryPanel(self.storage_manager)
        self.history_panel.show()
        self.history_panel.raise_()
        self.history_panel.activateWindow()
    
    def show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About OmniScreen",
            "<h2>OmniScreen</h2>"
            "<p><b>Version:</b> 1.0.0</p>"
            "<p><b>Ancient Greek Screenshot Tool</b></p>"
            "<p>Capture your screen with the elegance of classical antiquity.</p>"
            "<p><i>Ἐν ἀρχῇ ἦν ὁ λόγος</i> - In the beginning was the word</p>"
            "<p>© 2024 OmniScreen Project</p>"
        )
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Left click - toggle window visibility
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()
    
    def quit_application(self):
        """Quit the application completely."""
        logger.info("Application quit requested")
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Minimize to tray instead of closing
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "OmniScreen",
            "Application minimized to tray",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
