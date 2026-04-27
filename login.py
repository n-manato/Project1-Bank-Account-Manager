"""Login dialog for the Bank Account Manager."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from auth import authenticate_user, register_user


class LoginDialog(QDialog):
    """A login and registration dialog."""

    def __init__(self) -> None:
        """Initialize the login dialog."""
        super().__init__()
        self.logged_in_username: str = ""

        self.setWindowTitle("Login")
        self.setFixedSize(360, 220)

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the login interface."""
        main_layout = QVBoxLayout()

        title_label = QLabel("Bank Account Manager Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        form_layout = QGridLayout()

        username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addWidget(username_label, 0, 0)
        form_layout.addWidget(self.username_input, 0, 1)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        login_button = QPushButton("Login")
        register_button = QPushButton("Register")

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)

        form_layout.addWidget(login_button, 2, 0)
        form_layout.addWidget(register_button, 2, 1)

        self.status_label = QLabel("Create an account first, then log in.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def login(self) -> None:
        """Log in with the entered username and password."""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        success, message = authenticate_user(username, password)

        if success:
            self.logged_in_username = username
            self.accept()
        else:
            self.status_label.setText(message)
            QMessageBox.warning(self, "Login Failed", message)

    def register(self) -> None:
        """Register a new user with the entered username and password."""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        success, message = register_user(username, password)

        if success:
            self.status_label.setText("Registration successful. Please log in.")
            QMessageBox.information(self, "Register", message)
        else:
            self.status_label.setText(message)
            QMessageBox.warning(self, "Register Failed", message)
