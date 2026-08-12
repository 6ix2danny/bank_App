
from pymongo import ReturnDocument

from app.db import get_db, next_id


class Branch:
    def __init__(self, branch_id, name, address):
        self.id = branch_id
        self.name = name
        self.address = address


def _from_doc(doc):
    if doc is None:
        return None
    return Branch(doc["_id"], doc["name"], doc["address"])


def create_branch(name, address):
    branch_id = next_id("branch_id")
    get_db().branches.insert_one({"_id": branch_id, "name": name, "address": address})
    return Branch(branch_id, name, address)


def get_branch(branch_id):
    return _from_doc(get_db().branches.find_one({"_id": branch_id}))


def get_all_branches():
    return [_from_doc(d) for d in get_db().branches.find().sort("_id", 1)]


def update_branch(branch_id, name=None, address=None):
    updates = {}
    if name is not None:
        updates["name"] = name
    if address is not None:
        updates["address"] = address
    if not updates:
        return get_branch(branch_id)

    doc = get_db().branches.find_one_and_update(
        {"_id": branch_id}, {"$set": updates}, return_document=ReturnDocument.AFTER
    )
    return _from_doc(doc)


def delete_branch(branch_id):
    result = get_db().branches.delete_one({"_id": branch_id})
    return result.deleted_count > 0
