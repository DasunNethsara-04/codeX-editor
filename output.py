from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit


class OutputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Title bar
        title_layout = QHBoxLayout()
        self.title_label = QLabel("Output")
        self.title_label.setStyleSheet("font-weight: bold; padding: 5px;")
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        self.clear_button.setMaximumWidth(60)

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.clear_button)

        layout.addLayout(title_layout)

        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        self.output_text.setStyleSheet("background-color: #1a1a1a; color: #ffffff; border: 1px solid #555;")

        layout.addWidget(self.output_text)

    def append_output(self, text):
        self.output_text.append(text)
        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output_text.setTextCursor(cursor)

    def clear_output(self):
        self.output_text.clear()

    def set_title(self, title):
        self.title_label.setText(title)

