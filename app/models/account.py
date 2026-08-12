
from pymongo import ReturnDocument

from app.db import get_db, next_id


class Account:
    def __init__(self, account_id, customer_id, branch_id, account_type, balance=0):
        self.id = account_id
        self.customer_id = customer_id
        self.branch_id = branch_id
        self.account_type = account_type  # "checking" or "savings"
        self.balance = balance

    def add_interest(self):
        """Applies interest based on account type and returns the new
        balance. Savings earns 3%, checking earns 2% - same rule as the
        original Java version's CheckingAccount/SavingsAccount classes."""
        rate = 0.03 if self.account_type == "savings" else 0.02
        self.balance = round(self.balance * (1 + rate), 2)
        return self.balance


def _from_doc(doc):
    if doc is None:
        return None
    return Account(doc["_id"], doc["customer_id"], doc["branch_id"], doc["account_type"], doc["balance"])


def create_account(customer_id, branch_id, account_type, balance=0):
    account_id = next_id("account_id")
    get_db().accounts.insert_one(
        {
            "_id": account_id,
            "customer_id": customer_id,
            "branch_id": branch_id,
            "account_type": account_type,
            "balance": balance,
        }
    )
    return Account(account_id, customer_id, branch_id, account_type, balance)


def get_account(account_id):
    return _from_doc(get_db().accounts.find_one({"_id": account_id}))


def get_all_accounts():
    return [_from_doc(d) for d in get_db().accounts.find().sort("_id", 1)]


def get_accounts_for_customer(customer_id):
    docs = get_db().accounts.find({"customer_id": customer_id}).sort("_id", 1)
    return [_from_doc(d) for d in docs]


def update_account(account_id, account_type=None, balance=None):
    updates = {}
    if account_type is not None:
        updates["account_type"] = account_type
    if balance is not None:
        updates["balance"] = balance
    if not updates:
        return get_account(account_id)

    doc = get_db().accounts.find_one_and_update(
        {"_id": account_id}, {"$set": updates}, return_document=ReturnDocument.AFTER
    )
    return _from_doc(doc)


def try_debit(account_id, amount):
    """Atomically decrements balance only if it's sufficient, so two
    concurrent transfers can't both pass a balance check and overdraw the
    account. Returns the updated Account, or None if funds were insufficient
    (or the account doesn't exist)."""
    doc = get_db().accounts.find_one_and_update(
        {"_id": account_id, "balance": {"$gte": amount}},
        {"$inc": {"balance": -amount}},
        return_document=ReturnDocument.AFTER,
    )
    return _from_doc(doc)


def credit(account_id, amount):
    doc = get_db().accounts.find_one_and_update(
        {"_id": account_id},
        {"$inc": {"balance": amount}},
        return_document=ReturnDocument.AFTER,
    )
    return _from_doc(doc)


def delete_account(account_id):
    result = get_db().accounts.delete_one({"_id": account_id})
    return result.deleted_count > 0
