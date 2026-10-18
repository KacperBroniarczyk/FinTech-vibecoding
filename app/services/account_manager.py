from decimal import Decimal
import app.core.exceptions
from app.core.schemas import Currency


class BankAccount:
    def __init__(self,account_id: str, currency: Currency, initial_balance: Decimal=Decimal("0.00")) -> None:
        self.account_id = account_id
        self._currency = currency
        self._balance: Decimal = initial_balance

    @property
    def balance(self) -> Decimal:
        return self._balance

    def withdraw(self, amount: Decimal) -> None:
        if amount <= Decimal("0.00"):
            raise app.core.exceptions.InvalidTransactionAmountError("Invalid transaction amount")
        if self._balance < amount:
            raise app.core.exceptions.InsufficientFundsError("Insufficient funds")
        self._balance -= amount

    def deposit(self, amount: Decimal) -> None:
        if amount <= Decimal("0.00"):
            raise app.core.exceptions.InvalidTransactionAmountError("Invalid transaction amount")
        self._balance += amount

accounts_db:dict[str, BankAccount]={
"12345678901234567890123456": BankAccount(
    account_id="12345678901234567890123456",
    currency=Currency.USD,
    initial_balance=Decimal("1000.00")
    )
}
