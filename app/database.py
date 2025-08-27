import os

from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

print("MONGO_URI", os.getenv("MONGO_URI"))

client = AsyncMongoClient(os.getenv("MONGO_URI", "mongodb://mongodb:27017"))
db = client[os.getenv("DATABASE_NAME", "url_shortener")]
