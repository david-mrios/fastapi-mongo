# app/main.py
from fastapi import FastAPI
from app.routes.Dashboard import router as dashboard_router

app = FastAPI()

# Incluye las rutas de "Dashboard" en la aplicación
app.include_router(dashboard_router, prefix="/TecnoNic")

# Incluye las rutas de "Crud" en la aplicación
