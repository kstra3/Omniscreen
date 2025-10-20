# Installation Guide

## Prerequisites

### All Platforms

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure Python is added to PATH

2. **pip** (usually comes with Python)
   ```bash
   python --version
   pip --version
   ```

### Platform-Specific Requirements

#### Windows

- **Visual C++ Redistributable**
  - Required for some Python packages
  - Download from [Microsoft](https://aka.ms/vs/17/release/vc_redist.x64.exe)

- **Administrator privileges** (for global hotkeys)

#### macOS

- **Xcode Command Line Tools**
  ```bash
  xcode-select --install
  ```

- **Homebrew** (optional but recommended)
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev
sudo apt-get install python3-xlib scrot xclip
sudo apt-get install libx11-dev libxtst-dev
```

For other distributions, install equivalent packages.

## Installation Steps

### 1. Clone or Download

```bash
# Clone repository
git clone https://github.com/yourusername/OmniScreen.git
cd OmniScreen

# Or download and extract ZIP
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter errors:

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Run tests
python -m pytest tests/

# Try CLI
python main.py capture --fullscreen --clipboard

# Launch GUI
python main.py
```

## First Run

1. **Grant Permissions**

   - **macOS**: Allow accessibility and screen recording permissions when prompted
   - **Linux**: May need to run with appropriate permissions for global hotkeys

2. **Configure Settings**

   - Launch the app: `python main.py`
   - Click "Settings" to configure:
     - Screenshot save location
     - Hotkeys
     - File naming patterns
     - Notifications

3. **Test Capture**

   - Try each capture mode
   - Verify screenshots are saved correctly
   - Test clipboard functionality

## Troubleshooting

### Import Errors

```bash
# If PyQt6 fails to install
pip install --upgrade PyQt6

# If Pillow fails
pip install --upgrade Pillow

# Platform-specific issues
# Windows: Install pywin32
pip install pywin32

# macOS: Install pyobjc
pip install pyobjc-framework-Cocoa pyobjc-framework-Quartz

# Linux: Install python-xlib
pip install python-xlib
```

### Permission Issues

**macOS:**
- Go to System Preferences > Security & Privacy > Privacy
- Enable Screen Recording for Terminal/Python
- Enable Accessibility for global hotkeys

**Linux:**
- For global hotkeys, you may need to run with appropriate permissions
- Some desktop environments may require additional configuration

### Hotkeys Not Working

1. Check if another application is using the same hotkey
2. Try different key combinations
3. Run with administrator/root privileges
4. Check logs in `~/.local/share/OmniScreen/logs/` (Linux/macOS) or `%APPDATA%/OmniScreen/logs/` (Windows)

### GUI Not Starting

```bash
# Check Qt platform plugin
export QT_DEBUG_PLUGINS=1  # Linux/macOS
set QT_DEBUG_PLUGINS=1     # Windows
python main.py

# Try setting Qt platform
export QT_QPA_PLATFORM=xcb  # Linux
python main.py
```

## Development Setup

For development:

```bash
# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Run tests
python -m pytest tests/ -v

# Code formatting
black .

# Type checking
mypy .
```

## Building Executable

### Windows (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --name OmniScreen --windowed --icon=assets/icons/icon.ico main.py
```

### macOS (py2app)

```bash
pip install py2app
python setup.py py2app
```

### Linux (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --name omniscreen --onefile main.py
```

## Uninstallation

1. Deactivate virtual environment (if used):
   ```bash
   deactivate
   ```

2. Remove application directory

3. Remove configuration (optional):
   - Windows: Delete `%APPDATA%/OmniScreen`
   - macOS: Delete `~/Library/Application Support/OmniScreen`
   - Linux: Delete `~/.config/OmniScreen` and `~/.local/share/OmniScreen`

## Getting Help

- Check the [README.md](README.md) for usage instructions
- Review logs in the logs directory
- Open an issue on GitHub with:
  - Your OS and Python version
  - Error messages
  - Log files (if applicable)

---

*Καλή τύχη! (Good luck!)*
