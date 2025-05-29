from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        try:
            self.code_editor.line_number_area_paint_event(event)
        except Exception as e:
            # Fallback to prevent crashes
            from PySide6.QtGui import QPainter
            painter = QPainter(self)
            painter.fillRect(event.rect(), QColor(40, 40, 40))