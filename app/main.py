import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.endpoint import menu, submenu, dish

app = FastAPI(
    title='Y_lab',
    docs_url='/'
)


origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(menu.router, tags=['Menus'], prefix='/api/v1/menus')
app.include_router(submenu.router, tags=['Submenus'], prefix='/api/v1/menus')
app.include_router(dish.router, tags=['Dishes'], prefix='/api/v1/menus')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
