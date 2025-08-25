import string
import random
from datetime import datetime

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse

from app.models import URLModel, CreateURLModel
from app.database import db

router = APIRouter()


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@router.post(
    "/shorten",
    response_description="Shorten a URL",
    response_model=URLModel,
    status_code=status.HTTP_201_CREATED,
)
async def shorten_url(data: CreateURLModel):
    short_code: str = generate_short_code()
    url_doc = {
        "short_code": short_code,
        "original_url": str(data.url),
        "created_at": datetime.utcnow(),
    }

    result = await db.urls.insert_one(url_doc)
    url_doc["id"] = str(result.inserted_id)
    return URLModel(**url_doc)


@router.get("/{short_code}", response_description="Redirect to original URL")
async def redirect_to_url(short_code: str):
    url_doc = await db.urls.find_one({"short_code": short_code})

    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url_doc["original_url"])
