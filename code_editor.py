from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QFont
from PySide6.QtWidgets import QCompleter, QTextEdit
from keywords import keywords
from syntax_highlighter import SyntaxHighlighter


class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 12))
        self.highlighter = None
        self.completer = None
        self.language = ""

    def set_language(self, language):
        self.language = language
        self.highlighter = SyntaxHighlighter(self.document(), language)
        self.setup_completer(language)

    def setup_completer(self, language):
        if language.lower() in keywords:
            self.completer = QCompleter(keywords[language.lower()])
            self.completer.setWidget(self)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        super().keyPressEvent(event)

        if self.completer:
            tc = self.textCursor()
            tc.select(QTextCursor.WordUnderCursor)
            cr = self.cursorRect()

            if len(tc.selectedText()) > 2:
                self.completer.setCompletionPrefix(tc.selectedText())
                popup = self.completer.popup()
                popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
                cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                            + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cr)
            else:
                self.completer.popup().hide()

    # Add after the keyPressEvent method in CodeEditor class (around line 140):
    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            # Zoom functionality with Ctrl + mouse wheel
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        font = self.font()
        current_size = font.pointSize()
        if current_size < 72:  # Maximum zoom limit
            font.setPointSize(current_size + 1)
            self.setFont(font)

    def zoom_out(self):
        font = self.font()
        current_size = font.pointSize()
        if current_size > 6:  # Minimum zoom limit
            font.setPointSize(current_size - 1)
            self.setFont(font)

