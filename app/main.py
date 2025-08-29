from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(title="URL Shortener", lifespan=lifespan)

app.include_router(urls.router, tags=["URLs"])
