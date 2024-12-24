from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.database.db_manager import get_db_manager
from src.server.routes.routes import Routes
from src.server.middleware.middleware import Middleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    To learn more about lifespan events, visit:
    https://fastapi.tiangolo.com/advanced/events/#lifespan

    To learn more about context managers, visit:
    https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager
    """
    yield
    # We ignore the error as we know that the client is initialized
    _ = get_db_manager().close_all_connections()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, root_path="/api/v3")

    Routes.register_routes(app)
    Middleware.bind(app)

    return app
