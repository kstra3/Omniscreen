"""
Clipboard Management Module

Handles copying screenshots to the system clipboard, enabling users to
paste captures directly into other applications. Like Hermes delivering
messages between the gods and mortals.
"""

import io
from PIL import Image
import pyperclip
from logger import get_logger

# Platform-specific clipboard handling
import platform
system = platform.system()

if system == "Windows":
    import win32clipboard
    from PIL import ImageGrab
elif system == "Darwin":  # macOS
    import subprocess
elif system == "Linux":
    import subprocess


logger = get_logger(__name__)


class ClipboardManager:
    """
    Manages clipboard operations for screenshots.
    
    The swift messenger - delivering captures to wherever they're needed.
    """
    
    def __init__(self):
        """Initialize clipboard manager."""
        self.system = system
        logger.debug(f"ClipboardManager initialized | Platform: {self.system}")
    
    def copy_image(self, image: Image.Image) -> bool:
        """
        Copy an image to the system clipboard.
        
        The sacred transfer - sending the image to the ethereal clipboard realm.
        
        Args:
            image: PIL Image to copy
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.system == "Windows":
                return self._copy_windows(image)
            elif self.system == "Darwin":
                return self._copy_macos(image)
            elif self.system == "Linux":
                return self._copy_linux(image)
            else:
                logger.warning(f"Clipboard copy not supported on {self.system}")
                return False
        except Exception as e:
            logger.error(f"Failed to copy image to clipboard: {e}", exc_info=True)
            return False
    
    def _copy_windows(self, image: Image.Image) -> bool:
        """Copy image to clipboard on Windows."""
        try:
            output = io.BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]  # Remove BMP header
            output.close()
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            
            logger.info("Image copied to clipboard (Windows)")
            return True
        except Exception as e:
            logger.error(f"Windows clipboard copy failed: {e}", exc_info=True)
            return False
    
    def _copy_macos(self, image: Image.Image) -> bool:
        """Copy image to clipboard on macOS."""
        try:
            # Save to temporary file and use osascript
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                image.save(tmp.name, 'PNG')
                tmp_path = tmp.name
            
            # Use osascript to copy to clipboard
            subprocess.run([
                'osascript', '-e',
                f'set the clipboard to (read (POSIX file "{tmp_path}") as «class PNGf»)'
            ], check=True)
            
            # Clean up temp file
            import os
            os.unlink(tmp_path)
            
            logger.info("Image copied to clipboard (macOS)")
            return True
        except Exception as e:
            logger.error(f"macOS clipboard copy failed: {e}", exc_info=True)
            return False
    
    def _copy_linux(self, image: Image.Image) -> bool:
        """Copy image to clipboard on Linux."""
        try:
            # Try xclip first (most common)
            try:
                output = io.BytesIO()
                image.save(output, 'PNG')
                output.seek(0)
                
                subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-t', 'image/png'],
                    input=output.read(),
                    check=True
                )
                output.close()
                
                logger.info("Image copied to clipboard (Linux - xclip)")
                return True
            except FileNotFoundError:
                # xclip not available, try xsel
                logger.debug("xclip not found, trying xsel")
                
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    image.save(tmp.name, 'PNG')
                    tmp_path = tmp.name
                
                subprocess.run([
                    'xsel', '--clipboard', '--input', tmp_path
                ], check=True)
                
                import os
                os.unlink(tmp_path)
                
                logger.info("Image copied to clipboard (Linux - xsel)")
                return True
        except Exception as e:
            logger.error(f"Linux clipboard copy failed: {e}", exc_info=True)
            logger.warning("Install xclip or xsel for clipboard support: sudo apt-get install xclip")
            return False
    
    def copy_text(self, text: str) -> bool:
        """
        Copy text to clipboard (for file paths, etc.)
        
        Args:
            text: Text to copy
        
        Returns:
            True if successful, False otherwise
        """
        try:
            pyperclip.copy(text)
            logger.debug(f"Text copied to clipboard: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to copy text to clipboard: {e}", exc_info=True)
            return False
