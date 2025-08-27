from datetime import datetime, timezone

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse

from app.zookeeper import get_next_id
from app.utils import base62encode
from app.models import URLModel, CreateURLModel
from app.database import db

router = APIRouter()


@router.post(
    "/api/shorten",
    response_description="Shorten a URL",
    response_model=URLModel,
    status_code=status.HTTP_201_CREATED,
)
async def shorten(data: CreateURLModel):
    seq_id: int = get_next_id()
    print(seq_id)
    short_code: str = base62encode(seq_id)
    url_doc = {
        "short_code": short_code,
        "original_url": str(data.url),
        "created_at": datetime.now(timezone.utc),
    }

    result = await db.urls.insert_one(url_doc)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert URL")
    url_doc["id"] = str(result.inserted_id)
    return URLModel(**url_doc)


@router.get("/{short_code}", response_description="Redirect to original URL")
async def redirect_to_url(short_code: str):
    url_doc = await db.urls.find_one({"short_code": short_code})

    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url_doc["original_url"])
