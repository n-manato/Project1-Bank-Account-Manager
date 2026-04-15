"""Bank logic for managing accounts and transaction history."""

from __future__ import annotations

from datetime import datetime

from accounts import Account, CheckingAccount, SavingAccount


class Bank:
    """A class that manages multiple bank accounts and transaction history."""

    def __init__(self) -> None:
        """Initialize the bank with empty account and transaction lists."""
        self.__accounts: list[Account] = []
        self.__transactions: list[dict[str, str]] = []

    def get_accounts(self) -> list[Account]:
        """
        Get the list of all accounts.

        Returns:
            A list of account objects.
        """
        return self.__accounts

    def get_transactions(self) -> list[dict[str, str]]:
        """
        Get the transaction history.

        Returns:
            A list of transaction dictionaries.
        """
        return self.__transactions

    def add_account(self, account_type: str, name: str) -> tuple[bool, str]:
        """
        Create and add a new account.

        Args:
            account_type: The type of account to create.
            name: The account owner's name.

        Returns:
            A tuple containing success status and a message.
        """
        clean_name: str = name.strip()

        if not clean_name:
            return False, "Account name cannot be empty."

        if self.find_account(clean_name) is not None:
            return False, "An account with this name already exists."

        if account_type == "Account":
            account: Account = Account(clean_name)
        elif account_type == "SavingAccount":
            account = SavingAccount(clean_name)
        elif account_type == "CheckingAccount":
            account = CheckingAccount(clean_name)
        else:
            return False, "Invalid account type."

        self.__accounts.append(account)
        self._add_transaction(
            action="Create",
            account=clean_name,
            details=f"Created {account_type}",
            amount=0.0,
            result="Success",
        )
        return True, f"{account_type} created for {clean_name}."

    def find_account(self, name: str) -> Account | None:
        """
        Find an account by name.

        Args:
            name: The account owner's name.

        Returns:
            The matching account, or None if not found.
        """
        target_name: str = name.strip().lower()
        for account in self.__accounts:
            if account.get_name().lower() == target_name:
                return account
        return None

    def deposit(self, name: str, amount: float) -> tuple[bool, str]:
        """
        Deposit money into an account.

        Args:
            name: The account owner's name.
            amount: The amount to deposit.

        Returns:
            A tuple containing success status and a message.
        """
        account: Account | None = self.find_account(name)
        if account is None:
            return False, "Account not found."

        if amount <= 0:
            return False, "Deposit amount must be greater than 0."

        success: bool = account.deposit(amount)
        result: str = "Success" if success else "Failed"
        self._add_transaction(
            action="Deposit",
            account=account.get_name(),
            details="Deposit made",
            amount=amount,
            result=result,
        )

        if success:
            return True, f"Deposited ${amount:.2f} into {account.get_name()}."
        return False, "Deposit failed."

    def withdraw(self, name: str, amount: float) -> tuple[bool, str]:
        """
        Withdraw money from an account.

        Args:
            name: The account owner's name.
            amount: The amount to withdraw.

        Returns:
            A tuple containing success status and a message.
        """
        account: Account | None = self.find_account(name)
        if account is None:
            return False, "Account not found."

        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0."

        success: bool = account.withdraw(amount)
        result: str = "Success" if success else "Failed"
        self._add_transaction(
            action="Withdraw",
            account=account.get_name(),
            details="Withdrawal made",
            amount=amount,
            result=result,
        )

        if success:
            return True, f"Withdrew ${amount:.2f} from {account.get_name()}."
        return False, "Withdrawal failed. Check balance or account rules."

    def transfer(self, from_name: str, to_name: str, amount: float) -> tuple[bool, str]:
        """
        Transfer money from one account to another.

        Args:
            from_name: The sender account owner's name.
            to_name: The receiver account owner's name.
            amount: The amount to transfer.

        Returns:
            A tuple containing success status and a message.
        """
        from_account: Account | None = self.find_account(from_name)
        to_account: Account | None = self.find_account(to_name)

        if from_account is None or to_account is None:
            return False, "One or both accounts were not found."

        if from_account.get_name() == to_account.get_name():
            return False, "You cannot transfer to the same account."

        if amount <= 0:
            return False, "Transfer amount must be greater than 0."

        if not from_account.withdraw(amount):
            self._add_transaction(
                action="Transfer",
                account=from_account.get_name(),
                details=f"Transfer to {to_account.get_name()}",
                amount=amount,
                result="Failed",
            )
            return False, "Transfer failed. Check balance or account rules."

        deposit_success: bool = to_account.deposit(amount)
        if not deposit_success:
            from_account.deposit(amount)
            self._add_transaction(
                action="Transfer",
                account=from_account.get_name(),
                details=f"Transfer to {to_account.get_name()}",
                amount=amount,
                result="Failed",
            )
            return False, "Transfer failed during deposit."

        self._add_transaction(
            action="Transfer",
            account=from_account.get_name(),
            details=f"Transfer to {to_account.get_name()}",
            amount=amount,
            result="Success",
        )
        return (
            True,
            f"Transferred ${amount:.2f} from {from_account.get_name()} "
            f"to {to_account.get_name()}.",
        )

    def get_account_summary(self) -> list[dict[str, str]]:
        """
        Get account data for table display.

        Returns:
            A list of dictionaries containing account display data.
        """
        summary: list[dict[str, str]] = []
        for account in self.__accounts:
            summary.append(
                {
                    "name": account.get_name(),
                    "type": account.get_account_type(),
                    "balance": f"${account.get_balance():.2f}",
                }
            )
        return summary

    def total_balance(self) -> float:
        """
        Get the total money in the bank.

        Returns:
            The total balance of all accounts.
        """
        return sum(account.get_balance() for account in self.__accounts)

    def load_data(
        self,
        accounts: list[Account],
        transactions: list[dict[str, str]],
    ) -> None:
        """
        Replace the current bank data with loaded data.

        Args:
            accounts: A list of loaded accounts.
            transactions: A list of loaded transactions.
        """
        self.__accounts = accounts
        self.__transactions = transactions

    def _add_transaction(
        self,
        action: str,
        account: str,
        details: str,
        amount: float,
        result: str,
    ) -> None:
        """
        Add a transaction record.

        Args:
            action: The type of action performed.
            account: The account name involved.
            details: Extra details about the action.
            amount: The transaction amount.
            result: The result of the action.
        """
        self.__transactions.append(
            {
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": action,
                "account": account,
                "details": details,
                "amount": f"{amount:.2f}",
                "result": result,
            }
        )