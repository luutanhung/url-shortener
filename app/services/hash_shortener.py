import hashlib
import base64
from typing import Any
from datetime import datetime, timezone

from pymongo.database import Database
from pymongo import ReturnDocument


class HashURLShortener:
    def __init__(self, db: Database):
        self.db = db
        self.urls = db.urls
        self.short_length: int = 8

    async def _generate_hash_code(self, original_url: str, salt: int = 0) -> str:
        """
        Generate hash-based key with salt for collision handling
        """

        unique_string: str = f"{original_url}{salt}"
        hash_bytes = hashlib.sha256(unique_string.encode()).digest()
        base64_str = base64.urlsafe_b64encode(hash_bytes).decode()
        short_code = (
            base64_str.replace("=", "")
            .replace("+", "-")
            .replace("/", "_")[: self.short_length]
        )
        return short_code

    async def _check_collision(self, short_code: str) -> bool:
        return await self.urls.find_one({"short_code": short_code}) is not None

    async def shorten(self, original_url: str) -> dict[str, Any]:
        existing_url = await self.urls.find_one({"original_url": original_url})
        if existing_url:
            return existing_url

        salt: int = 0
        max_attempts: int = 10

        while salt < max_attempts:
            short_code: str = await self._generate_hash_code(original_url, salt)

            collision = await self._check_collision(short_code)
            if not collision:
                break

            salt += 1
        else:
            short_code: str = self._generate_hash_code(
                f"{original_url}{datetime.now().timestamp()}"
            )

        url_doc = {
            "original_url": original_url,
            "short_code": short_code,
            "created_at": datetime.now(timezone.utc),
            "clicks": 0,
            "last_accessed": None,
            "salt": salt,
        }

        result = await self.urls.insert_one(url_doc)
        url_doc["_id"] = str(result.inserted_id)
        return url_doc

    async def get_original_url(self, short_code: str) -> str | None:
        result = await self.urls.find_one_and_update(
            {"short_code": short_code},
            {
                "$inc": {"clicks": 1},
                "$set": {"last_accessed": datetime.now(timezone.utc)},
            },
            return_document=ReturnDocument.AFTER,
        )

        if result:
            return result["original_url"]
        else:
            return None
