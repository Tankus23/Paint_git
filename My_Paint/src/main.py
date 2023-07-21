from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src import database
from src.pictures.router import router as router_picture
from src.pages.router import router as router_pages
from src.auth.router import router as router_auth

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Trading App"

)
# Монтируем статические файлы для обслуживания
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth",
#     tags=["Auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )
# Подключаем роутеры для различных модулей
app.include_router(router_picture)
app.include_router(router_pages)
app.include_router(router_auth)


# Определяем разрешенные источники CORS
origins = [
    "http://localhost:8000",
]

# Добавляем промежуточное ПО CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)