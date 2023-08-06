from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio

from app.api.v1.endpoint import dish, menu, submenu
from app.db.database import CLIENT_ORIGIN

app = FastAPI(title="Y_lab", docs_url="/")

origins = [
    CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu.router, tags=["Menus"], prefix="/api/v1/menus")
app.include_router(submenu.router, tags=["Submenus"], prefix="/api/v1/submenus")
app.include_router(dish.router, tags=["Dishes"], prefix="/api/v1/dish")


@app.on_event("startup")
async def startup_event():
    redis = asyncio.from_url(
        "redis://localhost",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
