# app/config.py
from pymongo import MongoClient
from dotenv import load_dotenv  # Cargar dotenv
import os
# Cargar el archivo .env ubicado en el nivel principal
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Usar la variable de entorno para la conexión
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(CONNECTION_STRING)
db = client["TecnoNic"]
