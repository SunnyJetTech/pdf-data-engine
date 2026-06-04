from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from core.config import settings
from pymongo import MongoClient
from pymongo.synchronous.mongo_client import MongoClient as MongoClientType

client: MongoClientType = MongoClient(settings.MONGO_URL)
try:
    client.admin.command("ping")
    print("MongoDB connected successfully")
except ConnectionFailure:
    print("MongoDB connection failed")

mongo_db = client[settings.MONGO_DATABASE]
client = MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)