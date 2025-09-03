import re
from typing import Literal, Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse, Response

from app.exceptions import URLDeleteNotAllowed, URLNotFound
from app.models import URL, URLCreate, URLRead, User
from app.services.hash_shortener import HashURLShortener

from .auth import get_current_user, get_current_user_optional

router = APIRouter()


@router.post(
    "/api/shorten",
    response_description="Shorten a URL",
    response_model=URLRead,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def shorten(
    url_data: URLCreate,
    user: Optional[User] = Depends(get_current_user_optional),
):
    shortener = HashURLShortener()
    return await shortener.shorten(
        str(url_data.original_url),
        created_by=str(user.id) if user else None,
        short_code=url_data.short_code,
        expires_at=url_data.expires_at,
    )


@router.get("/{short_code}", response_description="Redirect to original URL")
async def redirect(short_code: str):
    shortener = HashURLShortener()
    original_url: str = await shortener.get_original_url(short_code)
    return RedirectResponse(url=original_url)


@router.get("/api/urls")
async def get_urls(
    user: User = Depends(get_current_user),
    page: int = 1,
    limit: int = 10,
    order_by: Literal["created_at", "last_accessed", "clicks"] = "created_at",
    direction: Literal["asc", "desc"] = "desc",
    search: Optional[str] = "",
):
    """
    Retrieves all URLs created by the currently authenticated user with pagination and sorting by attributes and optional search.
    """

    skip: int = (page - 1) * limit
    short_field = order_by if direction == "asc" else f"-{order_by}"

    filter_query = {"created_by": str(user.id)}

    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        filter_query["$or"] = [
            {"short_code": regex},
            {"original_url": regex},
        ]

    total = await URL.find(filter_query).count()
    urls = (
        await URL.find(filter_query).sort(short_field).skip(skip).limit(limit).to_list()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "urls": [{**url.model_dump(), "id": str(url.id)} for url in urls],
    }


@router.delete("/api/urls/{short_code}", status_code=204)
async def delete(
    short_code: str, user: Optional[User] = Depends(get_current_user_optional)
):
    url = await URL.find_one({"short_code": short_code})
    if not url:
        raise URLNotFound(short_code)

    if url.created_by is not None and url.created_by != str(user.id):
        raise URLDeleteNotAllowed(short_code)

    await url.delete()
    return Response(status_code=204)
