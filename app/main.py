from fastapi import FastAPI

from app.routers import urls

app = FastAPI(title="URL Shortener")

app.include_router(urls.router, prefix="/api", tags=["URLs"])
