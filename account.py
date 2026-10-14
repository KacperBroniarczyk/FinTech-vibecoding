from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass
from decimal import Decimal

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"

class InsufficientFundsError(Exception):
    pass
class InvalidTransactionAmountError(Exception):
    pass

@dataclass(frozen=True)
class Transaction:
    amount: Decimal
    transaction_type: str
    transaction_date: datetime

class BankAccount:
    def __init__(self, account_id: str, currency: Currency, initial_balance: Decimal=Decimal("0.00"))->None:
        if initial_balance < Decimal("0.00"):
            raise InvalidTransactionAmountError
        self.account_id = account_id
        self.currency = currency
        self._balance: Decimal = initial_balance
        self._history: list[Transaction] = []

    @property
    def balance(self)->Decimal:
        return self._balance

    def deposit(self, amount: Decimal)->None:
        if amount <= Decimal("0.00"):
            raise InvalidTransactionAmountError
        else:
            self._balance += amount
            self._history.append(Transaction(amount, "DEPOSIT", datetime.now(timezone.utc)))

    def withdraw(self, amount: Decimal)->None:
        if amount <= Decimal("0.00"):
            raise InvalidTransactionAmountError
        elif amount > self.balance:
            raise InsufficientFundsError
        else:
            self._balance -= amount
            self._history.append(Transaction(amount, "WITHDRAWAL", datetime.now(timezone.utc)))

    def get_history(self)->list[Transaction]:
        return self._history.copy()