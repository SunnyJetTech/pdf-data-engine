from __future__ import annotations
from typing import Any
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from core.config import settings

class MongoIntegration:
    _client: MongoClient | None = None

    @classmethod
    def client(cls) -> MongoClient:
        if cls._client is None:
            cls._client = MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)

        return cls._client

    @classmethod
    def database(cls) -> Database:
        return cls.client()[settings.MONGO_DATABASE]

    @classmethod
    def collection(cls, collection_name: str) -> Collection:
        return cls.database()[collection_name]

    @classmethod
    def append_dataframe(cls, *, collection_name: str, dataframe: DataFrame) -> int:
        rows = dataframe.to_dict("records")

        if not rows:
            return 0

        collection = cls.collection(collection_name)
        collection.insert_many(rows)

        return len(rows)

    @classmethod
    def search(cls, *, collection_name: str, query: dict[str, Any], page: int, page_size: int) -> dict[str, Any]:
        collection = cls.collection(collection_name)
        total = collection.count_documents(query)
        skip = max(page - 1, 0) * page_size

        rows = list(collection.find(query, {"_id": 0}) .skip(skip) .limit(page_size))

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": rows,
        }

    @classmethod
    def columns(cls, *, collection_name: str) -> list[str]:
        collection = cls.collection(collection_name)
        row = collection.find_one()

        if not row:
            return []

        row.pop("_id", None)

        return list(row.keys())

    @classmethod
    def sample(cls, *, collection_name: str, limit: int = 10) -> list[dict[str, Any]]:
        collection = cls.collection(collection_name)

        return list(collection.find( {}, {"_id": 0}).limit(limit))

    @classmethod
    def statistics(cls, *, collection_name: str) -> dict[str, Any]:
        collection = cls.collection(collection_name)
        first = collection.find_one()

        columns: list[str] = []

        if first:
            first.pop("_id", None)
            columns = list(first.keys())

        return {
            "rows": collection.count_documents({}),
            "columns": len(columns),
            "column_names": columns,
        }

    @classmethod
    def export(cls, *, collection_name: str) -> DataFrame:
        collection = cls.collection(collection_name)
        rows = list(collection.find( {}, {"_id": 0}))

        return DataFrame(rows)

    @classmethod
    def delete_collection(cls, *, collection_name: str) -> None:
        cls.database().drop_collection(collection_name)

    @classmethod
    def count(cls, *, collection_name: str) -> int:
        return cls.collection(collection_name).count_documents({})

    @classmethod
    def exists(cls, *, collection_name: str) -> bool:
        return (collection_name in cls.database().list_collection_names())

    @classmethod
    def close(cls) -> None:
        if cls._client is not None:
            cls._client.close()
            cls._client = None