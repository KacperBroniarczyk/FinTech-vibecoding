from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"

class TransactionRequest(BaseModel):
    amount: Decimal=Field(gt=0, decimal_places=2)
    currency: Currency
    destination_account: str=Field(min_length=26,max_length=26)
    description: str=Field(default="Transfer")

class AccountResponse(BaseModel):
    account_id: str
    balance: Decimal
    currency: Currency