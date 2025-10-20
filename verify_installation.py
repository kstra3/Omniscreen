"""
Installation Verification Script

Run this script to verify that OmniScreen is properly installed and configured.
"""

import sys
import importlib
import platform


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is too old. Python 3.8+ required.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_module(module_name, display_name=None):
    """Check if a module can be imported."""
    if display_name is None:
        display_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✅ {display_name}")
        return True
    except ImportError:
        print(f"❌ {display_name} - Not installed")
        return False


def check_platform_specific():
    """Check platform-specific dependencies."""
    system = platform.system()
    
    if system == "Windows":
        print("\n📋 Windows-specific dependencies:")
        check_module("win32gui", "pywin32")
        check_module("win32clipboard", "pywin32 (clipboard)")
    elif system == "Darwin":
        print("\n📋 macOS-specific dependencies:")
        check_module("Quartz", "pyobjc-framework-Quartz")
        check_module("AppKit", "pyobjc-framework-Cocoa")
    elif system == "Linux":
        print("\n📋 Linux-specific dependencies:")
        check_module("Xlib", "python-xlib")


def check_directories():
    """Check if necessary directories exist."""
    from pathlib import Path
    from config import get_config
    
    print("\n📁 Checking directories:")
    
    config = get_config()
    
    # Config directory
    config_dir = config.config_dir
    if config_dir.exists():
        print(f"✅ Config directory: {config_dir}")
    else:
        print(f"⚠️  Config directory will be created: {config_dir}")
    
    # Data directory
    data_dir = config.data_dir
    if data_dir.exists():
        print(f"✅ Data directory: {data_dir}")
    else:
        print(f"⚠️  Data directory will be created: {data_dir}")
    
    # Screenshot directory
    screenshot_dir = config.get_screenshot_path()
    if screenshot_dir.exists():
        print(f"✅ Screenshot directory: {screenshot_dir}")
    else:
        print(f"⚠️  Screenshot directory will be created: {screenshot_dir}")


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("OmniScreen Installation Verification")
    print("=" * 70)
    
    print(f"\n🖥️  Platform: {platform.system()} {platform.release()}")
    
    # Check Python version
    print("\n🐍 Python Version:")
    if not check_python_version():
        print("\n❌ Installation verification failed!")
        return 1
    
    # Check core dependencies
    print("\n📦 Core Dependencies:")
    all_ok = True
    
    modules_to_check = [
        ("PyQt6.QtCore", "PyQt6"),
        ("PIL", "Pillow"),
        ("mss", "mss"),
        ("pynput", "pynput"),
        ("pyperclip", "pyperclip"),
        ("appdirs", "appdirs"),
    ]
    
    for module, display in modules_to_check:
        if not check_module(module, display):
            all_ok = False
    
    # Check platform-specific
    check_platform_specific()
    
    # Check directories
    try:
        check_directories()
    except Exception as e:
        print(f"\n⚠️  Directory check failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok:
        print("✅ Installation verification successful!")
        print("\nYou can now run OmniScreen:")
        print("  python main.py")
    else:
        print("⚠️  Some dependencies are missing!")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("=" * 70)
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
