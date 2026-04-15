"""PyQt6 GUI for the Bank Account Manager."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from bank import Bank
from storage import load_accounts, load_transactions, save_accounts, save_transactions


class BankApp(QMainWindow):
    """Main GUI window for the Bank Account Manager."""

    def __init__(self) -> None:
        """Initialize the main window and all UI components."""
        super().__init__()
        self.bank: Bank = Bank()
        self.selected_account_name: str = ""

        self.setWindowTitle("Bank Account Manager")
        self.resize(1100, 700)

        self._build_ui()
        self.refresh_ui()

    def _build_ui(self) -> None:
        """Build the full user interface."""
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        title_label = QLabel("Bank Account Manager")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.selected_label = QLabel("Selected Account: None")
        self.selected_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.total_label = QLabel("Total Balance: $0.00")
        self.total_label.setStyleSheet("font-size: 14px;")

        header_layout = QVBoxLayout()
        header_layout.addWidget(title_label)
        header_layout.addWidget(self.selected_label)
        header_layout.addWidget(self.total_label)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self._create_left_panel(), 1)
        content_layout.addWidget(self._create_right_panel(), 2)

        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet(
            "padding: 8px; border: 1px solid gray; font-weight: bold;"
        )

        main_layout.addLayout(header_layout)
        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.status_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _create_left_panel(self) -> QWidget:
        """
        Create the left control panel.

        Returns:
            The left panel widget.
        """
        panel = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self._create_account_group())
        layout.addWidget(self._create_transaction_group())
        layout.addWidget(self._create_transfer_group())
        layout.addWidget(self._create_file_group())
        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def _create_right_panel(self) -> QWidget:
        """
        Create the right display panel.

        Returns:
            The right panel widget.
        """
        panel = QWidget()
        layout = QVBoxLayout()

        accounts_title = QLabel("Accounts")
        accounts_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.accounts_table = QTableWidget()
        self.accounts_table.setColumnCount(3)
        self.accounts_table.setHorizontalHeaderLabels(["Name", "Type", "Balance"])
        self.accounts_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.accounts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.accounts_table.cellClicked.connect(self.select_account_from_table)

        history_title = QLabel("Transaction History")
        history_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(
            ["Date/Time", "Action", "Account", "Details", "Amount", "Result"]
        )
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(accounts_title)
        layout.addWidget(self.accounts_table)
        layout.addWidget(history_title)
        layout.addWidget(self.history_table)

        panel.setLayout(layout)
        return panel

    def _create_account_group(self) -> QGroupBox:
        """
        Create the account creation group.

        Returns:
            The account creation group box.
        """
        group = QGroupBox("Create Account")
        layout = QGridLayout()

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        type_label = QLabel("Type:")
        self.account_type_combo = QComboBox()
        self.account_type_combo.addItems(["Account", "SavingAccount", "CheckingAccount"])

        create_button = QPushButton("Create Account")
        create_button.clicked.connect(self.create_account)

        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_input, 0, 1)
        layout.addWidget(type_label, 1, 0)
        layout.addWidget(self.account_type_combo, 1, 1)
        layout.addWidget(create_button, 2, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _create_transaction_group(self) -> QGroupBox:
        """
        Create the deposit and withdrawal group.

        Returns:
            The transaction group box.
        """
        group = QGroupBox("Transactions")
        layout = QGridLayout()

        amount_label = QLabel("Amount:")
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.0, 1_000_000.0)
        self.amount_input.setDecimals(2)
        self.amount_input.setSingleStep(1.0)

        deposit_button = QPushButton("Deposit")
        withdraw_button = QPushButton("Withdraw")

        deposit_button.clicked.connect(self.deposit_money)
        withdraw_button.clicked.connect(self.withdraw_money)

        layout.addWidget(amount_label, 0, 0)
        layout.addWidget(self.amount_input, 0, 1)
        layout.addWidget(deposit_button, 1, 0)
        layout.addWidget(withdraw_button, 1, 1)

        group.setLayout(layout)
        return group

    def _create_transfer_group(self) -> QGroupBox:
        """
        Create the transfer group.

        Returns:
            The transfer group box.
        """
        group = QGroupBox("Transfer")
        layout = QGridLayout()

        target_label = QLabel("Transfer To:")
        self.transfer_to_combo = QComboBox()

        transfer_amount_label = QLabel("Amount:")
        self.transfer_amount_input = QDoubleSpinBox()
        self.transfer_amount_input.setRange(0.0, 1_000_000.0)
        self.transfer_amount_input.setDecimals(2)
        self.transfer_amount_input.setSingleStep(1.0)

        transfer_button = QPushButton("Transfer")
        transfer_button.clicked.connect(self.transfer_money)

        layout.addWidget(target_label, 0, 0)
        layout.addWidget(self.transfer_to_combo, 0, 1)
        layout.addWidget(transfer_amount_label, 1, 0)
        layout.addWidget(self.transfer_amount_input, 1, 1)
        layout.addWidget(transfer_button, 2, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _create_file_group(self) -> QGroupBox:
        """
        Create the file controls group.

        Returns:
            The file group box.
        """
        group = QGroupBox("File")
        layout = QVBoxLayout()

        save_button = QPushButton("Save CSV")
        load_button = QPushButton("Load CSV")

        save_button.clicked.connect(self.save_data)
        load_button.clicked.connect(self.load_data)

        layout.addWidget(save_button)
        layout.addWidget(load_button)

        group.setLayout(layout)
        return group

    def create_account(self) -> None:
        """Create a new account from the input fields."""
        name: str = self.name_input.text().strip()
        account_type: str = self.account_type_combo.currentText()

        try:
            success, message = self.bank.add_account(account_type, name)
            if success:
                self.name_input.clear()
                self.set_status(message, "success")
                self.refresh_ui()
            else:
                self.set_status(message, "error")
                QMessageBox.warning(self, "Create Account", message)
        except Exception as error:
            self.handle_error("An error occurred while creating the account.", error)

    def deposit_money(self) -> None:
        """Deposit money into the selected account."""
        if not self.selected_account_name:
            QMessageBox.warning(self, "Deposit", "Please select an account first.")
            return

        amount: float = float(self.amount_input.value())
        if amount <= 0:
            QMessageBox.warning(self, "Deposit", "Amount must be greater than 0.")
            return

        try:
            success, message = self.bank.deposit(self.selected_account_name, amount)
            if success:
                self.amount_input.setValue(0.0)
                self.set_status(message, "success")
                self.refresh_ui()
            else:
                self.set_status(message, "error")
                QMessageBox.warning(self, "Deposit", message)
        except Exception as error:
            self.handle_error("An error occurred during deposit.", error)

    def withdraw_money(self) -> None:
        """Withdraw money from the selected account."""
        if not self.selected_account_name:
            QMessageBox.warning(self, "Withdraw", "Please select an account first.")
            return

        amount: float = float(self.amount_input.value())
        if amount <= 0:
            QMessageBox.warning(self, "Withdraw", "Amount must be greater than 0.")
            return

        try:
            success, message = self.bank.withdraw(self.selected_account_name, amount)
            if success:
                self.amount_input.setValue(0.0)
                self.set_status(message, "success")
                self.refresh_ui()
            else:
                self.set_status(message, "error")
                QMessageBox.warning(self, "Withdraw", message)
        except Exception as error:
            self.handle_error("An error occurred during withdrawal.", error)

    def transfer_money(self) -> None:
        """Transfer money from the selected account to another account."""
        if not self.selected_account_name:
            QMessageBox.warning(self, "Transfer", "Please select an account first.")
            return

        to_name: str = self.transfer_to_combo.currentText()
        amount: float = float(self.transfer_amount_input.value())

        if not to_name:
            QMessageBox.warning(self, "Transfer", "Please choose a target account.")
            return

        if amount <= 0:
            QMessageBox.warning(self, "Transfer", "Amount must be greater than 0.")
            return

        try:
            success, message = self.bank.transfer(
                self.selected_account_name,
                to_name,
                amount,
            )
            if success:
                self.transfer_amount_input.setValue(0.0)
                self.set_status(message, "success")
                self.refresh_ui()
            else:
                self.set_status(message, "error")
                QMessageBox.warning(self, "Transfer", message)
        except Exception as error:
            self.handle_error("An error occurred during transfer.", error)

    def save_data(self) -> None:
        """Save account and transaction data to CSV files."""
        try:
            save_accounts(self.bank.get_accounts())
            save_transactions(self.bank.get_transactions())
            self.set_status("Data saved to CSV files.", "success")
            QMessageBox.information(self, "Save CSV", "Data saved successfully.")
        except Exception as error:
            self.handle_error("An error occurred while saving data.", error)

    def load_data(self) -> None:
        """Load account and transaction data from CSV files."""
        try:
            accounts = load_accounts()
            transactions = load_transactions()
            self.bank.load_data(accounts, transactions)

            if self.selected_account_name:
                if self.bank.find_account(self.selected_account_name) is None:
                    self.selected_account_name = ""

            self.set_status("Data loaded from CSV files.", "success")
            self.refresh_ui()
            QMessageBox.information(self, "Load CSV", "Data loaded successfully.")
        except Exception as error:
            self.handle_error("An error occurred while loading data.", error)

    def select_account_from_table(self, row: int, column: int) -> None:
        """
        Select an account from the accounts table.

        Args:
            row: The selected row index.
            column: The selected column index.
        """
        del column
        item = self.accounts_table.item(row, 0)
        if item is not None:
            self.selected_account_name = item.text()
            self.refresh_ui()

    def refresh_ui(self) -> None:
        """Refresh all visible UI data."""
        self.update_accounts_table()
        self.update_history_table()
        self.update_selected_account_label()
        self.update_transfer_targets()
        self.total_label.setText(f"Total Balance: ${self.bank.total_balance():.2f}")

    def update_accounts_table(self) -> None:
        """Update the accounts table with current account data."""
        account_summary = self.bank.get_account_summary()
        self.accounts_table.setRowCount(len(account_summary))

        for row_index, account in enumerate(account_summary):
            self.accounts_table.setItem(row_index, 0, QTableWidgetItem(account["name"]))
            self.accounts_table.setItem(row_index, 1, QTableWidgetItem(account["type"]))
            self.accounts_table.setItem(row_index, 2, QTableWidgetItem(account["balance"]))

        self.accounts_table.resizeColumnsToContents()

    def update_history_table(self) -> None:
        """Update the transaction history table."""
        transactions = self.bank.get_transactions()
        self.history_table.setRowCount(len(transactions))

        for row_index, transaction in enumerate(transactions):
            self.history_table.setItem(
                row_index, 0, QTableWidgetItem(transaction["datetime"])
            )
            self.history_table.setItem(
                row_index, 1, QTableWidgetItem(transaction["action"])
            )
            self.history_table.setItem(
                row_index, 2, QTableWidgetItem(transaction["account"])
            )
            self.history_table.setItem(
                row_index, 3, QTableWidgetItem(transaction["details"])
            )
            self.history_table.setItem(
                row_index, 4, QTableWidgetItem(f"${transaction['amount']}")
            )
            self.history_table.setItem(
                row_index, 5, QTableWidgetItem(transaction["result"])
            )

        self.history_table.resizeColumnsToContents()

    def update_selected_account_label(self) -> None:
        """Update the label showing the currently selected account."""
        if not self.selected_account_name:
            self.selected_label.setText("Selected Account: None")
            return

        account = self.bank.find_account(self.selected_account_name)
        if account is None:
            self.selected_account_name = ""
            self.selected_label.setText("Selected Account: None")
            return

        self.selected_label.setText(
            f"Selected Account: {account.get_name()} | "
            f"Type: {account.get_account_type()} | "
            f"Balance: ${account.get_balance():.2f}"
        )

    def update_transfer_targets(self) -> None:
        """Update the transfer target combo box."""
        current_target: str = self.transfer_to_combo.currentText()
        self.transfer_to_combo.clear()

        for account in self.bank.get_accounts():
            if account.get_name() != self.selected_account_name:
                self.transfer_to_combo.addItem(account.get_name())

        index = self.transfer_to_combo.findText(current_target)
        if index >= 0:
            self.transfer_to_combo.setCurrentIndex(index)

    def set_status(self, message: str, status_type: str) -> None:
        """
        Set the bottom status message.

        Args:
            message: The message to display.
            status_type: The message type.
        """
        if status_type == "success":
            color = "#d4edda"
            border = "#155724"
            text_color = "#155724"
        elif status_type == "error":
            color = "#f8d7da"
            border = "#721c24"
            text_color = "#721c24"
        else:
            color = "#fff3cd"
            border = "#856404"
            text_color = "#856404"

        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            f"""
            padding: 8px;
            border: 1px solid {border};
            background-color: {color};
            color: {text_color};
            font-weight: bold;
            """
        )

    def handle_error(self, user_message: str, error: Exception) -> None:
        """
        Show an error message for an unexpected exception.

        Args:
            user_message: A user-friendly message.
            error: The caught exception.
        """
        full_message = f"{user_message}\n\nDetails: {error}"
        self.set_status(user_message, "error")
        QMessageBox.critical(self, "Error", full_message)