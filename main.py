from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

from api.handlers import user_routrer


# Создаем экземпляр FastAPI, устанавливаем заголовок приложения
app = FastAPI(title="vladrunk WebApp")

# Создаем APIRouter для основного маршрута
main_api_router = APIRouter()

# Включаем APIRouter для пользователей, добавляя префикс "/user" и тег "user"
main_api_router.include_router(user_routrer, prefix="/user", tags=["user"])
# Включаем основной APIRouter в наше приложение
app.include_router(main_api_router)

# region Main
if __name__ == "__main__":
    # Запускаем приложение, используя сервер Uvicorn, на хосте "0.0.0.0" и порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
# endregion
