# OmniScreen Project Summary

## Overview

**OmniScreen** is a cross-platform screenshot application with an ancient Greek-inspired aesthetic. It provides powerful screenshot capabilities wrapped in a beautiful, classical UI design.

## Project Statistics

- **Total Files**: 28 Python files + documentation
- **Lines of Code**: ~4,000+ lines
- **Modules**: 4 main modules (core, gui, cli, utils)
- **Test Coverage**: Unit tests for core functionality
- **Supported Platforms**: Windows, macOS, Linux

## Architecture

### Core Components

1. **Configuration System** (`config.py`)
   - JSON-based persistent configuration
   - Platform-specific paths
   - Default settings with user overrides

2. **Logging System** (`logger.py`)
   - Rotating file logs
   - Color-coded console output
   - Comprehensive error tracking

3. **Screenshot Capture** (`core/capture.py`)
   - Three capture modes: fullscreen, window, region
   - Multi-monitor support
   - MSS-based fast capture

4. **Storage Management** (`core/storage.py`)
   - SQLite database for history
   - Automated organization (by date/application)
   - File naming patterns
   - Auto-delete old screenshots

5. **Clipboard Integration** (`core/clipboard.py`)
   - Platform-specific clipboard handling
   - Image and text copying
   - Fallback mechanisms

6. **Global Hotkeys** (`core/hotkey.py`)
   - System-wide keyboard shortcuts
   - Configurable key combinations
   - Background listener service

### GUI Components

1. **Main Window** (`gui/main_window.py`)
   - Primary application interface
   - Capture mode selection
   - System tray integration
   - Menu system

2. **Greek Theme** (`gui/theme.py`)
   - Custom stylesheet
   - Pastel color palette
   - Classical fonts
   - Consistent aesthetic

3. **History Panel** (`gui/history.py`)
   - Screenshot browser
   - Search functionality
   - Management tools
   - Thumbnail preview

4. **Settings Dialog** (`gui/settings.py`)
   - Tabbed configuration interface
   - Live settings updates
   - Validation and feedback

5. **Region Selector** (`gui/region_selector.py`)
   - Fullscreen overlay
   - Interactive selection
   - Visual feedback
   - Dimension display

### Utilities

1. **Platform Utilities** (`utils/platform_utils.py`)
   - Platform detection
   - Window information retrieval
   - OS-specific adaptations

2. **Notifications** (`utils/notification.py`)
   - System notifications
   - Sound feedback
   - Platform-specific implementations

3. **Window Info** (`utils/window_info.py`)
   - Window detection
   - Name sanitization
   - Window enumeration

### CLI Interface

1. **Command Handler** (`cli/commands.py`)
   - Argument parsing
   - Command dispatch
   - Non-interactive operations

## Features Implemented

### Screenshot Capabilities
✅ Full screen capture
✅ Active window capture
✅ Custom region selection
✅ Multi-monitor support
✅ Configurable output format (PNG, JPG, BMP)

### Organization
✅ Automatic file naming with timestamps
✅ Window name integration
✅ Date-based folder organization
✅ Application-based organization
✅ Custom naming patterns

### History & Search
✅ SQLite database storage
✅ Full-text search
✅ Pagination support
✅ Screenshot metadata
✅ Management operations (view, delete, copy path)

### User Interface
✅ Ancient Greek theme
✅ Pastel color palette
✅ Classical fonts (EB Garamond, GFS Didot)
✅ System tray integration
✅ Intuitive controls
✅ Keyboard navigation

### Global Hotkeys
✅ Configurable shortcuts
✅ Background service
✅ Multiple hotkey support
✅ Cross-platform compatibility

### Clipboard
✅ Copy screenshots to clipboard
✅ Platform-specific implementations
✅ Save and copy mode
✅ Copy-only mode

### Auto-Management
✅ Auto-delete old screenshots
✅ Configurable retention period
✅ Background cleanup

### Configuration
✅ Persistent settings
✅ User-friendly settings dialog
✅ JSON configuration format
✅ Platform-appropriate paths

### CLI Interface
✅ Command-line operations
✅ Scripting support
✅ Configuration management
✅ History viewing

### Testing
✅ Unit tests for core modules
✅ Mock-based testing
✅ Test runner
✅ Coverage reporting

### Documentation
✅ Comprehensive README
✅ Installation guide
✅ Quick start guide
✅ Contributing guidelines
✅ Changelog
✅ Inline code documentation

## Technology Stack

### Core Dependencies
- **PyQt6**: GUI framework
- **Pillow**: Image processing
- **mss**: Fast screenshot capture
- **pynput**: Global hotkey handling
- **pyperclip**: Clipboard operations
- **appdirs**: Platform-specific paths

### Platform-Specific
- **pywin32** (Windows): Window management
- **pyobjc** (macOS): Window information
- **python-xlib** (Linux): X11 integration

### Development Tools
- **pytest**: Testing framework
- **unittest**: Unit testing
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## Design Principles

### 1. **Modularity**
- Clear separation of concerns
- Independent, testable modules
- Minimal coupling

### 2. **Cross-Platform**
- Platform detection layer
- OS-specific implementations
- Graceful fallbacks

### 3. **User Experience**
- Intuitive interface
- Consistent behavior
- Helpful error messages
- Visual feedback

### 4. **Aesthetic Excellence**
- Ancient Greek theme
- Pastel colors
- Classical typography
- Cultural references

### 5. **Maintainability**
- Comprehensive documentation
- Clear code structure
- Type hints
- Unit tests

### 6. **Extensibility**
- Plugin architecture ready
- Modular design
- Configuration-driven

## Greek Theme Elements

### Color Palette
- **Marble White** (#F5F5F0): Primary background
- **Aegean Blue** (#6B9BD1): Accents and highlights
- **Olive Green** (#9CAF88): Borders and secondary
- **Golden Laurel** (#D4AF37): Important actions
- **Terracotta** (#D2691E): Headers and warnings
- **Parchment** (#F0E6D2): Input backgrounds

### Typography
- EB Garamond (primary)
- GFS Didot (alternative)
- Palatino Linotype (fallback)
- Georgia (fallback)

### Cultural References
- Greek phrases in UI
- Mythology-inspired comments
- Classical design patterns
- Temple/column motifs

## File Organization

```
OmniScreen/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── logger.py              # Logging system
├── requirements.txt       # Dependencies
├── README.md              # Main documentation
├── QUICKSTART.md          # Quick start guide
├── INSTALLATION.md        # Installation instructions
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
├── LICENSE                # MIT License
├── .gitignore            # Git exclusions
│
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── capture.py        # Screenshot capture
│   ├── storage.py        # File management
│   ├── clipboard.py      # Clipboard operations
│   └── hotkey.py         # Global hotkeys
│
├── gui/                   # GUI components
│   ├── __init__.py
│   ├── main_window.py    # Main application window
│   ├── theme.py          # Greek theme styling
│   ├── history.py        # History browser
│   ├── settings.py       # Settings dialog
│   └── region_selector.py # Region selection overlay
│
├── cli/                   # CLI interface
│   ├── __init__.py
│   └── commands.py       # Command handling
│
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── platform_utils.py # Platform-specific code
│   ├── notification.py   # Notification system
│   └── window_info.py    # Window detection
│
└── tests/                 # Unit tests
    ├── __init__.py
    ├── test_capture.py
    ├── test_storage.py
    └── test_hotkey.py
```

## Future Enhancements

### Planned Features
- Plugin system for extensions
- Multiple language support
- Cloud storage integration
- OCR text extraction
- Video recording mode
- Screenshot annotations
- Custom notification sounds
- Scheduled captures

### Technical Improvements
- Increase test coverage
- Performance optimizations
- Memory usage reduction
- Better error recovery
- Enhanced logging

## Getting Started

### For Users
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

### For Developers
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Set up development environment
3. Run tests: `python -m pytest tests/`
4. Follow code style guidelines

### For Contributors
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Credits

- **Theme Inspiration**: Ancient Greek art and architecture
- **Fonts**: EB Garamond, GFS Didot (Greek Font Society)
- **Libraries**: PyQt6, Pillow, mss, pynput, and others

## License

MIT License - See [LICENSE](LICENSE) file

---

**OmniScreen** - Capturing moments with the elegance of ancient Greece

*Ἐν ἀρχῇ ἦν ὁ λόγος - In the beginning was the word*

🏛️ Built with passion for beauty, functionality, and history 🏛️
