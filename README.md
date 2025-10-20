# OmniScreen 📸

**OmniScreen** is a cross-platform screenshot application inspired by ancient Greek aesthetics. Capture your screen with the elegance of classical antiquity.

## Features

- 🖥️ **Multi-platform**: Windows, macOS, and Linux support
- 📷 **Multiple capture modes**: Full screen, window, or custom region
- 🖼️ **Multi-monitor support**: Seamless capturing across all displays
- 🏛️ **Ancient Greek theme**: Beautiful UI with pastel colors and classical fonts
- 📂 **Smart organization**: Automatic naming with timestamps and window names
- 🔍 **Searchable history**: Easy retrieval of past screenshots
- ⌨️ **Global hotkeys**: Configurable keyboard shortcuts (default: Ctrl+Shift+S)
- 📋 **Clipboard integration**: Copy screenshots directly to clipboard
- ⏰ **Auto-delete**: Set expiration rules for old screenshots
- 🔧 **CLI interface**: Quick command-line access
- 🔔 **Notifications**: Visual and audio feedback
- ♿ **Accessible**: Full keyboard navigation and high-contrast mode
- 🌍 **Localization-ready**: Structured for easy translation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone or download the repository
cd OmniScreen

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Platform-Specific Notes

#### Windows
- Run with administrator privileges for global hotkey support
- Install Visual C++ Redistributable if needed

#### macOS
- Grant accessibility permissions when prompted
- Allow screen recording in System Preferences > Security & Privacy

#### Linux
- Install X11 dependencies: `sudo apt-get install python3-xlib`
- For Wayland, some features may be limited

## Usage

### GUI Mode

Launch the application:
```bash
python main.py
```

### CLI Mode

```bash
# Capture full screen
python main.py capture --fullscreen

# Capture active window
python main.py capture --window

# Capture region (interactive)
python main.py capture --region

# View history
python main.py history

# Configure settings
python main.py config --hotkey "ctrl+alt+s"
```

### Global Hotkeys

- **Ctrl+Shift+S**: Quick capture (configurable)
- **Ctrl+Shift+W**: Capture active window
- **Ctrl+Shift+R**: Capture region

## Configuration

Settings are stored in:
- Windows: `%APPDATA%/OmniScreen/config.json`
- macOS: `~/Library/Application Support/OmniScreen/config.json`
- Linux: `~/.config/OmniScreen/config.json`

### Customizable Settings

- Screenshot save location
- File naming patterns
- Hotkey combinations
- Auto-delete rules
- Notification preferences
- Theme customization

## Project Structure

```
OmniScreen/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── logger.py              # Logging setup
├── core/
│   ├── capture.py         # Screenshot capture engine
│   ├── storage.py         # File management & organization
│   ├── hotkey.py          # Global hotkey handling
│   └── clipboard.py       # Clipboard operations
├── gui/
│   ├── main_window.py     # Main GUI window
│   ├── theme.py           # Greek-inspired theme
│   ├── history.py         # Screenshot history panel
│   ├── settings.py        # Settings dialog
│   └── region_selector.py # Region selection overlay
├── cli/
│   └── commands.py        # CLI command handler
├── utils/
│   ├── platform_utils.py  # Platform-specific utilities
│   ├── notification.py    # Notification system
│   └── window_info.py     # Window detection
├── tests/
│   ├── test_capture.py
│   ├── test_storage.py
│   └── test_hotkey.py
└── assets/
    ├── fonts/            # Greek-inspired fonts
    ├── icons/            # Application icons
    └── sounds/           # Notification sounds
```

## Ancient Greek Design Philosophy

The UI embodies the principles of ancient Greek design:

- **Harmony (Ἁρμονία)**: Balanced proportions inspired by the golden ratio
- **Simplicity (Ἁπλότης)**: Clean, uncluttered interface
- **Beauty (Κάλλος)**: Aesthetic pastel colors and classical typography
- **Functionality (Χρησιμότης)**: Practical tools in an elegant package

UI elements reference:
- Column capitals for borders and dividers
- Olive wreath motifs for success indicators
- Greek key patterns for decorative elements
- Temples and amphoras as iconography

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- New features include documentation
- Commit messages are descriptive

## License

MIT License - See LICENSE file for details

## Credits

Fonts:
- GFS Didot: Greek Font Society
- EB Garamond: Open source classical font

Inspired by the timeless beauty of ancient Greek art and architecture.

---

*"Ἐν ἀρχῇ ἦν ὁ λόγος" - In the beginning was the word*
