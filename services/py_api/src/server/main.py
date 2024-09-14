from src.server.config.app_factory import create_app
from src.server.config.server_config import start

# from src.server.routes.routes import Routes
# This app is not created in the main guard as uvicorn's run method expects the app passed as an import string to
# enable 'reload' or 'workers'
app = create_app()

if __name__ == "__main__":
    start()
