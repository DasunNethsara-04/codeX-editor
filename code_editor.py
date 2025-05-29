from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QFont
from PySide6.QtWidgets import QCompleter, QTextEdit
from keywords import keywords, get_keywords, get_functions
from syntax_highlighter import SyntaxHighlighter
import re


class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Cascadia Code", 12))
        self.highlighter = None
        self.completer = None
        self.language = ""

    def set_language(self, language):
        self.language = language
        self.highlighter = SyntaxHighlighter(self.document(), language)
        self.setup_completer(language)

    def setup_completer(self, language):
        if language.lower() in keywords:
            from keywords import get_all_suggestions
            all_suggestions = get_all_suggestions(language)
            self.completer = QCompleter(all_suggestions)
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

        # Handle Enter key for auto-indentation
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.handle_enter_key()
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

    def handle_enter_key(self):
        cursor = self.textCursor()
        current_line = cursor.block().text()

        # Get current indentation
        indent_match = re.match(r'^(\s*)', current_line)
        current_indent = indent_match.group(1) if indent_match else ""

        # Insert new line
        cursor.insertText('\n')

        # Determine if we need extra indentation
        extra_indent = self.get_extra_indentation(current_line)

        # Insert indentation
        new_indent = current_indent + extra_indent
        cursor.insertText(new_indent)

        self.setTextCursor(cursor)

    def get_extra_indentation(self, line):
        """Determine extra indentation needed based on the current line"""
        stripped_line = line.strip()

        if not stripped_line:
            return ""

        # HTML indentation rules
        html_indent_triggers = [
            r'<[^/!][^>]*[^/]>\s*',
            r'^\s*<(html|head|body|div|p|h[1-6]|ul|ol|li|table|thead|tbody|tr|td|th|form|fieldset|legend|script|style|section|article|header|footer|nav|aside|main|figure|figcaption|blockquote|pre|code)\b[^>]*>\s*'
        ]

        # CSS indentation rules
        css_indent_triggers = [
            r'{\s*',
            r'^\s*[^{}]+{\s*',
            r'^\s*@media\s+[^{]+{\s*',
            r'^\s*@keyframes\s+[^{]+{\s*',
            r'^\s*@[^{]+{\s*'
        ]

        # JavaScript indentation rules
        js_indent_triggers = [
            r'{\s*',
            r'^\s*if\s*\([^)]*\)\s*{\s*',
            r'^\s*else\s*if\s*\([^)]*\)\s*{\s*',
            r'^\s*else\s*{\s*',
            r'^\s*for\s*\([^)]*\)\s*{\s*',
            r'^\s*while\s*\([^)]*\)\s*{\s*',
            r'^\s*do\s*{\s*',
            r'^\s*switch\s*\([^)]*\)\s*{\s*',
            r'^\s*case\s+.*:\s*',
            r'^\s*default\s*:\s*',
            r'^\s*function\s*[^{]*{\s*',
            r'^\s*\w+\s*:\s*function\s*[^{]*{\s*',
            r'^\s*try\s*{\s*',
            r'^\s*catch\s*\([^)]*\)\s*{\s*',
            r'^\s*finally\s*{\s*'
        ]

        # PHP indentation rules
        php_indent_triggers = [
            r'{\s*',
            r'^\s*if\s*\([^)]*\)\s*{\s*',
            r'^\s*elseif\s*\([^)]*\)\s*{\s*',
            r'^\s*else\s*{\s*',
            r'^\s*for\s*\([^)]*\)\s*{\s*',
            r'^\s*foreach\s*\([^)]*\)\s*{\s*',
            r'^\s*while\s*\([^)]*\)\s*{\s*',
            r'^\s*do\s*{\s*',
            r'^\s*switch\s*\([^)]*\)\s*{\s*',
            r'^\s*case\s+.*:\s*',
            r'^\s*default\s*:\s*',
            r'^\s*function\s+[^{]*{\s*',
            r'^\s*class\s+[^{]*{\s*',
            r'^\s*interface\s+[^{]*{\s*',
            r'^\s*trait\s+[^{]*{\s*',
            r'^\s*try\s*{\s*',
            r'^\s*catch\s*\([^)]*\)\s*{\s*',
            r'^\s*finally\s*{\s*',
            r'^\s*\?\>\s*'
        ]

        # SQL indentation rules
        sql_indent_triggers = [
            r'^\s*SELECT\s+',
            r'^\s*FROM\s+',
            r'^\s*WHERE\s+',
            r'^\s*JOIN\s+',
            r'^\s*INNER\s+JOIN\s+',
            r'^\s*LEFT\s+JOIN\s+',
            r'^\s*RIGHT\s+JOIN\s+',
            r'^\s*FULL\s+JOIN\s+',
            r'^\s*GROUP\s+BY\s+',
            r'^\s*ORDER\s+BY\s+',
            r'^\s*HAVING\s+',
            r'^\s*UNION\s+',
            r'^\s*CASE\s+',
            r'^\s*WHEN\s+',
            r'^\s*BEGIN\s*',
            r'^\s*IF\s+.*THEN\s*',
            r'^\s*ELSE\s*',
            r'^\s*WHILE\s+.*DO\s*',
            r'^\s*FOR\s+.*DO\s*'
        ]

        python_indent_triggers = [
            r':\s*',
            r'^\s*if\s+.*:\s*',
            r'^\s*elif\s+.*:\s*',
            r'^\s*else\s*:\s*',
            r'^\s*for\s+.*:\s*',
            r'^\s*while\s+.*:\s*',
            r'^\s*def\s+.*:\s*',
            r'^\s*class\s+.*:\s*',
            r'^\s*try\s*:\s*',
            r'^\s*except\s*.*:\s*',
            r'^\s*finally\s*:\s*',
            r'^\s*with\s+.*:\s*',
            r'^\s*match\s+.*:\s*',
            r'^\s*case\s+.*:\s*'
        ]

        # Check for indentation triggers based on language
        if self.language.lower() == 'html':
            for pattern in html_indent_triggers:
                if re.search(pattern, stripped_line):
                    return "    "

        elif self.language.lower() == 'css':
            for pattern in css_indent_triggers:
                if re.search(pattern, stripped_line):
                    return "    "

        elif self.language.lower() in ['javascript', 'js']:
            for pattern in js_indent_triggers:
                if re.search(pattern, stripped_line):
                    return "    "

        elif self.language.lower() == 'php':
            for pattern in php_indent_triggers:
                if re.search(pattern, stripped_line):
                    return "    "

        elif self.language.lower() == 'sql':
            for pattern in sql_indent_triggers:
                if re.search(pattern, stripped_line, re.IGNORECASE):
                    return "    "
        elif self.language.lower() == 'python':
            for pattern in python_indent_triggers:
                if re.search(pattern, stripped_line):
                    return "    "

        return ""

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

