from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from beanie import init_beanie


from app.database import mongodb
from app.models import URL, User
from app.routers import urls, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        mongodb.connect()
        await init_beanie(database=mongodb.get_db(), document_models=[URL, User])
        print("✅ Application startup complete")
    except Exception as e:
        print(f"❌ Application startup failed: {e}")
        raise

    yield

    await mongodb.close()
    print("✅ Application shutdown complete")


app = FastAPI(title="URL Shortener", lifespan=lifespan)

app.include_router(urls.router, tags=["URLs"])
app.include_router(users.router, tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
