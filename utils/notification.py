"""
Notification System

Provides visual and audio feedback for screenshot captures, following the
tradition of Greek heralds announcing important events.
"""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import platform
from pathlib import Path
from config import get_config
from logger import get_logger


logger = get_logger(__name__)


class NotificationManager:
    """
    Manages system notifications and audio feedback.
    
    The herald's trumpet - announcing each successful capture to the user.
    """
    
    def __init__(self):
        """Initialize notification manager."""
        self.config = get_config()
        self.system = platform.system()
        logger.debug(f"NotificationManager initialized | Platform: {self.system}")
    
    def show_notification(self, title: str, message: str, icon_path: str = None):
        """
        Display a system notification.
        
        Args:
            title: Notification title
            message: Notification message
            icon_path: Optional path to icon file
        """
        if not self.config.get("notifications", "enabled"):
            logger.debug("Notifications disabled, skipping")
            return
        
        try:
            # Try to use system tray icon for notification if available
            from PyQt6.QtWidgets import QSystemTrayIcon
            
            # Get QApplication instance
            app = QApplication.instance()
            if app and hasattr(app, 'tray_icon'):
                tray_icon = app.tray_icon
                if isinstance(tray_icon, QSystemTrayIcon):
                    tray_icon.showMessage(
                        title,
                        message,
                        QSystemTrayIcon.MessageIcon.Information,
                        3000  # 3 seconds
                    )
                    logger.debug(f"Notification shown: {title}")
                    return
            
            # Fallback to platform-specific notifications
            self._show_platform_notification(title, message)
            
        except Exception as e:
            logger.error(f"Failed to show notification: {e}", exc_info=True)
    
    def _show_platform_notification(self, title: str, message: str):
        """Show notification using platform-specific methods."""
        if self.system == "Windows":
            self._show_windows_notification(title, message)
        elif self.system == "Darwin":
            self._show_macos_notification(title, message)
        elif self.system == "Linux":
            self._show_linux_notification(title, message)
    
    def _show_windows_notification(self, title: str, message: str):
        """Show notification on Windows using win10toast or plyer."""
        try:
            # Try using Windows toast notification
            import subprocess
            ps_script = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
            
            $template = @"
            <toast>
                <visual>
                    <binding template="ToastText02">
                        <text id="1">{title}</text>
                        <text id="2">{message}</text>
                    </binding>
                </visual>
            </toast>
"@
            
            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("OmniScreen").Show($toast)
            """
            
            subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                timeout=2
            )
            logger.debug("Windows notification shown")
        except Exception as e:
            logger.debug(f"Windows notification failed: {e}")
    
    def _show_macos_notification(self, title: str, message: str):
        """Show notification on macOS using osascript."""
        try:
            import subprocess
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], timeout=2)
            logger.debug("macOS notification shown")
        except Exception as e:
            logger.debug(f"macOS notification failed: {e}")
    
    def _show_linux_notification(self, title: str, message: str):
        """Show notification on Linux using notify-send."""
        try:
            import subprocess
            subprocess.run(['notify-send', title, message], timeout=2)
            logger.debug("Linux notification shown")
        except FileNotFoundError:
            logger.debug("notify-send not available")
        except Exception as e:
            logger.debug(f"Linux notification failed: {e}")
    
    def play_sound(self):
        """
        Play notification sound.
        
        The chime of success - a pleasant tone to mark the capture.
        """
        if not self.config.get("notifications", "sound"):
            return
        
        try:
            # Simple beep for now - can be extended with custom sounds
            if self.system == "Windows":
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
            elif self.system == "Darwin":
                import subprocess
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], timeout=1)
            elif self.system == "Linux":
                import subprocess
                subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/camera-shutter.oga'], 
                             timeout=1)
            
            logger.debug("Notification sound played")
        except Exception as e:
            logger.debug(f"Failed to play sound: {e}")
    
    def notify_capture_success(self, filepath: str):
        """
        Show notification for successful screenshot capture.
        
        Args:
            filepath: Path where screenshot was saved
        """
        filename = Path(filepath).name
        self.show_notification(
            "Screenshot Captured",
            f"Saved as {filename}"
        )
        self.play_sound()
    
    def notify_capture_error(self, error_msg: str):
        """
        Show notification for capture error.
        
        Args:
            error_msg: Error message to display
        """
        self.show_notification(
            "Screenshot Failed",
            error_msg
        )
