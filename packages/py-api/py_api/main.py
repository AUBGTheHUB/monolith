from uvicorn import run
from fastapi import FastAPI

from py_api.middleware import AuthMiddleware
from py_api.routes import Routes

app = FastAPI()
AuthMiddleware(app)
Routes(app)


def start():
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)
