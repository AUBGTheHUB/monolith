from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from py_api.environment import IS_OFFLINE, SSL_FILES
from py_api.middleware import Middleware
from py_api.routes import Routes
from py_api.utilities.logging import get_log_config
from uvicorn import run

origins = ['*']

main_app = FastAPI()
app = FastAPI()

Routes.bind(app)
Middleware.bind(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.mount("/v2", app)


def start() -> None:
    run(
        "py_api.main:main_app", host="0.0.0.0", port=6969,
        reload=True if IS_OFFLINE else False,
        log_config=get_log_config(), **SSL_FILES if not IS_OFFLINE else {},
    )


if __name__ == "__main__":
    start()
