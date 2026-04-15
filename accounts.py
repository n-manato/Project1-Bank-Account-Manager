"""Account classes for the Bank Account Manager."""

from __future__ import annotations


class Account:
    """A basic bank account with deposit and withdrawal support."""

    def __init__(self, name: str, balance: float = 0.0) -> None:
        """
        Initialize an account.

        Args:
            name: The account owner's name.
            balance: The starting balance.
        """
        self.__account_name: str = name
        self.__account_balance: float = 0.0
        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account.

        Args:
            amount: The amount to deposit.

        Returns:
            True if the deposit succeeds, otherwise False.
        """
        if amount <= 0:
            return False
        self.__account_balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account.

        Args:
            amount: The amount to withdraw.

        Returns:
            True if the withdrawal succeeds, otherwise False.
        """
        if amount <= 0 or amount > self.__account_balance:
            return False
        self.__account_balance -= amount
        return True

    def get_balance(self) -> float:
        """
        Get the current account balance.

        Returns:
            The current balance.
        """
        return self.__account_balance

    def get_name(self) -> str:
        """
        Get the account owner's name.

        Returns:
            The account owner's name.
        """
        return self.__account_name

    def set_balance(self, value: float) -> None:
        """
        Set the account balance.

        Args:
            value: The new balance value.
        """
        if value < 0:
            self.__account_balance = 0.0
        else:
            self.__account_balance = value

    def set_name(self, value: str) -> None:
        """
        Set the account owner's name.

        Args:
            value: The new account name.
        """
        self.__account_name = value

    def get_account_type(self) -> str:
        """
        Get the account type name.

        Returns:
            The account type.
        """
        return "Account"

    def to_dict(self) -> dict[str, str]:
        """
        Convert the account to a dictionary for CSV saving.

        Returns:
            A dictionary representation of the account.
        """
        return {
            "type": self.get_account_type(),
            "name": self.get_name(),
            "balance": f"{self.get_balance():.2f}",
            "deposit_count": "0",
            "withdrawal_count": "0",
        }

    def __str__(self) -> str:
        """
        Return a readable string representation of the account.

        Returns:
            A formatted account string.
        """
        return (
            f"Account name = {self.get_name()}, "
            f"Account balance = {self.get_balance():.2f}"
        )


class SavingAccount(Account):
    """A savings account with a minimum balance and periodic interest."""

    MINIMUM: float = 100.0
    RATE: float = 0.02

    def __init__(
        self,
        name: str,
        balance: float = MINIMUM,
        deposit_count: int = 0,
    ) -> None:
        """
        Initialize a savings account.

        Args:
            name: The account owner's name.
            balance: The starting balance.
            deposit_count: The number of successful deposits already made.
        """
        super().__init__(name, max(balance, SavingAccount.MINIMUM))
        self.__deposit_count: int = deposit_count

    def apply_interest(self) -> None:
        """Apply interest to the account balance."""
        self.set_balance(self.get_balance() * (1 + SavingAccount.RATE))

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the savings account.

        Every 5 successful deposits, interest is applied.

        Args:
            amount: The amount to deposit.

        Returns:
            True if the deposit succeeds, otherwise False.
        """
        success = super().deposit(amount)
        if success:
            self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
        return success

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money while keeping the minimum balance.

        Args:
            amount: The amount to withdraw.

        Returns:
            True if the withdrawal succeeds, otherwise False.
        """
        if amount <= 0 or self.get_balance() - amount < SavingAccount.MINIMUM:
            return False
        self.set_balance(self.get_balance() - amount)
        return True

    def set_balance(self, value: float) -> None:
        """
        Set the savings account balance.

        The balance cannot go below the minimum.

        Args:
            value: The new balance value.
        """
        if value < SavingAccount.MINIMUM:
            super().set_balance(SavingAccount.MINIMUM)
        else:
            super().set_balance(value)

    def get_deposit_count(self) -> int:
        """
        Get the number of successful deposits.

        Returns:
            The deposit count.
        """
        return self.__deposit_count

    def get_account_type(self) -> str:
        """
        Get the account type name.

        Returns:
            The account type.
        """
        return "SavingAccount"

    def to_dict(self) -> dict[str, str]:
        """
        Convert the account to a dictionary for CSV saving.

        Returns:
            A dictionary representation of the account.
        """
        return {
            "type": self.get_account_type(),
            "name": self.get_name(),
            "balance": f"{self.get_balance():.2f}",
            "deposit_count": str(self.get_deposit_count()),
            "withdrawal_count": "0",
        }

    def __str__(self) -> str:
        """
        Return a readable string representation of the savings account.

        Returns:
            A formatted savings account string.
        """
        return f"SAVING ACCOUNT: {super().__str__()}"


class CheckingAccount(Account):
    """A checking account with a withdrawal fee after several withdrawals."""

    FREE_WITHDRAWALS: int = 3
    WITHDRAWAL_FEE: float = 1.0

    def __init__(
        self,
        name: str,
        balance: float = 0.0,
        withdrawal_count: int = 0,
    ) -> None:
        """
        Initialize a checking account.

        Args:
            name: The account owner's name.
            balance: The starting balance.
            withdrawal_count: The number of successful withdrawals already made.
        """
        super().__init__(name, balance)
        self.__withdrawal_count: int = withdrawal_count

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the checking account.

        After the free withdrawals are used, a fee is charged.

        Args:
            amount: The amount to withdraw.

        Returns:
            True if the withdrawal succeeds, otherwise False.
        """
        if amount <= 0:
            return False

        fee: float = 0.0
        if self.__withdrawal_count >= CheckingAccount.FREE_WITHDRAWALS:
            fee = CheckingAccount.WITHDRAWAL_FEE

        total_needed: float = amount + fee
        if total_needed > self.get_balance():
            return False

        self.set_balance(self.get_balance() - total_needed)
        self.__withdrawal_count += 1
        return True

    def get_withdrawal_count(self) -> int:
        """
        Get the number of successful withdrawals.

        Returns:
            The withdrawal count.
        """
        return self.__withdrawal_count

    def get_account_type(self) -> str:
        """
        Get the account type name.

        Returns:
            The account type.
        """
        return "CheckingAccount"

    def to_dict(self) -> dict[str, str]:
        """
        Convert the account to a dictionary for CSV saving.

        Returns:
            A dictionary representation of the account.
        """
        return {
            "type": self.get_account_type(),
            "name": self.get_name(),
            "balance": f"{self.get_balance():.2f}",
            "deposit_count": "0",
            "withdrawal_count": str(self.get_withdrawal_count()),
        }

    def __str__(self) -> str:
        """
        Return a readable string representation of the checking account.

        Returns:
            A formatted checking account string.
        """
        return f"CHECKING ACCOUNT: {super().__str__()}"