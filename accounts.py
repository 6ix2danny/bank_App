

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from app import store
from app.schemas import AccountCreate, AccountUpdate, AccountOut

router = APIRouter(prefix="/accounts", tags=["accounts"])



@router.post("", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate):
    if store.get_customer(payload.customer_id) is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    account = store.create_account(payload.customer_id, payload.account_type, payload.balance)
    return AccountOut(**vars(account))



@router.get("", response_model=List[AccountOut])
def list_accounts(
    account_type: Optional[str] = Query(
        default=None,
        pattern="^(checking|savings)$",
        description="Filter: only accounts of this type",
    ),
    min_balance: Optional[float] = Query(default=None, description="Filter: balance >= this"),
    max_balance: Optional[float] = Query(default=None, description="Filter: balance <= this"),
    customer_id: Optional[int] = Query(default=None, description="Filter: only this customer's accounts"),
    sort_by: Optional[str] = Query(
        default=None,
        description="Field to sort by: 'balance', 'id', or 'account_type'",
    ),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    results = store.get_all_accounts()


    if account_type:
        results = [a for a in results if a.account_type == account_type]
    if min_balance is not None:
        results = [a for a in results if a.balance >= min_balance]
    if max_balance is not None:
        results = [a for a in results if a.balance <= max_balance]
    if customer_id is not None:
        results = [a for a in results if a.customer_id == customer_id]


    if sort_by in ("balance", "id", "account_type"):
        results = sorted(results, key=lambda a: getattr(a, sort_by), reverse=(order == "desc"))

    return [AccountOut(**vars(a)) for a in results]


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int):
    account = store.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountOut(**vars(account))



@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, payload: AccountUpdate):
    account = store.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    updated = store.update_account(
        account_id,
        account_type=payload.account_type,
        balance=payload.balance,
    )
    return AccountOut(**vars(updated))


@router.post("/{account_id}/add-interest", response_model=AccountOut)
def add_interest(account_id: int):
    """Extra action endpoint (not pure CRUD) - applies this account's
    interest rate and returns the updated balance, same behavior as
    addInterest() in the Java version."""
    account = store.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    account.add_interest()
    return AccountOut(**vars(account))


@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: int):
    deleted = store.delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account not found")
    return None
