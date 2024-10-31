# app/main.py
from fastapi import FastAPI
from app.routes.Dashboard import router as router

app = FastAPI()

# Incluye las rutas de "items" en la aplicación
app.include_router(router, prefix="/TecnoNic")
