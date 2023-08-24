from fastapi import FastAPI
from py_api.middleware import AuthMiddleware
from py_api.routes import Routes
from uvicorn import run

app = FastAPI()
AuthMiddleware.bind(app)
Routes.bind(app)


def start() -> None:
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)
