from fastapi import APIRouter, FastAPI
from py_api.middleware import AuthMiddleware
from py_api.routes import Routes
from uvicorn import run

router = APIRouter(prefix='/v2')
Routes.bind(router)

app = FastAPI()
AuthMiddleware.bind(app)
app.include_router(router)


def start() -> None:
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)
