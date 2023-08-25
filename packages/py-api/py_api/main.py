from dotenv import load_dotenv  # noqa

load_dotenv()  # noqa
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from py_api.middleware import AuthMiddleware
from py_api.middleware.exception_handler import ExceptionHandler
from py_api.routes import Routes
from uvicorn import run

origins = ['*']

main_app = FastAPI()
app = FastAPI()

Routes.bind(app)
AuthMiddleware.bind(app)
ExceptionHandler.bind(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.mount("/v2", app)


def start() -> None:
    run("py_api.main:main_app", host="0.0.0.0", port=6969, reload=True)


if __name__ == "__main__":
    start()
