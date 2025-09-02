from datetime import datetime, timezone
from typing import Optional

from beanie import Document, PydanticObjectId
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, HttpUrl, field_serializer


class URL(Document):
    short_code: str
    original_url: HttpUrl
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    clicks: int = 0
    last_accessed: Optional[datetime] = None
    salt: int
    created_by: Optional[str] = None
    expires_at: datetime | None = None

    class Settings:
        name = "urls"

    model_config = {"json_encoders": {ObjectId: str}}


class URLRead(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    clicks: int
    last_accessed: datetime | None
    salt: int
    created_by: Optional[str]
    expires_at: Optional[datetime]

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PydanticObjectId: str,
        },
    }

    @field_serializer("id")
    def serialize_id(self, id: PydanticObjectId, _info):
        return str(id)


class URLCreate(BaseModel):
    original_url: HttpUrl
    short_code: str | None = None
    expires_at: datetime | None = None
