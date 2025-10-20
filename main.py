"""
OmniScreen - Ancient Greek Screenshot Application

Main entry point for the OmniScreen application.
Where the journey begins - Ἀρχή (The Beginning).
"""

import sys
import argparse
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from logger import get_logger, log_startup, log_shutdown
from config import get_config
from gui import MainWindow, GreekTheme
from core import HotkeyManager
from cli import CLIHandler


logger = get_logger(__name__)


class OmniScreenApp:
    """
    Main application controller.
    
    The Archon - the ruler that orchestrates all components of OmniScreen.
    """
    
    def __init__(self, cli_mode: bool = False):
        """
        Initialize the application.
        
        Args:
            cli_mode: Run in CLI mode if True, GUI mode if False
        """
        self.cli_mode = cli_mode
        self.config = get_config()
        self.app = None
        self.main_window = None
        self.hotkey_manager = None
        
        log_startup()
        logger.info(f"OmniScreen initializing | Mode: {'CLI' if cli_mode else 'GUI'}")
    
    def run_gui(self):
        """Run the application in GUI mode."""
        try:
            # Create QApplication
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("OmniScreen")
            self.app.setOrganizationName("OmniScreen")
            
            # Apply Greek theme
            GreekTheme.apply_theme(self.app)
            
            # Create main window
            self.main_window = MainWindow()
            self.main_window.show()
            
            # Setup global hotkeys if background service enabled
            if self.config.get("background_service", "enabled"):
                self._setup_hotkeys()
            
            logger.info("GUI mode started successfully")
            
            # Run application
            exit_code = self.app.exec()
            
            # Cleanup
            self._cleanup()
            
            return exit_code
            
        except Exception as e:
            logger.error(f"GUI mode failed: {e}", exc_info=True)
            return 1
    
    def run_cli(self, args=None):
        """
        Run the application in CLI mode.
        
        Args:
            args: Command-line arguments
        
        Returns:
            Exit code
        """
        try:
            cli_handler = CLIHandler()
            return cli_handler.handle(args)
        except Exception as e:
            logger.error(f"CLI mode failed: {e}", exc_info=True)
            return 1
    
    def _setup_hotkeys(self):
        """Setup global hotkeys."""
        try:
            self.hotkey_manager = HotkeyManager()
            
            # Register hotkeys
            quick_hotkey = self.config.get("hotkeys", "quick_capture")
            window_hotkey = self.config.get("hotkeys", "window_capture")
            region_hotkey = self.config.get("hotkeys", "region_capture")
            
            from core import CaptureMode
            
            self.hotkey_manager.register_hotkey(
                quick_hotkey,
                lambda: self.main_window.initiate_capture(CaptureMode.FULLSCREEN)
            )
            
            self.hotkey_manager.register_hotkey(
                window_hotkey,
                lambda: self.main_window.initiate_capture(CaptureMode.WINDOW)
            )
            
            self.hotkey_manager.register_hotkey(
                region_hotkey,
                lambda: self.main_window.initiate_capture(CaptureMode.REGION)
            )
            
            self.hotkey_manager.start()
            
            logger.info("Global hotkeys registered and active")
            
        except Exception as e:
            logger.error(f"Failed to setup hotkeys: {e}", exc_info=True)
    
    def _cleanup(self):
        """Cleanup resources."""
        try:
            if self.hotkey_manager:
                self.hotkey_manager.stop()
            
            log_shutdown()
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}", exc_info=True)


def main():
    """
    Main entry point for OmniScreen.
    
    Ἀρχὴ ἥμισυ παντός - The beginning is half of everything.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='OmniScreen - Ancient Greek Screenshot Tool',
        add_help=True
    )
    
    parser.add_argument(
        '--cli', action='store_true',
        help='Run in CLI mode'
    )
    
    # If there are subcommands, assume CLI mode
    if len(sys.argv) > 1 and sys.argv[1] in ['capture', 'history', 'config']:
        app = OmniScreenApp(cli_mode=True)
        sys.exit(app.run_cli())
    else:
        # Check for --cli flag
        args, remaining = parser.parse_known_args()
        
        if args.cli:
            app = OmniScreenApp(cli_mode=True)
            sys.exit(app.run_cli(remaining))
        else:
            # Run in GUI mode
            app = OmniScreenApp(cli_mode=False)
            sys.exit(app.run_gui())


if __name__ == '__main__':
    main()
