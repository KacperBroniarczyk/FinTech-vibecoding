from fastapi import FastAPI, HTTPException
from account import BankAccount, Currency, InsufficientFundsError, InvalidTransactionAmountError
from models import TransactionRequest
from decimal import Decimal

app = FastAPI(title="FinTech Core API")

accounts_db:dict[str, BankAccount]={
    "12345678901234567890123456": BankAccount(
        account_id="12345678901234567890123456",
        currency=Currency.USD,
        initial_balance=Decimal("1000.00")
    )
}

@app.post("/accounts/{account_id}/withdraw")
def withdraw_money(account_id: str, request: TransactionRequest):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    account=accounts_db[account_id]
    try:
        account.withdraw(request.amount)
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidTransactionAmountError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status":"success","new_balance":account.balance}

@app.post("/accounts/{account_id}/deposit")
def deposit_money(account_id: str, request: TransactionRequest):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    account = accounts_db[account_id]
    try:
        account.deposit(request.amount)
    except InvalidTransactionAmountError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success", "new_balance": account.balance}

@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    account=accounts_db[account_id]
    return {"account_balance": account.balance, "currency": account.currency}