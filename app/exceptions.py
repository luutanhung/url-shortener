from fastapi.responses import JSONResponse


class ShortCodeAlreadyExists(Exception):
    def __init__(self, short_code: str):
        self.short_code = short_code
        super().__init__(f"Short code '{short_code}' already exists")


async def shortcode_exists_handler(request, exc: ShortCodeAlreadyExists):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
