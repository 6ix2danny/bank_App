"""
Search / Sort / Filter are all implemented as optional query
parameters on GET /api/v1/customers, e.g.:
  GET /api/v1/customers?search=dan                  -> name/username contains "dan"
  GET /api/v1/customers?sort_by=name&order=desc      -> sorted by name, Z-A
  GET /api/v1/customers?min_accounts=2               -> only customers with 2+ accounts
"""

from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.schemas import (
    AccountOut,
    CustomerCreate,
    CustomerOut,
    CustomerUpdate,
    CustomerWithAccountsOut,
)
from app.services import customer_service

router = APIRouter(prefix="/customers", tags=["customers"])


def _to_out(customer) -> CustomerWithAccountsOut:
    accounts = customer_service.accounts_for_customer(customer.id)
    return CustomerWithAccountsOut(
        id=customer.id,
        name=customer.name,
        username=customer.username,
        is_active=customer.is_active,
        accounts=[AccountOut(**vars(a)) for a in accounts],
    )


def _to_customer_out(customer) -> CustomerOut:
    return CustomerOut(
        id=customer.id, name=customer.name, username=customer.username, is_active=customer.is_active
    )


@router.post("", response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerCreate):
    return _to_customer_out(customer_service.create_customer(payload))


@router.get("", response_model=List[CustomerWithAccountsOut])
def list_customers(
    search: Optional[str] = Query(
        default=None,
        description="Case-insensitive substring match against name or username",
    ),
    sort_by: Optional[str] = Query(
        default=None,
        description="Field to sort by: 'name', 'username', or 'id'",
    ),
    order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sort direction: 'asc' or 'desc'",
    ),
    min_accounts: Optional[int] = Query(
        default=None,
        description="Filter: only customers with at least this many accounts",
    ),
):
    results = customer_service.list_customers(
        search=search, sort_by=sort_by, order=order, min_accounts=min_accounts
    )
    return [_to_out(c) for c in results]


@router.get("/{customer_id}", response_model=CustomerWithAccountsOut)
def get_customer(customer_id: int):
    return _to_out(customer_service.get_customer(customer_id))


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, payload: CustomerUpdate):
    return _to_customer_out(customer_service.update_customer(customer_id, payload))


@router.delete("/{customer_id}", status_code=204)
def deactivate_customer(customer_id: int):
    customer_service.deactivate_customer(customer_id)
    return None
