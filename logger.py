"""
Logging Module

Provides comprehensive logging capabilities, inspired by the meticulous
historians of ancient Greece who recorded every significant event.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from config import get_config


class GreekFormatter(logging.Formatter):
    """
    Custom formatter with Greek-inspired styling.
    Adds aesthetic touches to log messages, honoring the art of documentation.
    """
    
    # Color codes for terminal output
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan - the color of wisdom
        'INFO': '\033[37m',     # White - the color of marble
        'WARNING': '\033[33m',  # Yellow - the color of gold
        'ERROR': '\033[31m',    # Red - the color of sacrifice
        'CRITICAL': '\033[35m', # Magenta - the color of royalty
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        """Format log record with colors and Greek touches."""
        # Add color for console output
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logger(name: str = "OmniScreen") -> logging.Logger:
    """
    Set up application logger with file and console handlers.
    
    The logger follows the principle of 'Ἱστορία' (Historia) - thorough
    investigation and recording of events.
    
    Args:
        name: Logger name (default: OmniScreen)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Get log file path from config
    config = get_config()
    log_dir = config.get_logs_path()
    log_file = log_dir / f"omniscreen_{datetime.now().strftime('%Y%m%d')}.log"
    
    # File handler - rotating log files (10MB max, keep 5 backups)
    # Like scrolls in the Library of Alexandria, but with automatic archiving
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler - for immediate feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = GreekFormatter(
        '⚡ %(levelname)-8s | %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log the initialization - marking the beginning of our chronicle
    logger.info("=" * 70)
    logger.info("OmniScreen Logger Initialized - Ἀρχὴ τῆς ἱστορίας (Beginning of History)")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 70)
    
    return logger


def get_logger(name: str = "OmniScreen") -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# Module-level convenience functions
def log_capture(mode: str, success: bool, file_path: str = None):
    """Log screenshot capture event."""
    logger = get_logger()
    if success:
        logger.info(f"Screenshot captured successfully | Mode: {mode} | Saved: {file_path}")
    else:
        logger.error(f"Screenshot capture failed | Mode: {mode}")


def log_error(operation: str, error: Exception):
    """Log an error with context."""
    logger = get_logger()
    logger.error(f"Error during {operation}: {str(error)}", exc_info=True)


def log_config_change(setting: str, old_value: any, new_value: any):
    """Log configuration change."""
    logger = get_logger()
    logger.info(f"Config changed | {setting}: {old_value} → {new_value}")


def log_startup():
    """Log application startup."""
    logger = get_logger()
    logger.info("🏛️ OmniScreen Application Starting - Καλώς ἦλθες (Welcome)")


def log_shutdown():
    """Log application shutdown."""
    logger = get_logger()
    logger.info("🏛️ OmniScreen Application Shutting Down - Χαίρε (Farewell)")
    logger.info("=" * 70)
