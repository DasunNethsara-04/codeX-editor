from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTextEdit

from code_editor import CodeEditor
from line_numbers_area import LineNumberArea

class CodeEditorWithLineNumbers(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.line_number_area = LineNumberArea(self)
        self.editor = CodeEditor()

        layout.addWidget(self.line_number_area)
        layout.addWidget(self.editor)

        # Connect signals
        self.editor.document().blockCountChanged.connect(self.update_line_number_area_width)
        self.editor.verticalScrollBar().valueChanged.connect(self.update_line_numbers)
        self.editor.cursorPositionChanged.connect(self.highlight_current_line)
        self.editor.textChanged.connect(self.line_number_area.update)
        self.editor.document().documentLayoutChanged.connect(self.line_number_area.update)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.editor.document().blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.editor.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_numbers(self):
        """Update line numbers when scrolling"""
        self.line_number_area.update()

    def wheelEvent(self, event):
        """Handle wheel events to update line numbers"""
        super().wheelEvent(event)
        self.line_number_area.update()

    def update_line_number_area_width(self, new_block_count):
        width = self.line_number_area_width()
        self.line_number_area.setFixedWidth(width)
        self.editor.setViewportMargins(width, 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        self.line_number_area.setGeometry(0, 0, width, cr.height())
        # Trigger line number update after resize
        QTimer.singleShot(0, self.line_number_area.update)

    def line_number_area_paint_event(self, event):
        from PySide6.QtGui import QPainter

        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(40, 40, 40))
        painter.setPen(QColor(120, 120, 120))

        # Get the first visible block and its geometry
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()

        # Get the geometry of the first visible block
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        # Paint line numbers for all visible blocks
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width() - 3,
                                 self.editor.fontMetrics().height(),
                                 Qt.AlignRight | Qt.AlignVCenter, number)

            block = block.next()
            if block.isValid():
                top = bottom
                bottom = top + int(self.editor.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.editor.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(40, 40, 40)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
            selection.cursor = self.editor.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.editor.setExtraSelections(extra_selections)

