
from pymongo import ReturnDocument

from app.db import get_db, next_id


class Customer:
    def __init__(self, customer_id, name, username, password, is_active=True):
        self.id = customer_id
        self.name = name
        self.username = username
        self.password = password
        self.is_active = is_active


def _from_doc(doc):
    if doc is None:
        return None
    return Customer(doc["_id"], doc["name"], doc["username"], doc["password"], doc["is_active"])


def create_customer(name, username, password):
    customer_id = next_id("customer_id")
    get_db().customers.insert_one(
        {
            "_id": customer_id,
            "name": name,
            "username": username,
            "password": password,
            "is_active": True,
        }
    )
    return Customer(customer_id, name, username, password)


def get_customer(customer_id):
    return _from_doc(get_db().customers.find_one({"_id": customer_id}))


def get_all_customers():
    return [_from_doc(d) for d in get_db().customers.find().sort("_id", 1)]


def find_by_username(username):
    return _from_doc(get_db().customers.find_one({"username": username}))


def update_customer(customer_id, name=None, username=None, password=None):
    updates = {}
    if name is not None:
        updates["name"] = name
    if username is not None:
        updates["username"] = username
    if password is not None:
        updates["password"] = password
    if not updates:
        return get_customer(customer_id)

    doc = get_db().customers.find_one_and_update(
        {"_id": customer_id}, {"$set": updates}, return_document=ReturnDocument.AFTER
    )
    return _from_doc(doc)


def set_active(customer_id, is_active):
    doc = get_db().customers.find_one_and_update(
        {"_id": customer_id},
        {"$set": {"is_active": is_active}},
        return_document=ReturnDocument.AFTER,
    )
    return _from_doc(doc)
