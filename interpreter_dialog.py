import os
import subprocess

from PyQt6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QDialog, QLabel, QHBoxLayout, QLineEdit, QPushButton, QDialogButtonBox, QFileDialog, \
    QMessageBox


class InterpreterDialog(QDialog):
    def __init__(self, language, parent=None):
        super().__init__(parent)
        self.language = language
        self.interpreter_path = ""
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"Configure {self.language} Interpreter")
        self.setModal(True)
        self.resize(500, 200)

        layout = QVBoxLayout(self)

        label = QLabel(f"Select {self.language} interpreter:")
        layout.addWidget(label)

        # Path input
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_interpreter)

        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_button)
        layout.addLayout(path_layout)

        # Search in environment variables
        env_button = QPushButton("Search in Environment Variables")
        env_button.clicked.connect(self.search_in_env)
        layout.addWidget(env_button)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def browse_interpreter(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, f"Select {self.language} Interpreter",
            "", "Executable Files (*.exe);;All Files (*)"
        )
        if file_path:
            self.path_edit.setText(file_path)

    def search_in_env(self):
        commands = {
            'python': ['python', 'python3', 'py'],
            'php': ['php'],
            'sql': ['mysql', 'sqlite3', 'psql']
        }

        found_paths = []
        for cmd in commands.get(self.language.lower(), []):
            try:
                result = subprocess.run(['where', cmd] if os.name == 'nt' else ['which', cmd],
                                        capture_output=True, text=True, check=True)
                if result.stdout.strip():
                    found_paths.extend(result.stdout.strip().split('\n'))
            except subprocess.CalledProcessError:
                continue

        if found_paths:
            # Show selection dialog
            from PySide6.QtWidgets import QInputDialog
            path, ok = QInputDialog.getItem(
                self, "Found Interpreters", "Select interpreter:",
                found_paths, 0, False
            )
            if ok and path:
                self.path_edit.setText(path.strip())
        else:
            QMessageBox.information(
                self, "Not Found",
                f"No {self.language} interpreter found in environment variables."
            )

    def get_interpreter_path(self):
        return self.path_edit.text().strip()

