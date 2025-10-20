"""
CLI Command Handler

Implements command-line interface for OmniScreen.
The ancient art of text-based command.
"""

import argparse
import sys
from pathlib import Path
from logger import get_logger, log_startup
from config import get_config
from core import ScreenCapture, CaptureMode, StorageManager, ClipboardManager


logger = get_logger(__name__)


class CLIHandler:
    """
    Handles command-line interface operations.
    
    The Hermit's path - achieving mastery through text commands alone.
    """
    
    def __init__(self):
        """Initialize CLI handler."""
        self.config = get_config()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create argument parser.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            prog='omniscreen',
            description='OmniScreen - Ancient Greek Screenshot Tool',
            epilog='Ἐν ἀρχῇ ἦν ὁ λόγος - In the beginning was the word'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Capture command
        capture_parser = subparsers.add_parser('capture', help='Capture screenshot')
        capture_parser.add_argument(
            '--fullscreen', action='store_true',
            help='Capture full screen'
        )
        capture_parser.add_argument(
            '--window', action='store_true',
            help='Capture active window'
        )
        capture_parser.add_argument(
            '--region', action='store_true',
            help='Capture custom region (interactive)'
        )
        capture_parser.add_argument(
            '--clipboard', action='store_true',
            help='Copy to clipboard instead of saving'
        )
        capture_parser.add_argument(
            '--output', '-o', type=str,
            help='Output file path'
        )
        
        # History command
        history_parser = subparsers.add_parser('history', help='View screenshot history')
        history_parser.add_argument(
            '--limit', '-n', type=int, default=10,
            help='Number of records to show'
        )
        history_parser.add_argument(
            '--search', '-s', type=str,
            help='Search term'
        )
        
        # Config command
        config_parser = subparsers.add_parser('config', help='Configure settings')
        config_parser.add_argument(
            '--hotkey', type=str,
            help='Set global hotkey'
        )
        config_parser.add_argument(
            '--save-location', type=str,
            help='Set save location'
        )
        config_parser.add_argument(
            '--show', action='store_true',
            help='Show current configuration'
        )
        
        return parser
    
    def handle(self, args=None):
        """
        Handle CLI command.
        
        Args:
            args: Command-line arguments (None = sys.argv)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 0
            
            if parsed_args.command == 'capture':
                return self.handle_capture(parsed_args)
            elif parsed_args.command == 'history':
                return self.handle_history(parsed_args)
            elif parsed_args.command == 'config':
                return self.handle_config(parsed_args)
            else:
                print(f"Unknown command: {parsed_args.command}")
                return 1
        
        except KeyboardInterrupt:
            print("\nOperation cancelled")
            return 130
        except Exception as e:
            logger.error(f"CLI error: {e}", exc_info=True)
            print(f"Error: {e}")
            return 1
    
    def handle_capture(self, args) -> int:
        """
        Handle capture command.
        
        Args:
            args: Parsed arguments
        
        Returns:
            Exit code
        """
        try:
            # Determine capture mode
            if args.fullscreen:
                mode = CaptureMode.FULLSCREEN
            elif args.window:
                mode = CaptureMode.WINDOW
            elif args.region:
                print("Region capture not supported in CLI mode")
                print("Please use GUI mode for region selection")
                return 1
            else:
                # Default to fullscreen
                mode = CaptureMode.FULLSCREEN
            
            print(f"Capturing {mode.value}...")
            
            # Capture screenshot
            capture_engine = ScreenCapture()
            image, window_name = capture_engine.capture(mode)
            
            # Handle output
            if args.clipboard:
                clipboard = ClipboardManager()
                clipboard.copy_image(image)
                print("Screenshot copied to clipboard")
            else:
                # Save to file
                storage = StorageManager()
                
                if args.output:
                    # Save to specified path
                    filepath = Path(args.output)
                    image.save(filepath)
                    print(f"Screenshot saved: {filepath}")
                else:
                    # Save using storage manager
                    filepath = storage.save_screenshot(image, window_name, mode.value)
                    print(f"Screenshot saved: {filepath}")
            
            return 0
            
        except Exception as e:
            logger.error(f"Capture failed: {e}", exc_info=True)
            print(f"Capture failed: {e}")
            return 1
    
    def handle_history(self, args) -> int:
        """
        Handle history command.
        
        Args:
            args: Parsed arguments
        
        Returns:
            Exit code
        """
        try:
            storage = StorageManager()
            history = storage.get_history(
                limit=args.limit,
                search_term=args.search if hasattr(args, 'search') else None
            )
            
            if not history:
                print("No screenshots found")
                return 0
            
            print(f"\n{'=' * 80}")
            print(f"Screenshot History ({len(history)} items)")
            print(f"{'=' * 80}\n")
            
            for record in history:
                filename = record.get('filename', 'Unknown')
                timestamp = record.get('timestamp', 'N/A')
                window_name = record.get('window_name', 'N/A')
                filepath = record.get('filepath', 'N/A')
                
                print(f"📸 {filename}")
                print(f"   Time: {timestamp}")
                if window_name and window_name != 'None':
                    print(f"   Window: {window_name}")
                print(f"   Path: {filepath}")
                print()
            
            return 0
            
        except Exception as e:
            logger.error(f"History retrieval failed: {e}", exc_info=True)
            print(f"Failed to retrieve history: {e}")
            return 1
    
    def handle_config(self, args) -> int:
        """
        Handle config command.
        
        Args:
            args: Parsed arguments
        
        Returns:
            Exit code
        """
        try:
            if args.show:
                # Show current configuration
                print(f"\n{'=' * 80}")
                print("OmniScreen Configuration")
                print(f"{'=' * 80}\n")
                
                print(f"Save Location: {self.config.get('storage', 'save_location')}")
                print(f"Format: {self.config.get('storage', 'format')}")
                print(f"Naming Pattern: {self.config.get('storage', 'naming_pattern')}")
                print(f"\nHotkeys:")
                print(f"  Quick Capture: {self.config.get('hotkeys', 'quick_capture')}")
                print(f"  Window Capture: {self.config.get('hotkeys', 'window_capture')}")
                print(f"  Region Capture: {self.config.get('hotkeys', 'region_capture')}")
                print()
                
                return 0
            
            # Update configuration
            if args.hotkey:
                self.config.set('hotkeys', 'quick_capture', value=args.hotkey)
                print(f"Hotkey updated: {args.hotkey}")
            
            if args.save_location:
                save_path = Path(args.save_location)
                save_path.mkdir(parents=True, exist_ok=True)
                self.config.set('storage', 'save_location', value=str(save_path))
                print(f"Save location updated: {save_path}")
            
            return 0
            
        except Exception as e:
            logger.error(f"Config operation failed: {e}", exc_info=True)
            print(f"Configuration failed: {e}")
            return 1


def main():
    """CLI entry point."""
    log_startup()
    handler = CLIHandler()
    sys.exit(handler.handle())


if __name__ == '__main__':
    main()
