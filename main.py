"""Application entry point for the Bank Account Manager."""

import sys

from PyQt6.QtWidgets import QApplication, QDialog

from gui import BankApp
from login import LoginDialog


def main() -> None:
    """Start the PyQt6 application after login."""
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    login_result = login_dialog.exec()

    if login_result == QDialog.DialogCode.Accepted:
        window = BankApp(login_dialog.logged_in_username)
        window.show()
        sys.exit(app.exec())

    sys.exit(0)


if __name__ == "__main__":
    main()
