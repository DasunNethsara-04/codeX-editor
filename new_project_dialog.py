import os

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, \
    QDialogButtonBox, QFileDialog, QMessageBox


class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Create New Project")
        self.setModal(True)
        self.resize(500, 300)

        layout = QVBoxLayout(self)

        # Project Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Project Name:"))
        self.project_name_edit = QLineEdit()
        self.project_name_edit.setPlaceholderText("Enter project name")
        name_layout.addWidget(self.project_name_edit)
        layout.addLayout(name_layout)

        # Project Path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Project Path:"))
        self.project_path_edit = QLineEdit()
        self.project_path_edit.setPlaceholderText("Select project location")
        self.browse_path_button = QPushButton("Browse...")
        self.browse_path_button.clicked.connect(self.browse_project_path)
        path_layout.addWidget(self.project_path_edit)
        path_layout.addWidget(self.browse_path_button)
        layout.addLayout(path_layout)

        # Project Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Project Type:"))
        self.project_type_combo = QComboBox()
        self.project_type_combo.addItems([
            "Python Application",
            "Web Application",
            "PHP Application",
            "Database"
        ])
        self.project_type_combo.currentTextChanged.connect(self.on_project_type_changed)
        type_layout.addWidget(self.project_type_combo)
        layout.addLayout(type_layout)

        # Description area
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: #888; padding: 10px; border: 1px solid #555; border-radius: 4px;")
        layout.addWidget(self.description_label)

        # Set initial description
        self.on_project_type_changed("Python Application")

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Connect project name change to update path
        self.project_name_edit.textChanged.connect(self.update_project_path)

    def browse_project_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Project Location")
        if folder_path:
            self.project_path_edit.setText(folder_path)

    def update_project_path(self, project_name):
        """Update project path when project name changes"""
        if project_name and self.project_path_edit.text():
            base_path = os.path.dirname(self.project_path_edit.text()) if os.path.dirname(
                self.project_path_edit.text()) else self.project_path_edit.text()
            new_path = os.path.join(base_path, project_name.replace(" ", "_").lower())
            self.project_path_edit.setText(new_path)

    def on_project_type_changed(self, project_type):
        """Update description based on selected project type"""
        descriptions = {
            "Python Application": "Creates a Python project with main.py file and basic project structure. Ideal for desktop applications, scripts, and general Python development.",
            "Web Application": "Creates a web development project with HTML, CSS, and JavaScript files. Includes basic file structure for modern web development.",
            "PHP Application": "Creates a web application project with PHP, CSS and JavaScript files. Includes basic file structure for simple web application development",
            "Database": "Creates a database project with SQL files and database connection configurations. Perfect for database design and management tasks."
        }
        self.description_label.setText(descriptions.get(project_type, ""))

    def get_project_data(self):
        return {
            'name': self.project_name_edit.text().strip(),
            'path': self.project_path_edit.text().strip(),
            'type': self.project_type_combo.currentText()
        }

    def accept(self):
        # Validate inputs
        project_data = self.get_project_data()

        if not project_data['name']:
            QMessageBox.warning(self, "Validation Error", "Project name is required.")
            return

        if not project_data['path']:
            QMessageBox.warning(self, "Validation Error", "Project path is required.")
            return

        # Check if project directory already exists
        if os.path.exists(project_data['path']):
            reply = QMessageBox.question(self, "Directory Exists",
                                         f"Directory '{project_data['path']}' already exists. Continue anyway?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return

        super().accept()

