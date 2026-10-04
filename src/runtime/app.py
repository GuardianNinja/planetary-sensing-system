# src/runtime/app.py
from fastapi import FastAPI
from .api import api

def create_app() -> FastAPI:
    app = FastAPI(title="Governed HI Runtime", version="1.0.0")
    api.mount_routes(app)
    return app

app = create_app()
