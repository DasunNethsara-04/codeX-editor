import mysql.connector
import sqlite3
import psycopg2
from PySide6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, \
    QDialogButtonBox, QFileDialog


class SQLConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("SQL Connection Settings")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # Database type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Database Type:"))
        self.db_type = QComboBox()
        self.db_type.addItems(["MySQL", "SQLite", "PostgreSQL"])
        type_layout.addWidget(self.db_type)
        layout.addLayout(type_layout)

        # Host
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_edit = QLineEdit("localhost")
        host_layout.addWidget(self.host_edit)
        layout.addLayout(host_layout)

        # Port
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_edit = QLineEdit("3306")
        port_layout.addWidget(self.port_edit)
        layout.addLayout(port_layout)

        # Database name
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("Database:"))
        self.database_edit = QLineEdit()
        db_layout.addWidget(self.database_edit)
        layout.addLayout(db_layout)

        # Username
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Username:"))
        self.username_edit = QLineEdit("root")
        user_layout.addWidget(self.username_edit)
        layout.addLayout(user_layout)

        # Password
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("Password:"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.password_edit)
        layout.addLayout(pass_layout)

        # SQLite file path (only for SQLite)
        self.sqlite_layout = QHBoxLayout()
        self.sqlite_layout.addWidget(QLabel("SQLite File:"))
        self.sqlite_file_edit = QLineEdit()
        self.sqlite_browse_button = QPushButton("Browse...")
        self.sqlite_browse_button.clicked.connect(self.browse_sqlite_file)
        self.sqlite_layout.addWidget(self.sqlite_file_edit)
        self.sqlite_layout.addWidget(self.sqlite_browse_button)
        layout.addLayout(self.sqlite_layout)

        # Connect database type change to update UI
        self.db_type.currentTextChanged.connect(self.update_ui_for_db_type)
        self.update_ui_for_db_type("MySQL")  # Initial setup

        # Test connection button
        test_button = QPushButton("Test Connection")
        test_button.clicked.connect(self.test_connection)
        layout.addWidget(test_button)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def update_ui_for_db_type(self, db_type):
        is_sqlite = db_type == "SQLite"

        # Show/hide fields based on database type
        self.host_edit.setVisible(not is_sqlite)
        self.port_edit.setVisible(not is_sqlite)
        self.username_edit.setVisible(not is_sqlite)
        self.password_edit.setVisible(not is_sqlite)

        # Show/hide SQLite specific fields
        for i in range(self.sqlite_layout.count()):
            widget = self.sqlite_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_sqlite)

        # Update default port based on database type
        if db_type == "MySQL":
            self.port_edit.setText("3306")
        elif db_type == "PostgreSQL":
            self.port_edit.setText("5432")

    def browse_sqlite_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select SQLite Database File",
            "", "SQLite Files (*.db *.sqlite *.sqlite3);;All Files (*)"
        )
        if file_path:
            self.sqlite_file_edit.setText(file_path)

    def test_connection(self):
        """Test the database connection with actual connection attempt"""
        params = self.get_connection_params()

        try:
            if params['type'] == 'MySQL':
                if not params['host'] or not params['username']:
                    QMessageBox.warning(self, "Missing Parameters",
                                        "Host and Username are required for MySQL connection.")
                    return

                connection = mysql.connector.connect(
                    host=params['host'],
                    port=int(params['port']) if params['port'] else 3306,
                    user=params['username'],
                    password=params['password'],
                    database=params['database'] if params['database'] else None
                )
                connection.close()
                QMessageBox.information(self, "Connection Test",
                                        "✅ Successfully connected to MySQL database!")

            elif params['type'] == 'SQLite':
                if not params['sqlite_file']:
                    QMessageBox.warning(self, "Missing Parameters",
                                        "SQLite file path is required.")
                    return

                connection = sqlite3.connect(params['sqlite_file'])
                connection.close()
                QMessageBox.information(self, "Connection Test",
                                        "✅ Successfully connected to SQLite database!")

            elif params['type'] == 'PostgreSQL':
                if not params['host'] or not params['username']:
                    QMessageBox.warning(self, "Missing Parameters",
                                        "Host and Username are required for PostgreSQL connection.")
                    return

                connection = psycopg2.connect(
                    host=params['host'],
                    port=int(params['port']) if params['port'] else 5432,
                    user=params['username'],
                    password=params['password'],
                    database=params['database'] if params['database'] else 'postgres'
                )
                connection.close()
                QMessageBox.information(self, "Connection Test",
                                        "✅ Successfully connected to PostgreSQL database!")

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "MySQL Connection Failed",
                                 f"❌ Could not connect to MySQL database:\n{str(e)}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "SQLite Connection Failed",
                                 f"❌ Could not connect to SQLite database:\n{str(e)}")
        except psycopg2.Error as e:
            QMessageBox.critical(self, "PostgreSQL Connection Failed",
                                 f"❌ Could not connect to PostgreSQL database:\n{str(e)}")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Parameters",
                                f"Invalid port number: {params['port']}")
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed",
                                 f"❌ Unexpected error:\n{str(e)}")

    def get_connection_params(self):
        return {
            'type': self.db_type.currentText(),
            'host': self.host_edit.text(),
            'port': self.port_edit.text(),
            'database': self.database_edit.text(),
            'username': self.username_edit.text(),
            'password': self.password_edit.text(),
            'sqlite_file': self.sqlite_file_edit.text()
        }

