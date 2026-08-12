
from datetime import datetime, time

from fastapi import HTTPException

from app.models import account as account_model
from app.models import transaction as transaction_model


def transfer(payload):
    if payload.from_account_id == payload.to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")

    if account_model.get_account(payload.from_account_id) is None:
        raise HTTPException(status_code=404, detail="Source account not found")
    if account_model.get_account(payload.to_account_id) is None:
        raise HTTPException(status_code=404, detail="Destination account not found")

    # Atomic conditional decrement: the balance check and the debit happen
    # in one Mongo operation, so two concurrent transfers can't both pass
    # the check and overdraw the account.
    debited = account_model.try_debit(payload.from_account_id, payload.amount)
    if debited is None:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account_model.credit(payload.to_account_id, payload.amount)

    return transaction_model.create_transaction(
        payload.from_account_id, payload.to_account_id, payload.amount
    )


def list_transactions(start_date=None, type=None):
    results = transaction_model.get_all_transactions()

    if start_date is not None:
        start = datetime.combine(start_date, time.min)
        results = [t for t in results if t.created_at >= start]

    if type is not None:
        results = [t for t in results if t.type == type]

    return results
