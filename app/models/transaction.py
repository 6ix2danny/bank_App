
from datetime import datetime, timezone

from app.db import get_db, next_id


class Transaction:
    def __init__(self, transaction_id, from_account_id, to_account_id, amount, type_, status, created_at):
        self.id = transaction_id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.type = type_
        self.status = status
        self.created_at = created_at


def _from_doc(doc):
    if doc is None:
        return None
    return Transaction(
        doc["_id"],
        doc["from_account_id"],
        doc["to_account_id"],
        doc["amount"],
        doc["type"],
        doc["status"],
        doc["created_at"],
    )


def create_transaction(from_account_id, to_account_id, amount, type_="TRANSFER", status="COMPLETED"):
    transaction_id = next_id("transaction_id")
    # Naive UTC: pymongo's default MongoClient returns naive datetimes on
    # read (tz_aware=False), so we store naive UTC consistently to keep
    # reads and writes comparable.
    created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    get_db().transactions.insert_one(
        {
            "_id": transaction_id,
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount": amount,
            "type": type_,
            "status": status,
            "created_at": created_at,
        }
    )
    return Transaction(transaction_id, from_account_id, to_account_id, amount, type_, status, created_at)


def get_all_transactions():
    return [_from_doc(d) for d in get_db().transactions.find().sort("_id", 1)]
