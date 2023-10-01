from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

from api.handlers import user_routrer

app = FastAPI(title="vladrunk WebApp")

main_api_router = APIRouter()

main_api_router.include_router(user_routrer, prefix="/user", tags=["user"])
app.include_router(main_api_router)

# endregion

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
