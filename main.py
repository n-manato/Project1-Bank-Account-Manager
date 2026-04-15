"""Application entry point for the Bank Account Manager."""

import sys

from PyQt6.QtWidgets import QApplication

from gui import BankApp


def main() -> None:
    """Start the PyQt6 application."""
    app = QApplication(sys.argv)
    window = BankApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()