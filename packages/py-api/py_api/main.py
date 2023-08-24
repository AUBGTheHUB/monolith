from fastapi import APIRouter, FastAPI
from py_api.middleware import AuthMiddleware
from py_api.routes import Routes
from uvicorn import run

router = APIRouter(prefix='/v2')
AuthMiddleware.bind(router)
Routes.bind(router)

app = FastAPI()
app.include_router(router)


def start() -> None:
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)
