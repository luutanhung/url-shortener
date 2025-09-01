import base64
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import HTTPException
from pymongo import ReturnDocument
from pymongo.database import Database

from app.models import URL


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

    async def shorten(
        self,
        original_url: str,
        created_by: Optional[str],
        short_code: str = None,
        expires_at: datetime = None,
    ) -> dict[str, Any]:
        if created_by:
            if existing_url := await URL.find_one(
                {"original_url": original_url, "created_by": created_by}
            ):
                return existing_url.model_dump()
        else:
            if existing_url := await URL.find_one(
                {"original_url": original_url, "created_by": None}
            ):
                return existing_url.model_dump()

        if short_code is not None:
            existing_code = URL.find_one({"short_code": short_code})
            if existing_code:
                raise HTTPException(status_code=400, detail="Short code already exists")

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

        expires_at = expires_at or (datetime.now(timezone.utc) + timedelta(days=1))

        url_doc = URL(
            original_url=original_url,
            short_code=short_code,
            created_at=datetime.now(timezone.utc),
            clicks=0,
            last_accessed=None,
            salt=salt,
            created_by=created_by,
            expires_at=expires_at,
        )

        await url_doc.insert()
        return url_doc.model_dump()

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
