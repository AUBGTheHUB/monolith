from fastapi import FastAPI
from py_api.middleware import AuthMiddleware
from py_api.routes import Routes
from uvicorn import run

"""
    Currently, environment variables are loaded initially in the file
    packages/py-api/py_api/database/initialize.py.

    If, due to any reason, you require all custom environment variables
    to be set before initializing the database module, you should relocate
    the 'load_dotenv' invocation to a different location.

    It's important to note that we are intentionally not placing it at the
    top level in the main.py file.
    This decision is in line with the styling rules of autopep
    and follows the PEP guidelines for consistency.
"""

app = FastAPI()
AuthMiddleware.bind(app)
Routes.bind(app)


def start() -> None:
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)
