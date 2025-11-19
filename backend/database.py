import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from bson import ObjectId

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client = MongoClient(DATABASE_URL)
_db = _client[DATABASE_NAME]

# Helpers

def _serialize_id(document: Dict[str, Any]) -> Dict[str, Any]:
    if document is None:
        return document
    doc = document.copy()
    _id = doc.get("_id")
    if isinstance(_id, ObjectId):
        doc["_id"] = str(_id)
    return doc

# Public API used by app

def db():
    return _db


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    data["created_at"] = data.get("created_at", now)
    data["updated_at"] = now
    res = _db[collection_name].insert_one(data)
    inserted = _db[collection_name].find_one({"_id": res.inserted_id})
    return _serialize_id(inserted)


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    cursor = _db[collection_name].find(filter_dict or {}).limit(limit)
    return [_serialize_id(doc) for doc in cursor]


def get_document(collection_name: str, _id: str) -> Optional[Dict[str, Any]]:
    try:
        oid = ObjectId(_id)
    except Exception:
        return None
    found = _db[collection_name].find_one({"_id": oid})
    return _serialize_id(found) if found else None
