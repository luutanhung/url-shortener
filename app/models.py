from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class URLModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    short_code: str
    original_url: HttpUrl
    created_at: datetime


class CreateURLModel(BaseModel):
    url: HttpUrl
