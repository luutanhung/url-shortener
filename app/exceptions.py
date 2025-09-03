from fastapi.responses import JSONResponse


class ShortCodeAlreadyExists(Exception):
    def __init__(self, short_code: str) -> None:
        self.short_code = short_code
        super().__init__(f"Short code '{short_code}' already exists.")


class ShortenedURLNotFound(Exception):
    """Raised when a shortened URL does not exists."""

    def __init__(self, short_code: str) -> None:
        self.short_code = short_code
        super().__init__(
            f"The requested url for short code '{short_code}' does not exists."
        )


async def shortcode_exists_handler(request, exc: ShortCodeAlreadyExists):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def shortened_url_not_found_handler(request, exc: ShortenedURLNotFound):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
