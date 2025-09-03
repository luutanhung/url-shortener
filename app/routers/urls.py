from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, Response

from app.models import URL, URLCreate, URLRead, User
from app.services.hash_shortener import HashURLShortener

from .auth import get_current_user, get_current_user_optional

router = APIRouter()


@router.post(
    "/api/shorten",
    response_description="Shorten a URL",
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def shorten(
    url_data: URLCreate,
    user: Optional[User] = Depends(get_current_user_optional),
):
    try:
        shortener = HashURLShortener()
        result = await shortener.shorten(
            str(url_data.original_url),
            created_by=str(user.id) if user else None,
            short_code=url_data.short_code,
            expires_at=url_data.expires_at,
        )
        return {
            "success": True,
            "message": "URL shortened successfully",
            "data": URLRead(**result).model_dump(),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise e


@router.get("/{short_code}", response_description="Redirect to original URL")
async def redirect(short_code: str):
    try:
        shortener = HashURLShortener()
        original_url: str = await shortener.get_original_url(short_code)
        if not original_url:
            raise HTTPException(status_code=404, detail="URL not found")
        return RedirectResponse(url=original_url)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/urls")
async def get_urls(user: User = Depends(get_current_user)):
    """
    Retrieves all URLs created by the currently authenticated user.
    """

    urls = await URL.find({"created_by": str(user.id)}).to_list()
    return [{**url.model_dump(), "id": str(url.id)} for url in urls]


@router.delete("/api/urls/{short_code}", status_code=204)
async def delete(
    short_code: str, user: Optional[User] = Depends(get_current_user_optional)
):
    url = await URL.find_one({"short_code": short_code})
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shortened URL not found"
        )

    if url.created_by is not None and url.created_by != str(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this URL",
        )

    await url.delete()
    return Response(status_code=204)
