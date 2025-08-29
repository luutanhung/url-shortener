from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pymongo.database import Database

from app.database import get_db
from app.services.hash_shortener import HashURLShortener
from app.models import CreateURL, URLModel

router = APIRouter()


@router.post(
    "/api/shorten",
    response_description="Shorten a URL",
    response_model=URLModel,
    status_code=status.HTTP_201_CREATED,
)
async def shorten(url_data: CreateURL, db: Database = Depends(get_db)):
    try:
        shortener = HashURLShortener(db)
        result = await shortener.shorten(str(url_data.original_url))
        return URLModel(**result)
    except ValueError as e:
        print("Validation error in URL shortening", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("Unexpected error shortening URL", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{short_code}", response_description="Redirect to original URL")
async def redirect(short_code: str, db: Database = Depends(get_db)):
    try:
        shortener = HashURLShortener(db)
        original_url: str = await shortener.get_original_url(short_code)
        if not original_url:
            raise HTTPException(status_code=404, detail="URL not found")
        return RedirectResponse(url=original_url)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
