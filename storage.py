"""CSV storage utilities for accounts and transactions."""

from __future__ import annotations

import csv
from pathlib import Path

from accounts import Account, CheckingAccount, SavingAccount


ACCOUNTS_FILE: str = "accounts.csv"
TRANSACTIONS_FILE: str = "transactions.csv"


def save_accounts(accounts: list[Account], filename: str = ACCOUNTS_FILE) -> None:
    """
    Save accounts to a CSV file.

    Args:
        accounts: The accounts to save.
        filename: The CSV file name.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "type",
                "name",
                "balance",
                "deposit_count",
                "withdrawal_count",
            ],
        )
        writer.writeheader()
        for account in accounts:
            writer.writerow(account.to_dict())


def load_accounts(filename: str = ACCOUNTS_FILE) -> list[Account]:
    """
    Load accounts from a CSV file.

    Args:
        filename: The CSV file name.

    Returns:
        A list of loaded account objects.
    """
    path: Path = Path(filename)
    if not path.exists():
        return []

    loaded_accounts: list[Account] = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            account_type: str = row["type"]
            name: str = row["name"]
            balance: float = float(row["balance"])

            if account_type == "Account":
                loaded_accounts.append(Account(name, balance))
            elif account_type == "SavingAccount":
                deposit_count: int = int(row.get("deposit_count", "0"))
                loaded_accounts.append(
                    SavingAccount(name, balance, deposit_count)
                )
            elif account_type == "CheckingAccount":
                withdrawal_count: int = int(row.get("withdrawal_count", "0"))
                loaded_accounts.append(
                    CheckingAccount(name, balance, withdrawal_count)
                )

    return loaded_accounts


def save_transactions(
    transactions: list[dict[str, str]],
    filename: str = TRANSACTIONS_FILE,
) -> None:
    """
    Save transactions to a CSV file.

    Args:
        transactions: The transaction history to save.
        filename: The CSV file name.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["datetime", "action", "account", "details", "amount", "result"],
        )
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)


def load_transactions(filename: str = TRANSACTIONS_FILE) -> list[dict[str, str]]:
    """
    Load transactions from a CSV file.

    Args:
        filename: The CSV file name.

    Returns:
        A list of loaded transaction dictionaries.
    """
    path: Path = Path(filename)
    if not path.exists():
        return []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]