from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.models import URLCreate, URLRead, User
from app.services.hash_shortener import HashURLShortener

from .auth import get_current_user_optional

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
    try:
        shortener = HashURLShortener()
        result = await shortener.shorten(
            str(url_data.original_url),
            created_by=str(user.id) if user else None,
            short_code=url_data.short_code,
            expires_at=url_data.expires_at,
        )
        return URLRead(**result)
    except ValueError as e:
        print("Validation error in URL shortening", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("Unexpected error shortening URL", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{short_code}", response_description="Redirect to original URL")
async def redirect(short_code: str):
    try:
        shortener = HashURLShortener()
        original_url: str = await shortener.get_original_url(short_code)
        if not original_url:
            raise HTTPException(status_code=404, detail="URL not found")
        return RedirectResponse(url=original_url)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
