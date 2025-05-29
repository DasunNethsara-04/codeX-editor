import sys
from PySide6.QtWidgets import (
    QApplication
)
from PySide6.QtGui import (QColor)

from multi_language_ide import MultiLanguageIDE


def main():
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Dark theme
    from PySide6.QtGui import QPalette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

    # Create and show the IDE
    ide = MultiLanguageIDE()
    ide.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
