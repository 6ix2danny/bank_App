
from fastapi import HTTPException

from app.models import account as account_model
from app.models import branch as branch_model
from app.models import customer as customer_model


def create_account(payload):
    customer = customer_model.get_customer(payload.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    if not customer.is_active:
        raise HTTPException(status_code=400, detail="Cannot open an account for an inactive customer")

    if branch_model.get_branch(payload.branch_id) is None:
        raise HTTPException(status_code=404, detail="Branch not found")

    return account_model.create_account(
        payload.customer_id, payload.branch_id, payload.account_type, payload.balance
    )


def list_accounts(
    account_type=None,
    min_balance=None,
    max_balance=None,
    customer_id=None,
    branch_id=None,
    sort_by=None,
    order="asc",
):
    results = account_model.get_all_accounts()

    if account_type:
        results = [a for a in results if a.account_type == account_type]
    if min_balance is not None:
        results = [a for a in results if a.balance >= min_balance]
    if max_balance is not None:
        results = [a for a in results if a.balance <= max_balance]
    if customer_id is not None:
        results = [a for a in results if a.customer_id == customer_id]
    if branch_id is not None:
        results = [a for a in results if a.branch_id == branch_id]

    if sort_by in ("balance", "id", "account_type"):
        results = sorted(results, key=lambda a: getattr(a, sort_by), reverse=(order == "desc"))

    return results


def get_account(account_id):
    account = account_model.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def update_account(account_id, payload):
    get_account(account_id)
    return account_model.update_account(
        account_id, account_type=payload.account_type, balance=payload.balance
    )


def delete_account(account_id):
    get_account(account_id)
    account_model.delete_account(account_id)


def apply_interest(account_id):
    """Computes and persists this account's interest via an atomic credit,
    same rate rules as Account.add_interest()."""
    account = get_account(account_id)
    new_balance = account.add_interest()
    return account_model.update_account(account_id, balance=new_balance)
