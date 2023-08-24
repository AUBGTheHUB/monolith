from uvicorn import run
from fastapi import FastAPI

from py_api.middleware import AuthMiddleware 

app = FastAPI()
AuthMiddleware(app)

@app.get('/health')
async def root():
    return {"message": "Hello World"}

def start():
    run("py_api.main:app", host="0.0.0.0", port=6969, reload=True)