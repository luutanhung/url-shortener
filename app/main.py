from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database import mongodb
from app.routers import urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongDB
    try:
        mongodb.connect()
        print("✅ Application startup complete")
    except Exception as e:
        print(f"❌ Application startup failed: {e}")
        raise

    yield

    # Shutdown: Disconnect from MongoDB
    mongodb.close()
    print("✅ Application shutdown complete")


app = FastAPI(title="URL Shortener", lifespan=lifespan)

app.include_router(urls.router, tags=["URLs"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
