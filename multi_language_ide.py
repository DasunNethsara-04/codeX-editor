import json
import os
import subprocess
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import QDialog, QMessageBox, QFileDialog, QDialogButtonBox, QPushButton, QLineEdit, QHBoxLayout, \
    QLabel, QVBoxLayout, QWidget, QTabWidget, QTreeWidgetItem, QMainWindow, QSplitter, QTreeWidget, QStatusBar

from code_editor_with_line_numbers import CodeEditorWithLineNumbers
from interpreter_dialog import InterpreterDialog
from new_project_dialog import NewProjectDialog
from output import OutputWidget
from sql_connection_dialog import SQLConnectionDialog


class MultiLanguageIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_project_path = None
        self.open_files = {}  # filename -> editor widget
        self.interpreters = {}  # language -> interpreter path
        self.sql_connection_params = None  # Add this line
        self.setup_ui()
        self.setup_menu()
        self.load_settings()

    def setup_ui(self):
        self.setWindowTitle("CodeX Text Editor")
        self.setGeometry(100, 100, 1200, 800)
        icon = QIcon("./logo.ico")
        self.setWindowIcon(icon)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Main splitter for horizontal split
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # Left side - vertical splitter for editor and output
        self.left_splitter = QSplitter(Qt.Vertical)

        # Editor area (top of left side)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.left_splitter.addWidget(self.tab_widget)

        # Output area (bottom of left side)
        self.output_widget = OutputWidget()
        self.left_splitter.addWidget(self.output_widget)

        # Set initial sizes for left splitter (70% editor, 30% output)
        self.left_splitter.setSizes([560, 240])

        # Add left splitter to main splitter
        self.main_splitter.addWidget(self.left_splitter)

        # Project tree (right side)
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("Project Explorer")
        self.project_tree.itemDoubleClicked.connect(self.open_file_from_tree)
        self.main_splitter.addWidget(self.project_tree)

        # Set initial sizes for main splitter (80% left side, 20% tree)
        self.main_splitter.setSizes([800, 200])

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def setup_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_file_action = QAction("New File", self)
        new_file_action.setShortcut(QKeySequence.New)
        new_file_action.triggered.connect(self.new_file)
        file_menu.addAction(new_file_action)

        open_file_action = QAction("Open File", self)
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        file_menu.addSeparator()

        new_project_action = QAction("New Project...", self)
        new_project_action.setShortcut("Ctrl+Shift+N")
        new_project_action.triggered.connect(self.create_new_project)
        file_menu.addAction(new_project_action)

        open_folder_action = QAction("Open Folder as Project", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

        file_menu.addSeparator()

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        toggle_tree_action = QAction("Toggle Project Tree", self)
        toggle_tree_action.setShortcut("Ctrl+Shift+E")
        toggle_tree_action.triggered.connect(self.toggle_project_tree)
        view_menu.addAction(toggle_tree_action)

        toggle_output_action = QAction("Toggle Output Panel", self)
        toggle_output_action.setShortcut("Ctrl+Shift+O")
        toggle_output_action.triggered.connect(self.toggle_output_panel)
        view_menu.addAction(toggle_output_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in_current_editor)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out_current_editor)
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.reset_zoom_current_editor)
        view_menu.addAction(reset_zoom_action)

        # Run menu
        run_menu = menubar.addMenu("Run")

        run_action = QAction("Run Current File", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current_file)
        run_menu.addAction(run_action)

        configure_interpreters_action = QAction("Configure Interpreters", self)
        configure_interpreters_action.triggered.connect(self.configure_interpreters)
        run_menu.addAction(configure_interpreters_action)

        sql_connection_action = QAction("Configure SQL Connection", self)
        sql_connection_action.triggered.connect(self.configure_sql_connection)
        run_menu.addAction(sql_connection_action)

        run_menu.addSeparator()

        edit_sql_connection_action = QAction("Edit SQL Connection", self)
        edit_sql_connection_action.triggered.connect(self.configure_sql_connection)
        run_menu.addAction(edit_sql_connection_action)

    def configure_sql_connection(self):
        """Configure SQL connection settings"""
        connection_dialog = SQLConnectionDialog(self)

        # Pre-populate with existing settings if available
        if hasattr(self, 'sql_connection_params') and self.sql_connection_params:
            params = self.sql_connection_params
            connection_dialog.db_type.setCurrentText(params.get('type', 'MySQL'))
            connection_dialog.host_edit.setText(params.get('host', 'localhost'))
            connection_dialog.port_edit.setText(params.get('port', '3306'))
            connection_dialog.database_edit.setText(params.get('database', ''))
            connection_dialog.username_edit.setText(params.get('username', 'root'))
            connection_dialog.password_edit.setText(params.get('password', ''))
            connection_dialog.sqlite_file_edit.setText(params.get('sqlite_file', ''))
            # Trigger UI update for the selected database type
            connection_dialog.update_ui_for_db_type(params.get('type', 'MySQL'))

        if connection_dialog.exec() == QDialog.Accepted:
            self.sql_connection_params = connection_dialog.get_connection_params()
            self.save_settings()  # Save immediately when connection is configured
            self.status_bar.showMessage("SQL connection settings updated", 2000)

    def create_new_project(self):
        """Create a new project with specified structure"""
        dialog = NewProjectDialog(self)

        if dialog.exec() == QDialog.Accepted:
            project_data = dialog.get_project_data()

            try:
                # Create project directory
                os.makedirs(project_data['path'], exist_ok=True)

                # Create project structure based on type
                if project_data['type'] == "Python Application":
                    self.create_python_project(project_data)
                elif project_data['type'] == "Web Application":
                    self.create_web_project(project_data)
                elif project_data['type'] == "PHP Application":
                    self.create_php_project(project_data)
                elif project_data['type'] == "Database":
                    self.create_database_project(project_data)

                # Set as current project and populate tree
                self.current_project_path = project_data['path']
                self.populate_project_tree(project_data['path'])

                self.status_bar.showMessage(f"Project '{project_data['name']}' created successfully!", 3000)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create project: {str(e)}")

    def create_python_project(self, project_data):
        """Create Python project structure"""
        project_path = project_data['path']

        # Create main.py
        main_py_content = f'''#!/usr/bin/env python3
"""
{project_data['name']} - Main Application File
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def main():
    print("Hello, {project_data['name']}!")
    print("Welcome to your new Python application!")

if __name__ == "__main__":
    main()
    '''

        with open(os.path.join(project_path, "main.py"), 'w') as f:
            f.write(main_py_content)

        # Create README.md
        readme_content = f'''# {project_data['name']}

A Python application created with CodeX Text Editor.

## Getting Started

Run the application:
```bash
python main.py
```

## Project Structure

- `main.py` - Main application file
- `README.md` - This file
    '''

        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(readme_content)

    def create_php_project(self, project_data):
        """Create a simple web application project using PHP"""
        project_path = project_data['path']
        os.makedirs(os.path.join(project_path, "config"), exist_ok=True)

        db_file_content = '''// TODO: Implement the Database connection logic here.'''
        with open(os.path.join(project_path, "config", "db.php"), 'w') as f:
            f.write(db_file_content)

        self.create_web_project(project_data)

    def create_web_project(self, project_data):
        """Create Web project structure"""
        project_path = project_data['path']

        # Create directories
        os.makedirs(os.path.join(project_path, "css"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "js"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "images"), exist_ok=True)

        # Create index.html
        html_content = f'''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{project_data['name']}</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <header>
            <h1>Welcome to {project_data['name']}</h1>
        </header>

        <main>
            <p>Your web application is ready to go!</p>
            <button id="demo-button">Click Me</button>
        </main>

        <footer>
            <p>Created with CodeX Text Editor</p>
        </footer>

        <script src="js/script.js"></script>
    </body>
</html>
    '''

        with open(os.path.join(project_path, "index.html"), 'w') as f:
            f.write(html_content)

        # Create style.css
        css_content = '''/* CSS for {project_name} */
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}}

header {{
    background-color: #333;
    color: white;
    text-align: center;
    padding: 1rem;
}}

main {{
    max-width: 1200px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

button {{
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}}

button:hover {{
    background-color: #0056b3;
}}

footer {{
    text-align: center;
    padding: 1rem;
    color: #666;
}}
    '''.format(project_name=project_data['name'])

        with open(os.path.join(project_path, "css", "style.css"), 'w') as f:
            f.write(css_content)

        # Create script.js
        js_content = '''// JavaScript for {project_name}
document.addEventListener('DOMContentLoaded', function() {{
    const button = document.getElementById('demo-button');

    button.addEventListener('click', function() {{
        alert('Hello from {project_name}!');
    }});
}});
    '''.format(project_name=project_data['name'])

        with open(os.path.join(project_path, "js", "script.js"), 'w') as f:
            f.write(js_content)

    def create_database_project(self, project_data):
        """Create Database project structure"""
        project_path = project_data['path']

        # Create directories
        os.makedirs(os.path.join(project_path, "schemas"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "queries"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "migrations"), exist_ok=True)

        # Create initial schema file
        schema_content = f'''-- Database Schema for {project_data['name']}
-- Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

-- Example table structure
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Add indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
    '''

        with open(os.path.join(project_path, "schemas", "schema.sql"), 'w') as f:
            f.write(schema_content)

        # Create sample queries
        queries_content = f'''-- Sample Queries for {project_data['name']}

    -- Select all users
SELECT * FROM users;

-- Insert a new user
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com');

-- Update user email
UPDATE users 
SET email = 'newemail@example.com' 
WHERE username = 'john_doe';

-- Delete a user
DELETE FROM users 
WHERE username = 'john_doe';
    '''

        with open(os.path.join(project_path, "queries", "sample_queries.sql"), 'w') as f:
            f.write(queries_content)

    def new_file(self):
        editor_widget = CodeEditorWithLineNumbers()
        tab_index = self.tab_widget.addTab(editor_widget, "Untitled")
        self.tab_widget.setCurrentIndex(tab_index)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "All Files (*);;Python Files (*.py);;JavaScript Files (*.js);;HTML Files (*.html);;CSS Files (*.css);;PHP Files (*.php);;SQL Files (*.sql)"
        )
        if file_path:
            self.load_file(file_path)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder as Project")
        if folder_path:
            self.current_project_path = folder_path
            self.populate_project_tree(folder_path)

    def populate_project_tree(self, root_path):
        self.project_tree.clear()
        root_item = QTreeWidgetItem(self.project_tree)
        root_item.setText(0, os.path.basename(root_path))
        root_item.setData(0, Qt.UserRole, root_path)

        self.add_tree_items(root_item, root_path)
        self.project_tree.expandAll()

    def add_tree_items(self, parent_item, path, depth=0, max_depth=3):
        try:
            if depth > max_depth:
                return

            items = os.listdir(path)
            # Skip hidden files and common ignore patterns
            filtered_items = [item for item in items
                              if not item.startswith('.')
                              and item not in ['__pycache__', 'node_modules', '.git']]

            for item in sorted(filtered_items):
                item_path = os.path.join(path, item)
                tree_item = QTreeWidgetItem(parent_item)
                tree_item.setText(0, item)
                tree_item.setData(0, Qt.UserRole, item_path)

                if os.path.isdir(item_path):
                    self.add_tree_items(tree_item, item_path, depth + 1, max_depth)
        except (PermissionError, OSError):
            pass

    def open_file_from_tree(self, item):
        file_path = item.data(0, Qt.UserRole)
        if os.path.isfile(file_path):
            self.load_file(file_path)

    def load_file(self, file_path):
        # Check if file is already open
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if hasattr(widget, 'file_path') and widget.file_path == file_path:
                self.tab_widget.setCurrentIndex(i)
                return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            editor_widget = CodeEditorWithLineNumbers()
            editor_widget.file_path = file_path
            editor_widget.editor.setPlainText(content)

            # Set language based on file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            language_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.html': 'html',
                '.css': 'css',
                '.php': 'php',
                '.sql': 'sql'
            }

            if file_ext in language_map:
                editor_widget.editor.set_language(language_map[file_ext])

            tab_index = self.tab_widget.addTab(editor_widget, os.path.basename(file_path))
            self.tab_widget.setCurrentIndex(tab_index)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
            import traceback
            traceback.print_exc()  # For debugging

    def save_file(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            if hasattr(current_widget, 'file_path'):
                self.save_to_file(current_widget.file_path, current_widget.editor.toPlainText())
            else:
                self.save_file_as()

    def save_file_as(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File As", "",
                "All Files (*);;Python Files (*.py);;JavaScript Files (*.js);;HTML Files (*.html);;CSS Files (*.css);;PHP Files (*.php);;SQL Files (*.sql)"
            )
            if file_path:
                self.save_to_file(file_path, current_widget.editor.toPlainText())
                current_widget.file_path = file_path
                current_index = self.tab_widget.currentIndex()
                self.tab_widget.setTabText(current_index, os.path.basename(file_path))

    def save_to_file(self, file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            self.status_bar.showMessage(f"Saved: {file_path}", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        widget.deleteLater()

    def toggle_project_tree(self):
        self.project_tree.setVisible(not self.project_tree.isVisible())

    def run_current_file(self):
        current_widget = self.tab_widget.currentWidget()
        if not current_widget or not hasattr(current_widget, 'file_path'):
            QMessageBox.warning(self, "Warning", "No file is currently open or saved.")
            return

        file_path = current_widget.file_path
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == '.py':
            self.run_python_file(file_path)
        elif file_ext == '.php':
            self.run_php_file(file_path)
        elif file_ext == '.sql':
            self.run_sql_file(file_path)
        elif file_ext in ['.html', '.js', '.css']:
            # For web files, just show in status bar
            self.status_bar.showMessage("Web files can be opened in a browser", 3000)
        else:
            QMessageBox.information(self, "Info", "File type not supported for execution.")

    def run_python_file(self, file_path):
        if 'python' not in self.interpreters:
            dialog = InterpreterDialog('Python', self)
            if dialog.exec() == QDialog.Accepted:
                self.interpreters['python'] = dialog.get_interpreter_path()
            else:
                return

        interpreter = self.interpreters['python']
        if interpreter:
            self.execute_file(interpreter, file_path, "Python")

    def run_php_file(self, file_path):
        if 'php' not in self.interpreters:
            dialog = InterpreterDialog('PHP', self)
            if dialog.exec() == QDialog.Accepted:
                self.interpreters['php'] = dialog.get_interpreter_path()
            else:
                return

        interpreter = self.interpreters['php']
        if interpreter:
            self.execute_file(interpreter, file_path, "PHP")

    # Replace the existing run_sql_file method (around line 570):
    def run_sql_file(self, file_path):
        if 'sql' not in self.interpreters:
            dialog = InterpreterDialog('SQL', self)
            if dialog.exec() == QDialog.Accepted:
                self.interpreters['sql'] = dialog.get_interpreter_path()
                self.save_settings()  # Save interpreter settings
            else:
                return

        # Check if SQL connection settings exist
        if not hasattr(self, 'sql_connection_params') or not self.sql_connection_params:
            # Show SQL connection dialog only if no settings exist
            connection_dialog = SQLConnectionDialog(self)
            if connection_dialog.exec() == QDialog.Accepted:
                self.sql_connection_params = connection_dialog.get_connection_params()
                self.save_settings()  # Save connection settings
            else:
                return

        interpreter = self.interpreters['sql']
        if interpreter and self.sql_connection_params:
            self.execute_sql_file(interpreter, file_path, self.sql_connection_params)

    def execute_sql_file(self, interpreter, file_path, connection_params):
        """Execute a SQL file with connection parameters"""
        try:
            self.output_widget.clear_output()
            self.output_widget.set_title(f"SQL Output - {os.path.basename(file_path)}")
            self.output_widget.append_output(f"Running {file_path}...")
            self.output_widget.append_output(f"Database: {connection_params['type']}")
            if connection_params['type'] != 'SQLite':
                self.output_widget.append_output(f"Host: {connection_params['host']}:{connection_params['port']}")
                self.output_widget.append_output(f"User: {connection_params['username']}")
            self.output_widget.append_output("-" * 50)

            # Build command based on database type
            cmd = []

            if connection_params['type'] == 'MySQL':
                cmd = [interpreter]
                if connection_params['host']:
                    cmd.extend(['-h', connection_params['host']])
                if connection_params['port']:
                    cmd.extend(['-P', connection_params['port']])
                if connection_params['username']:
                    cmd.extend(['-u', connection_params['username']])
                if connection_params['password']:
                    cmd.extend([f'-p{connection_params["password"]}'])
                if connection_params['database']:
                    cmd.append(connection_params['database'])

                # Read the SQL file content and pass it as input
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sql_content = f.read()

                    process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        cwd=os.path.dirname(file_path) if os.path.dirname(file_path) else None
                    )

                    stdout, stderr = process.communicate(input=sql_content)
                except Exception as e:
                    self.output_widget.append_output(f"Error reading SQL file: {str(e)}")
                    return

            elif connection_params['type'] == 'SQLite':
                sqlite_file = connection_params['sqlite_file'] or ':memory:'
                cmd = [interpreter, sqlite_file, f'.read {file_path}']

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.path.dirname(file_path) if os.path.dirname(file_path) else None
                )
                stdout, stderr = process.communicate()

            elif connection_params['type'] == 'PostgreSQL':
                cmd = [interpreter]
                if connection_params['host']:
                    cmd.extend(['-h', connection_params['host']])
                if connection_params['port']:
                    cmd.extend(['-p', connection_params['port']])
                if connection_params['username']:
                    cmd.extend(['-U', connection_params['username']])
                if connection_params['database']:
                    cmd.extend(['-d', connection_params['database']])
                cmd.extend(['-f', file_path])

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.path.dirname(file_path) if os.path.dirname(file_path) else None
                )
                stdout, stderr = process.communicate()

            if stdout:
                self.output_widget.append_output("STDOUT:")
                self.output_widget.append_output(stdout)

            if stderr:
                self.output_widget.append_output("STDERR:")
                self.output_widget.append_output(stderr)

            return_code = process.returncode
            self.output_widget.append_output("-" * 50)
            self.output_widget.append_output(f"Process finished with return code: {return_code}")

            if return_code == 0:
                self.status_bar.showMessage(f"SQL execution completed successfully", 3000)
            else:
                self.status_bar.showMessage(f"SQL execution finished with errors (code: {return_code})", 5000)

        except Exception as e:
            self.output_widget.append_output(f"Error executing SQL file: {str(e)}")
            self.status_bar.showMessage(f"SQL execution failed: {str(e)}", 5000)

    def execute_file(self, interpreter, file_path, language):
        """Execute a file and capture output"""
        try:
            self.output_widget.clear_output()
            self.output_widget.set_title(f"{language} Output - {os.path.basename(file_path)}")
            self.output_widget.append_output(f"Running {file_path}...")
            self.output_widget.append_output("-" * 50)

            # Execute the file and capture output
            process = subprocess.Popen(
                [interpreter, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(file_path) if os.path.dirname(file_path) else None
            )

            stdout, stderr = process.communicate()

            if stdout:
                self.output_widget.append_output("STDOUT:")
                self.output_widget.append_output(stdout)

            if stderr:
                self.output_widget.append_output("STDERR:")
                self.output_widget.append_output(stderr)

            return_code = process.returncode
            self.output_widget.append_output("-" * 50)
            self.output_widget.append_output(f"Process finished with return code: {return_code}")

            if return_code == 0:
                self.status_bar.showMessage(f"Execution completed successfully", 3000)
            else:
                self.status_bar.showMessage(f"Execution finished with errors (code: {return_code})", 5000)

        except Exception as e:
            self.output_widget.append_output(f"Error executing file: {str(e)}")
            self.status_bar.showMessage(f"Execution failed: {str(e)}", 5000)

    def toggle_output_panel(self):
        """Toggle the visibility of the output panel"""
        self.output_widget.setVisible(not self.output_widget.isVisible())

    def zoom_in_current_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'editor'):
            current_widget.editor.zoom_in()

    def zoom_out_current_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'editor'):
            current_widget.editor.zoom_out()

    def reset_zoom_current_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'editor'):
            font = current_widget.editor.font()
            font.setPointSize(12)  # Reset to default size
            current_widget.editor.setFont(font)

    def configure_interpreters(self):
        languages = ['Python', 'PHP', 'SQL']

        class InterpreterConfigDialog(QDialog):
            def __init__(self, interpreters, parent=None):
                super().__init__(parent)
                self.interpreters = interpreters
                self.setup_ui()

            def setup_ui(self):
                self.setWindowTitle("Configure Interpreters")
                self.setModal(True)
                self.resize(600, 400)

                layout = QVBoxLayout(self)

                # Create tabs for each language
                tab_widget = QTabWidget()
                self.interpreter_widgets = {}

                for lang in ['python', 'php', 'sql']:
                    tab = QWidget()
                    tab_layout = QVBoxLayout(tab)

                    label = QLabel(f"Select {lang.title()} interpreter:")
                    tab_layout.addWidget(label)

                    # Path input
                    path_layout = QHBoxLayout()
                    path_edit = QLineEdit()
                    if lang in self.interpreters:
                        path_edit.setText(self.interpreters[lang])

                    browse_button = QPushButton("Browse...")
                    browse_button.clicked.connect(lambda checked, l=lang, e=path_edit: self.browse_interpreter(l, e))

                    env_button = QPushButton("Search in Environment")
                    env_button.clicked.connect(lambda checked, l=lang, e=path_edit: self.search_in_env(l, e))

                    path_layout.addWidget(path_edit)
                    path_layout.addWidget(browse_button)
                    path_layout.addWidget(env_button)

                    tab_layout.addLayout(path_layout)
                    tab_layout.addStretch()

                    self.interpreter_widgets[lang] = path_edit
                    tab_widget.addTab(tab, lang.title())

                layout.addWidget(tab_widget)

                # Dialog buttons
                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(self.accept)
                button_box.rejected.connect(self.reject)
                layout.addWidget(button_box)

            def browse_interpreter(self, language, path_edit):
                file_path, _ = QFileDialog.getOpenFileName(
                    self, f"Select {language.title()} Interpreter",
                    "", "Executable Files (*.exe);;All Files (*)"
                )
                if file_path:
                    path_edit.setText(file_path)

            def search_in_env(self, language, path_edit):
                commands = {
                    'python': ['python', 'python3', 'py'],
                    'php': ['php'],
                    'sql': ['mysql', 'sqlite3', 'psql']
                }

                found_paths = []
                for cmd in commands.get(language.lower(), []):
                    try:
                        result = subprocess.run(['where', cmd] if os.name == 'nt' else ['which', cmd],
                                                capture_output=True, text=True, check=True)
                        if result.stdout.strip():
                            found_paths.extend(result.stdout.strip().split('\n'))
                    except subprocess.CalledProcessError:
                        continue

                if found_paths:
                    from PySide6.QtWidgets import QInputDialog
                    path, ok = QInputDialog.getItem(
                        self, "Found Interpreters", "Select interpreter:",
                        found_paths, 0, False
                    )
                    if ok and path:
                        path_edit.setText(path.strip())
                else:
                    QMessageBox.information(
                        self, "Not Found",
                        f"No {language} interpreter found in environment variables."
                    )

            def get_interpreters(self):
                result = {}
                for lang, widget in self.interpreter_widgets.items():
                    path = widget.text().strip()
                    if path:
                        result[lang] = path
                return result

        dialog = InterpreterConfigDialog(self.interpreters, self)
        if dialog.exec() == QDialog.Accepted:
            self.interpreters.update(dialog.get_interpreters())
            self.save_settings()

    def load_settings(self):
        """Load interpreter and SQL connection settings from a config file"""
        config_file = os.path.join(os.path.expanduser("~"), ".multilang_ide_config.json")
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.interpreters = config.get('interpreters', {})
                    self.sql_connection_params = config.get('sql_connection_params', None)
        except Exception:
            pass

    def save_settings(self):
        """Save interpreter and SQL connection settings to a config file"""
        config_file = os.path.join(os.path.expanduser("~"), ".multilang_ide_config.json")
        try:
            config = {
                'interpreters': self.interpreters,
                'sql_connection_params': getattr(self, 'sql_connection_params', None)
            }
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass

    def closeEvent(self, event):
        """Save settings when closing the application"""
        self.save_settings()
        event.accept()
