from pydantic import BaseModel, Field, ValidationError
from decimal import Decimal
from account import Currency

class TransactionRequest(BaseModel):
    amount: Decimal=Field(gt=0)
    currency: Currency
    destination_account: str=Field(min_length=26,max_length=26)
    description: str=Field(default="Transfer")

# test_data={'amount':"700", 'currency': "USD", 'destination_account': "12345678901234567890123456", 'description': "Test"}
# try:
#     req=TransactionRequest(**test_data)
#     print("Success")
#     print(req.model_dump())
# except ValidationError as e:
#     print("Fail")
#     print(e.json())