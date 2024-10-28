# app/main.py
from fastapi import FastAPI
from app.routes.item_routes import router as item_router

app = FastAPI()

# Incluye las rutas de "items" en la aplicación
app.include_router(item_router, prefix="/items")
