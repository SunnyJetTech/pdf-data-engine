from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from core.config import settings

client = MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully")
except ConnectionFailure:
    print("MongoDB connection failed")

mongodb = client[settings.MONGO_DATABASE]