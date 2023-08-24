# isort: skip_file
from fastapi import APIRouter, FastAPI
from uvicorn import run
from py_api.routes import Routes
from py_api.middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()


router = APIRouter(prefix='/v2')
Routes.bind(router)

origins = ['*']

app = FastAPI()
AuthMiddleware.bind(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


def start() -> None:
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)


if __name__ == "__main__":
    start()
