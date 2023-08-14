from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio

from app.api.v1.endpoint import data, dish, menu, submenu
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

app.include_router(
    menu.router,
    prefix="/api/v1/menus",
    tags=["menus"],
)
app.include_router(
    submenu.router,
    prefix="/api/v1/menus/{target_menu_id}/submenus",
    tags=["submenus"],
)
app.include_router(
    dish.router,
    prefix="/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    tags=["dishes"],
)
app.include_router(
    data.router,
    prefix="/api/v1/get-linked-list",
    tags=["collected information"],
)


@app.on_event("startup")
async def startup_event():
    redis = asyncio.from_url(
        "redis://localhost",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
