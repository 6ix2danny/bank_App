"""
Mongo connection handling.
"""

from pymongo import MongoClient, ReturnDocument

from app.config import MONGODB_DB, MONGODB_URI

_client = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client


def get_db():
    return get_client()[MONGODB_DB]


def next_id(counter_name):
    """Atomically increments and returns a sequential id, backed by a
    Mongo counters collection - keeps ids as plain ints (1, 2, 3, ...)
    instead of switching the API over to ObjectId strings."""
    doc = get_db().counters.find_one_and_update(
        {"_id": counter_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return doc["seq"]
