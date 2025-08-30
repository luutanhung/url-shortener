from typing import Optional
from datetime import datetime, timezone
from bson.objectid import ObjectId

from pydantic import HttpUrl, Field
from beanie import Document


class URL(Document):
    short_code: str
    original_url: HttpUrl
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    clicks: int = 0
    last_accessed: Optional[datetime] = None
    salt: int

    class Settings:
        name = "urls"

    model_config = {"json_encoders": {ObjectId: str}}
