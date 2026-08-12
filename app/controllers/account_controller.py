
from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.schemas import AccountCreate, AccountOut, AccountUpdate
from app.services import account_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate):
    return AccountOut(**vars(account_service.create_account(payload)))


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
    branch_id: Optional[int] = Query(default=None, description="Filter: only this branch's accounts"),
    sort_by: Optional[str] = Query(
        default=None,
        description="Field to sort by: 'balance', 'id', or 'account_type'",
    ),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    results = account_service.list_accounts(
        account_type=account_type,
        min_balance=min_balance,
        max_balance=max_balance,
        customer_id=customer_id,
        branch_id=branch_id,
        sort_by=sort_by,
        order=order,
    )
    return [AccountOut(**vars(a)) for a in results]


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int):
    return AccountOut(**vars(account_service.get_account(account_id)))


@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, payload: AccountUpdate):
    return AccountOut(**vars(account_service.update_account(account_id, payload)))


@router.post("/{account_id}/add-interest", response_model=AccountOut)
def add_interest(account_id: int):
    """Extra action endpoint (not pure CRUD) - applies this account's
    interest rate and returns the updated balance, same behavior as
    addInterest() in the Java version."""
    return AccountOut(**vars(account_service.apply_interest(account_id)))


@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: int):
    account_service.delete_account(account_id)
    return None
