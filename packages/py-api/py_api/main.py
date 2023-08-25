import pathlib
from os import getenv

from dotenv import load_dotenv
from py_api.utilities.parsers import eval_bool  # noqa

load_dotenv()  # noqa
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from py_api.middleware import AuthMiddleware
from py_api.middleware.exception_handler import ExceptionHandler
from py_api.routes import Routes
from uvicorn import run

router = APIRouter(prefix='/v2')
Routes.bind(router)

origins = ['*']

app = FastAPI()

AuthMiddleware.bind(app)
ExceptionHandler.bind(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


prod_log_config = {}

cwd = pathlib.Path(__file__).parent.resolve()
prod_log_config = {"log_config": f"{cwd}/log.ini"}


def start() -> None:

    run(
        "py_api.main:app", host="0.0.0.0", port=6969, reload=True,
        *prod_log_config if not eval_bool(getenv("IS_OFFLINE", False)) else {}
    )


if __name__ == "__main__":
    start()
