"""
Region Selector Overlay

Provides an interactive overlay for selecting screenshot regions.
Like drawing borders on a map of conquered territories.
"""

from PyQt6.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QCursor
from logger import get_logger


logger = get_logger(__name__)


class RegionSelector(QWidget):
    """
    Fullscreen overlay for selecting screenshot regions.
    
    The canvas of selection - where users define their conquest area.
    """
    
    # Signal emitted when region is selected
    region_selected = pyqtSignal(int, int, int, int)  # x, y, width, height
    
    def __init__(self):
        """Initialize region selector."""
        super().__init__()
        
        self.start_point = None
        self.end_point = None
        self.rubber_band = None
        
        self._setup_ui()
        
        logger.debug("RegionSelector initialized")
    
    def _setup_ui(self):
        """Set up the overlay UI."""
        # Make window frameless and always on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Set transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set cursor to crosshair
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        
        # Create rubber band for selection
        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
    
    def show_fullscreen(self):
        """Show the selector in fullscreen mode."""
        # Get total screen geometry (all monitors)
        screen_geometry = QApplication.primaryScreen().virtualGeometry()
        
        self.setGeometry(screen_geometry)
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        
        logger.debug(f"RegionSelector shown fullscreen: {screen_geometry}")
    
    def paintEvent(self, event):
        """Paint the overlay with semi-transparent background."""
        painter = QPainter(self)
        
        # Draw semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        # If selection is active, draw highlighted area
        if self.start_point and self.end_point:
            # Draw selection rectangle outline
            pen = QPen(QColor(107, 155, 209), 2, Qt.PenStyle.SolidLine)  # Aegean Blue
            painter.setPen(pen)
            
            rect = QRect(self.start_point, self.end_point).normalized()
            
            # Clear the selected area (make it see-through)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, Qt.GlobalColor.transparent)
            
            # Draw border
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.drawRect(rect)
            
            # Draw corner handles
            handle_size = 8
            handles = [
                rect.topLeft(),
                QPoint(rect.right(), rect.top()),
                QPoint(rect.left(), rect.bottom()),
                rect.bottomRight()
            ]
            
            painter.setBrush(QColor(212, 175, 55))  # Golden Laurel
            for handle_pos in handles:
                handle_rect = QRect(
                    handle_pos.x() - handle_size // 2,
                    handle_pos.y() - handle_size // 2,
                    handle_size,
                    handle_size
                )
                painter.drawRect(handle_rect)
            
            # Draw dimensions text
            width = rect.width()
            height = rect.height()
            text = f"{width} × {height}"
            
            painter.setPen(QPen(Qt.GlobalColor.white))
            painter.drawText(
                rect.center().x() - 50,
                rect.top() - 10,
                text
            )
        
        painter.end()
    
    def mousePressEvent(self, event):
        """Handle mouse press - start selection."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.rubber_band.setGeometry(QRect(self.start_point, self.end_point))
            self.rubber_band.show()
            self.update()
            logger.debug(f"Selection started at {self.start_point}")
    
    def mouseMoveEvent(self, event):
        """Handle mouse move - update selection."""
        if self.start_point:
            self.end_point = event.pos()
            self.rubber_band.setGeometry(QRect(self.start_point, self.end_point).normalized())
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - complete selection."""
        if event.button() == Qt.MouseButton.LeftButton and self.start_point:
            self.end_point = event.pos()
            
            # Calculate selection rectangle
            rect = QRect(self.start_point, self.end_point).normalized()
            
            x = rect.x()
            y = rect.y()
            width = rect.width()
            height = rect.height()
            
            # Only emit if selection has size
            if width > 5 and height > 5:
                logger.info(f"Region selected: x={x}, y={y}, w={width}, h={height}")
                self.region_selected.emit(x, y, width, height)
            else:
                logger.debug("Selection too small, cancelled")
            
            # Close the selector
            self.close()
    
    def keyPressEvent(self, event):
        """Handle key press - cancel with Escape."""
        if event.key() == Qt.Key.Key_Escape:
            logger.debug("Selection cancelled by user")
            self.close()
