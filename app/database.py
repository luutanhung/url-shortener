import os
from typing import Optional

from pymongo import AsyncMongoClient
from pymongo.database import Database
from pymongo.errors import (
    ConnectionFailure,
    ConfigurationError,
)
from dotenv import load_dotenv

load_dotenv()


class MongoDBConnection:
    def __init__(self):
        self.client: Optional[AsyncMongoClient] = None
        self.db: Optional[Database] = None

    def connect(self) -> None:
        try:
            mongo_uri: str = os.getenv("MONGO_URI", "mongo://0.0.0.0:27017")
            database: str = os.getenv("DATABASE", "url_shortener")

            self.client = AsyncMongoClient(mongo_uri)
            self.db = self.client[database]
            print(f"Successfully connected to MongoDB: {database}")

        except (ConnectionFailure, ConfigurationError) as e:
            print(f"MongoDB connection failed: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error connection to MongoDB: {e}")
            raise

    def close(self) -> None:
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

    def get_database(self) -> Database:
        if not self.client:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db


mongodb = MongoDBConnection()


def get_db() -> Database:
    try:
        return mongodb.get_database()
    except Exception as e:
        print(f"Database session error: {e}")
        raise
