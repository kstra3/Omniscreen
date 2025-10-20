# Quick Start Guide

Get started with OmniScreen in 5 minutes!

## Installation

```bash
# 1. Install Python 3.8+ (if not already installed)
# Download from python.org

# 2. Navigate to OmniScreen directory
cd OmniScreen

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run OmniScreen
python main.py
```

## Basic Usage

### GUI Mode (Recommended)

```bash
python main.py
```

**Main Window Features:**
- **Capture Full Screen** - Captures your entire screen
- **Capture Active Window** - Captures the currently focused window
- **Capture Region** - Select a custom area to capture
- **History** - View and manage past screenshots
- **Settings** - Configure OmniScreen

**Global Hotkeys** (configurable):
- `Ctrl+Shift+S` - Quick fullscreen capture
- `Ctrl+Shift+W` - Capture active window
- `Ctrl+Shift+R` - Select region to capture

### CLI Mode

```bash
# Capture fullscreen
python main.py capture --fullscreen

# Capture and copy to clipboard
python main.py capture --fullscreen --clipboard

# View recent screenshots
python main.py history --limit 5

# Search history
python main.py history --search "Chrome"

# Show configuration
python main.py config --show
```

## Common Tasks

### Taking Your First Screenshot

1. Launch OmniScreen: `python main.py`
2. Click "Capture Full Screen" or press `Ctrl+Shift+S`
3. Check your Pictures/OmniScreen folder for the screenshot

### Changing Save Location

1. Click "Settings" in main window
2. Go to "Storage" tab
3. Click "Browse..." to select new location
4. Click "Save"

### Setting Up Hotkeys

1. Click "Settings"
2. Go to "Hotkeys" tab
3. Enter your preferred key combination (e.g., `ctrl+alt+s`)
4. Click "Save"

### Viewing Screenshot History

1. Click "History" button in main window
2. Use search box to filter screenshots
3. Double-click to open a screenshot
4. Right-click for more options

## First-Time Setup Tips

### 1. Configure Save Location

Choose a convenient location for screenshots:
- Default: `~/Pictures/OmniScreen`
- Recommended: Create a dedicated folder

### 2. Test Each Capture Mode

Try all three modes to see what works best:
- **Fullscreen**: Great for documenting entire screen
- **Window**: Perfect for application-specific captures
- **Region**: Ideal for precise selections

### 3. Set Up Auto-Organization

In Settings > Storage:
- Enable "Organize by Date" for time-based filing
- Or "Organize by Application" for app-based filing

### 4. Enable Notifications

In Settings > Notifications:
- Check "Enable notifications"
- Check "Play sound on capture"

## Troubleshooting Quick Fixes

### Screenshots Not Saving

1. Check Settings > Storage > Save Location is writable
2. Ensure sufficient disk space
3. Check logs: Look in the logs folder for error messages

### Hotkeys Not Working

1. Try different key combinations (avoid conflicts)
2. Run as administrator (Windows)
3. Grant accessibility permissions (macOS)
4. Check Settings > Hotkeys > Background Service is enabled

### Application Won't Start

```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for errors
python main.py --help
```

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [INSTALLATION.md](INSTALLATION.md) for platform-specific setup
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore Settings to customize your experience

## Keyboard Shortcuts Reference

| Action | Default Shortcut | Configurable |
|--------|-----------------|--------------|
| Quick Capture | Ctrl+Shift+S | ✅ Yes |
| Window Capture | Ctrl+Shift+W | ✅ Yes |
| Region Capture | Ctrl+Shift+R | ✅ Yes |
| Open Settings | Ctrl+, | ❌ No |
| Open History | Ctrl+H | ❌ No |
| Quit | Ctrl+Q | ❌ No |

## Example Workflows

### Workflow 1: Quick Documentation

1. Press `Ctrl+Shift+S` (or your configured hotkey)
2. Screenshot saved automatically
3. Access from system notification or History panel

### Workflow 2: Selective Capture

1. Press `Ctrl+Shift+R`
2. Click and drag to select region
3. Release to capture
4. Screenshot saved and/or copied to clipboard

### Workflow 3: Window-Specific Capture

1. Focus the window you want to capture
2. Press `Ctrl+Shift+W`
3. Screenshot named with window title

### Workflow 4: Clipboard-Only Mode

1. Settings > General > Check "Copy to clipboard on capture"
2. Uncheck "Save file and copy to clipboard" if you only want clipboard
3. Now all captures go directly to clipboard

## Getting Help

- **Logs**: Check `~/.local/share/OmniScreen/logs/` (Linux/macOS) or `%APPDATA%/OmniScreen/logs/` (Windows)
- **Config**: Located in `~/.config/OmniScreen/config.json` (Linux/macOS) or `%APPDATA%/OmniScreen/config.json` (Windows)
- **Screenshots**: Default in `~/Pictures/OmniScreen` or your configured location

## Tips & Tricks

1. **Use the system tray icon** for quick access without opening the main window
2. **Enable auto-delete** to automatically clean up old screenshots
3. **Organize by date** for chronological filing
4. **Use search in History** to quickly find specific screenshots
5. **Customize hotkeys** to match your workflow

---

**Ready to capture? Run `python main.py` and start screenshotting!**

*Χαίρε! (Rejoice!)* 🏛️
