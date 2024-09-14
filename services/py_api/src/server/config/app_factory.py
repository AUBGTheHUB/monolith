from fastapi import FastAPI

from src.server.routes.routes import Routes


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v3")

    Routes.register_routes(app)

    return app
