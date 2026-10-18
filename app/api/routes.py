from fastapi import APIRouter, HTTPException
from app.core.schemas import TransactionRequest, AccountResponse
from app.core.exceptions import InsufficientFundsError, InvalidTransactionAmountError
from app.services.account_manager import accounts_db
from app.services.anti_fraud import check_fraud

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/{account_id}/balance", response_model=AccountResponse)
async def get_balance(account_id: str):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    account = accounts_db[account_id]
    return AccountResponse(account_id=account.account_id, balance=account.balance, currency=account.currency)

@router.post("/{account_id}/withdraw")
async def withdraw(account_id: str, request: TransactionRequest):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    is_fraud = await check_fraud(request.amount)
    if is_fraud:
        raise HTTPException(status_code=403, detail="Transaction blocked by Anti-Fraud system")
    account = accounts_db[account_id]
    try:
        account.withdraw(request.amount)
    except InvalidTransactionAmountError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success", "new_balance": account.balance}

@router.post("/{account_id}/deposit")
async def deposit(account_id: str, request: TransactionRequest):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    is_fraud = await check_fraud(request.amount)
    if is_fraud:
        raise HTTPException(status_code=403, detail="Transaction blocked by Anti-Fraud system")
    account = accounts_db[account_id]
    try:
        account.deposit(request.amount)
    except InvalidTransactionAmountError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success", "new_balance": account.balance}
