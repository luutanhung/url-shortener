from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.zookeeper import init_zookeeper, close_zookeeper
from app.routers import urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_zookeeper()
    yield
    # Shutdown
    close_zookeeper()


app = FastAPI(title="URL Shortener", lifespan=lifespan)

app.include_router(urls.router, tags=["URLs"])
