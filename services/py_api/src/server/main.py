from src.server.config.app_factory import create_app
from src.server.config.server_config import start, load_server_config

# This app is not created in the main guard as uvicorn's run method expects the app passed as an import string to
# enable 'reload' or 'workers'
app = create_app()

if __name__ == "__main__":
    server_config = load_server_config()
    start(server_config)
