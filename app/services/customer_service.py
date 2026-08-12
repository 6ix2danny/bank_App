
from fastapi import HTTPException

from app.models import account as account_model
from app.models import customer as customer_model


def create_customer(payload):
    if customer_model.find_by_username(payload.username) is not None:
        raise HTTPException(status_code=400, detail="Username already taken")
    return customer_model.create_customer(payload.name, payload.username, payload.password)


def list_customers(search=None, sort_by=None, order="asc", min_accounts=None):
    results = [c for c in customer_model.get_all_customers() if c.is_active]

    if search:
        needle = search.lower()
        results = [c for c in results if needle in c.name.lower() or needle in c.username.lower()]

    if min_accounts is not None:
        results = [
            c for c in results
            if len(account_model.get_accounts_for_customer(c.id)) >= min_accounts
        ]

    if sort_by in ("name", "username", "id"):
        results = sorted(results, key=lambda c: getattr(c, sort_by), reverse=(order == "desc"))

    return results


def get_customer(customer_id):
    customer = customer_model.get_customer(customer_id)
    if customer is None or not customer.is_active:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def update_customer(customer_id, payload):
    get_customer(customer_id)

    if payload.username is not None:
        existing = customer_model.find_by_username(payload.username)
        if existing is not None and existing.id != customer_id:
            raise HTTPException(status_code=400, detail="Username already taken")

    return customer_model.update_customer(
        customer_id,
        name=payload.name,
        username=payload.username,
        password=payload.password,
    )


def deactivate_customer(customer_id):
    """Soft-delete: marks the customer inactive rather than removing their
    record, so account/transaction history stays intact for audit
    purposes. Their accounts are left untouched."""
    get_customer(customer_id)
    customer_model.set_active(customer_id, False)


def accounts_for_customer(customer_id):
    return account_model.get_accounts_for_customer(customer_id)
