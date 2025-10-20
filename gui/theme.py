"""
Greek-Inspired Theme Module

Implements the ancient Greek aesthetic with pastel colors, classical fonts,
and decorative motifs. Every element reflects the timeless beauty of
Hellenic art and architecture.
"""

from PyQt6.QtGui import QFont, QColor, QPalette, QFontDatabase
from PyQt6.QtCore import Qt
from pathlib import Path
from logger import get_logger


logger = get_logger(__name__)


class GreekTheme:
    """
    Embodies the aesthetic principles of ancient Greece.
    
    Color Palette (Τὰ Χρώματα):
    - Marble White: #F5F5F0 - Pure as Pentelic marble
    - Aegean Blue: #6B9BD1 - The color of Greek seas
    - Olive Green: #9CAF88 - Sacred olive groves
    - Golden Laurel: #D4AF37 - Victory wreaths
    - Terracotta: #D2691E - Ancient pottery
    - Parchment: #F0E6D2 - Aged scrolls
    - Shadow Gray: #808080 - Stone shadows
    """
    
    # Color definitions - The palette of the gods
    MARBLE_WHITE = "#F5F5F0"
    AEGEAN_BLUE = "#6B9BD1"
    OLIVE_GREEN = "#9CAF88"
    GOLDEN_LAUREL = "#D4AF37"
    TERRACOTTA = "#D2691E"
    PARCHMENT = "#F0E6D2"
    SHADOW_GRAY = "#808080"
    DEEP_BLUE = "#2C3E50"
    
    # Font family preferences
    FONT_FAMILIES = [
        "EB Garamond",
        "GFS Didot",
        "Palatino Linotype",
        "Georgia",
        "Times New Roman"
    ]
    
    @staticmethod
    def get_stylesheet() -> str:
        """
        Get the complete stylesheet for the Greek theme.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
        /* Main Window - The Temple */
        QMainWindow {{
            background-color: {GreekTheme.MARBLE_WHITE};
            color: {GreekTheme.DEEP_BLUE};
        }}
        
        /* Central Widget */
        QWidget {{
            background-color: {GreekTheme.MARBLE_WHITE};
            color: {GreekTheme.DEEP_BLUE};
            font-family: "EB Garamond", "Georgia", serif;
            font-size: 12pt;
        }}
        
        /* Buttons - Carved Stone Tablets */
        QPushButton {{
            background-color: {GreekTheme.PARCHMENT};
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            color: white;
            border-color: {GreekTheme.GOLDEN_LAUREL};
        }}
        
        QPushButton:pressed {{
            background-color: {GreekTheme.OLIVE_GREEN};
            border-color: {GreekTheme.TERRACOTTA};
        }}
        
        QPushButton:disabled {{
            background-color: {GreekTheme.SHADOW_GRAY};
            color: {GreekTheme.MARBLE_WHITE};
            border-color: {GreekTheme.SHADOW_GRAY};
        }}
        
        /* Primary Action Button - Golden Highlight */
        QPushButton[primary="true"] {{
            background-color: {GreekTheme.GOLDEN_LAUREL};
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.TERRACOTTA};
            font-size: 13pt;
        }}
        
        QPushButton[primary="true"]:hover {{
            background-color: {GreekTheme.TERRACOTTA};
            color: white;
        }}
        
        /* Labels - Inscriptions */
        QLabel {{
            color: {GreekTheme.DEEP_BLUE};
            background-color: transparent;
            padding: 4px;
        }}
        
        QLabel[heading="true"] {{
            font-size: 18pt;
            font-weight: bold;
            color: {GreekTheme.TERRACOTTA};
            padding: 10px 0px;
        }}
        
        QLabel[subheading="true"] {{
            font-size: 14pt;
            font-weight: bold;
            color: {GreekTheme.OLIVE_GREEN};
            padding: 6px 0px;
        }}
        
        /* Input Fields - Wax Tablets */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: white;
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-radius: 3px;
            padding: 6px;
            selection-background-color: {GreekTheme.AEGEAN_BLUE};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {GreekTheme.AEGEAN_BLUE};
            background-color: {GreekTheme.PARCHMENT};
        }}
        
        /* Combo Boxes - Scroll Selectors */
        QComboBox {{
            background-color: white;
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-radius: 3px;
            padding: 5px;
            min-width: 100px;
        }}
        
        QComboBox:hover {{
            border-color: {GreekTheme.AEGEAN_BLUE};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid {GreekTheme.OLIVE_GREEN};
            margin-right: 5px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: white;
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            selection-background-color: {GreekTheme.AEGEAN_BLUE};
        }}
        
        /* List Widget - Catalog of Records */
        QListWidget {{
            background-color: white;
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-radius: 5px;
            padding: 5px;
        }}
        
        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {GreekTheme.PARCHMENT};
        }}
        
        QListWidget::item:selected {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            color: white;
        }}
        
        QListWidget::item:hover {{
            background-color: {GreekTheme.PARCHMENT};
        }}
        
        /* Scroll Bars - Papyrus Scrolls */
        QScrollBar:vertical {{
            background-color: {GreekTheme.PARCHMENT};
            width: 12px;
            border: 1px solid {GreekTheme.OLIVE_GREEN};
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {GreekTheme.OLIVE_GREEN};
            min-height: 20px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {GreekTheme.AEGEAN_BLUE};
        }}
        
        QScrollBar:horizontal {{
            background-color: {GreekTheme.PARCHMENT};
            height: 12px;
            border: 1px solid {GreekTheme.OLIVE_GREEN};
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {GreekTheme.OLIVE_GREEN};
            min-width: 20px;
            border-radius: 5px;
        }}
        
        /* Group Box - Framed Sections */
        QGroupBox {{
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            color: {GreekTheme.TERRACOTTA};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 5px;
            background-color: {GreekTheme.MARBLE_WHITE};
        }}
        
        /* Tab Widget - Multiple Scrolls */
        QTabWidget::pane {{
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-radius: 5px;
            background-color: white;
        }}
        
        QTabBar::tab {{
            background-color: {GreekTheme.PARCHMENT};
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 8px 16px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: white;
            color: {GreekTheme.TERRACOTTA};
            font-weight: bold;
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            color: white;
        }}
        
        /* Check Boxes and Radio Buttons */
        QCheckBox, QRadioButton {{
            color: {GreekTheme.DEEP_BLUE};
            spacing: 8px;
        }}
        
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {GreekTheme.OLIVE_GREEN};
            background-color: white;
        }}
        
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            border-color: {GreekTheme.GOLDEN_LAUREL};
        }}
        
        QRadioButton::indicator {{
            border-radius: 9px;
        }}
        
        /* Status Bar - The Oracle's Messages */
        QStatusBar {{
            background-color: {GreekTheme.PARCHMENT};
            color: {GreekTheme.DEEP_BLUE};
            border-top: 2px solid {GreekTheme.OLIVE_GREEN};
            font-style: italic;
        }}
        
        /* Menu Bar - The Symposium */
        QMenuBar {{
            background-color: {GreekTheme.PARCHMENT};
            color: {GreekTheme.DEEP_BLUE};
            border-bottom: 2px solid {GreekTheme.OLIVE_GREEN};
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            color: white;
        }}
        
        QMenu {{
            background-color: {GreekTheme.PARCHMENT};
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.OLIVE_GREEN};
        }}
        
        QMenu::item {{
            padding: 6px 24px 6px 12px;
        }}
        
        QMenu::item:selected {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            color: white;
        }}
        
        /* Sliders - Mechanical Adjustments */
        QSlider::groove:horizontal {{
            border: 1px solid {GreekTheme.OLIVE_GREEN};
            height: 6px;
            background-color: {GreekTheme.PARCHMENT};
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {GreekTheme.AEGEAN_BLUE};
            border: 2px solid {GreekTheme.GOLDEN_LAUREL};
            width: 14px;
            margin: -5px 0;
            border-radius: 7px;
        }}
        
        /* Tool Tips - Divine Whispers */
        QToolTip {{
            background-color: {GreekTheme.PARCHMENT};
            color: {GreekTheme.DEEP_BLUE};
            border: 2px solid {GreekTheme.GOLDEN_LAUREL};
            padding: 5px;
            border-radius: 3px;
            font-size: 11pt;
        }}
        """
    
    @staticmethod
    def setup_fonts():
        """
        Load and register custom Greek fonts if available.
        
        Attempts to load classical fonts for the authentic experience.
        """
        try:
            # Try to load custom fonts from assets
            font_dir = Path(__file__).parent.parent / "assets" / "fonts"
            if font_dir.exists():
                for font_file in font_dir.glob("*.ttf"):
                    font_id = QFontDatabase.addApplicationFont(str(font_file))
                    if font_id != -1:
                        families = QFontDatabase.applicationFontFamilies(font_id)
                        logger.info(f"Loaded font: {families}")
        except Exception as e:
            logger.debug(f"Custom fonts not loaded: {e}")
    
    @staticmethod
    def get_default_font() -> QFont:
        """
        Get the default application font.
        
        Returns:
            QFont instance with Greek styling
        """
        font = QFont()
        
        # Try to use preferred fonts
        for family in GreekTheme.FONT_FAMILIES:
            font.setFamily(family)
            if font.family() == family:
                break
        
        font.setPointSize(12)
        return font
    
    @staticmethod
    def get_heading_font(size: int = 18) -> QFont:
        """
        Get font for headings.
        
        Args:
            size: Font size in points
        
        Returns:
            QFont instance
        """
        font = GreekTheme.get_default_font()
        font.setPointSize(size)
        font.setBold(True)
        return font
    
    @staticmethod
    def apply_theme(app):
        """
        Apply the Greek theme to the application.
        
        Args:
            app: QApplication instance
        """
        # Load custom fonts
        GreekTheme.setup_fonts()
        
        # Set default font
        app.setFont(GreekTheme.get_default_font())
        
        # Apply stylesheet
        app.setStyleSheet(GreekTheme.get_stylesheet())
        
        logger.info("Greek theme applied - Καλὴ ὄψις (Beautiful appearance)")
