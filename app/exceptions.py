from fastapi.responses import JSONResponse


class ShortCodeAlreadyExists(Exception):
    def __init__(self, short_code: str) -> None:
        super().__init__(f"Short code '{short_code}' already exists.")


class URLNotFound(Exception):
    """Raised when a shortened URL does not exists."""

    def __init__(self, short_code: str) -> None:
        super().__init__(
            f"The requested url for short code '{short_code}' does not exists."
        )


class URLDeleteNotAllowed(Exception):
    """Raises when a user is not authorized to delete a URL."""

    def __init__(self, short_code: str) -> None:
        super().__init__(
            f"You don't have enough permissions to delte this url associated with short code '{short_code}'"
        )


class UsernameAlreadyTaken(Exception):
    """Raises when a username is already taken by another user."""

    def __init__(self, username: str) -> None:
        super().__init__(
            f"Username '{username}' is already taken. Please use another username."
        )


async def shortcode_exists_handler(request, exc: ShortCodeAlreadyExists):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def url_not_found_handler(request, exc: URLNotFound):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def url_delete_not_allowed_handler(request, exc: URLDeleteNotAllowed):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


async def username_already_taken_handler(request, exc: UsernameAlreadyTaken):
    return JSONResponse(status_code=400, content={"detail", str(exc)})
