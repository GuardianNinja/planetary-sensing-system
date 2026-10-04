# src/runtime/api.py
from fastapi import FastAPI
from .api import routes

def mount_routes(app: FastAPI) -> None:
    routes.register_intent_routes(app)
