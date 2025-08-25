import os

from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

client = AsyncMongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DATABASE_NAME")]
