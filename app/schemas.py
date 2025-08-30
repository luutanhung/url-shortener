from typing import Optional
from datetime import datetime

from typing_extensions import Annotated
from pydantic import BaseModel, Field, HttpUrl
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class URLBase(BaseModel):
    id: Optional[PyObjectId] = Field(default=None)
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    clicks: int
    last_accessed: datetime | None
    salt: int


class URLCreate(BaseModel):
    original_url: HttpUrl
