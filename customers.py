"""
Search / Sort / Filter are all implemented as optional query
parameters on GET /customers, e.g.:
  GET /customers?search=dan                  -> name/username contains "dan"
  GET /customers?sort_by=name&order=desc      -> sorted by name, Z-A
  GET /customers?min_accounts=2               -> only customers with 2+ accounts
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from app import store
from app.schemas import CustomerCreate, CustomerUpdate, CustomerOut, CustomerWithAccountsOut, AccountOut

router = APIRouter(prefix="/customers", tags=["customers"])


def _to_out(customer) -> CustomerWithAccountsOut:
    """Converts a domain Customer + its accounts into the response schema."""
    accounts = store.get_accounts_for_customer(customer.id)
    return CustomerWithAccountsOut(
        id=customer.id,
        name=customer.name,
        username=customer.username,
        accounts=[AccountOut(**vars(a)) for a in accounts],
    )


@router.post("", response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerCreate):
    # Enforce unique usernames, same rule the original login() relied on
    for c in store.get_all_customers():
        if c.username == payload.username:
            raise HTTPException(status_code=409, detail="Username already taken")

    customer = store.create_customer(payload.name, payload.username, payload.password)
    return CustomerOut(id=customer.id, name=customer.name, username=customer.username)


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
    results = store.get_all_customers()


    if search:
        needle = search.lower()
        results = [
            c for c in results
            if needle in c.name.lower() or needle in c.username.lower()
        ]


    if min_accounts is not None:
        results = [
            c for c in results
            if len(store.get_accounts_for_customer(c.id)) >= min_accounts
        ]


    if sort_by in ("name", "username", "id"):
        results = sorted(results, key=lambda c: getattr(c, sort_by), reverse=(order == "desc"))

    return [_to_out(c) for c in results]


@router.get("/{customer_id}", response_model=CustomerWithAccountsOut)
def get_customer(customer_id: int):
    customer = store.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return _to_out(customer)




@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, payload: CustomerUpdate):
    customer = store.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    updated = store.update_customer(
        customer_id,
        name=payload.name,
        username=payload.username,
        password=payload.password,
    )
    return CustomerOut(id=updated.id, name=updated.name, username=updated.username)




@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int):
    deleted = store.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
