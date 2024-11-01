from fastapi import APIRouter, HTTPException, status
from app.config import db
from app.models import FAQ, Pregunta, CarritoCompras, ComentariosValoraciones, RecomendacionProducto
from typing import List
from bson import ObjectId

router = APIRouter()

### FAQ CRUD Operations

# Create FAQ
@router.post("/FAQ", response_model=FAQ)
def create_FAQ(faq: FAQ):
    collection = db["FAQ"]
    result = collection.insert_one(faq.dict(by_alias=True))
    if result.inserted_id:
        return faq
    raise HTTPException(status_code=400, detail="Error al insertar FAQ")

# Read All FAQs
@router.get("/FAQ", response_model=List[FAQ])
def read_FAQs():
    collection = db["FAQ"]
    items = list(collection.find())
    return items

# Read Single FAQ
@router.get("/FAQ/{faq_id}", response_model=FAQ)
def read_FAQ(faq_id: str):
    collection = db["FAQ"]
    item = collection.find_one({"_id": ObjectId(faq_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="FAQ no encontrada")

# Delete FAQ
@router.delete("/FAQ/{faq_id}")
def delete_FAQ(faq_id: str):
    collection = db["FAQ"]
    result = collection.delete_one({"_id": ObjectId(faq_id)})
    if result.deleted_count == 1:
        return {"detail": "FAQ eliminada"}
    raise HTTPException(status_code=404, detail="FAQ no encontrada")


### Pregunta CRUD Operations

# Create Pregunta
@router.post("/Pregunta", response_model=Pregunta)
def create_Pregunta(pregunta: Pregunta):
    collection = db["Pregunta"]
    result = collection.insert_one(pregunta.dict(by_alias=True))
    if result.inserted_id:
        return pregunta
    raise HTTPException(status_code=400, detail="Error al insertar Pregunta")

# Read All Preguntas
@router.get("/Pregunta", response_model=List[Pregunta])
def read_Preguntas():
    collection = db["Pregunta"]
    items = list(collection.find())
    return items

# Read Single Pregunta
@router.get("/Pregunta/{pregunta_id}", response_model=Pregunta)
def read_Pregunta(pregunta_id: str):
    collection = db["Pregunta"]
    item = collection.find_one({"_id": ObjectId(pregunta_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Pregunta no encontrada")

# Delete Pregunta
@router.delete("/Pregunta/{pregunta_id}")
def delete_Pregunta(pregunta_id: str):
    collection = db["Pregunta"]
    result = collection.delete_one({"_id": ObjectId(pregunta_id)})
    if result.deleted_count == 1:
        return {"detail": "Pregunta eliminada"}
    raise HTTPException(status_code=404, detail="Pregunta no encontrada")


### CarritoCompras CRUD Operations

# Create CarritoCompras
@router.post("/CarritoCompras", response_model=CarritoCompras)
def create_CarritoCompras(carrito: CarritoCompras):
    collection = db["CarritoCompras"]
    result = collection.insert_one(carrito.dict(by_alias=True))
    if result.inserted_id:
        return carrito
    raise HTTPException(status_code=400, detail="Error al insertar Carrito de Compras")

# Read All CarritoCompras
@router.get("/CarritoCompras", response_model=List[CarritoCompras])
def read_CarritoCompras():
    collection = db["CarritoCompras"]
    items = list(collection.find())
    return items

# Read Single CarritoCompras
@router.get("/CarritoCompras/{carrito_id}", response_model=CarritoCompras)
def read_CarritoCompras_single(carrito_id: str):
    collection = db["CarritoCompras"]
    item = collection.find_one({"_id": ObjectId(carrito_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Carrito de Compras no encontrado")

# Delete CarritoCompras
@router.delete("/CarritoCompras/{carrito_id}")
def delete_CarritoCompras(carrito_id: str):
    collection = db["CarritoCompras"]
    result = collection.delete_one({"_id": ObjectId(carrito_id)})
    if result.deleted_count == 1:
        return {"detail": "Carrito de Compras eliminado"}
    raise HTTPException(status_code=404, detail="Carrito de Compras no encontrado")


### ComentariosValoraciones CRUD Operations

# Create ComentariosValoraciones
@router.post("/ComentariosValoraciones", response_model=ComentariosValoraciones)
def create_ComentariosValoraciones(comentario: ComentariosValoraciones):
    collection = db["ComentariosValoraciones"]
    result = collection.insert_one(comentario.dict(by_alias=True))
    if result.inserted_id:
        return comentario
    raise HTTPException(status_code=400, detail="Error al insertar Comentario/Valoración")

# Read All ComentariosValoraciones
@router.get("/ComentariosValoraciones", response_model=List[ComentariosValoraciones])
def read_ComentariosValoraciones():
    collection = db["ComentariosValoraciones"]
    items = list(collection.find())
    return items

# Read Single Comentario/Valoración
@router.get("/ComentariosValoraciones/{comentario_id}", response_model=ComentariosValoraciones)
def read_Comentario(comentario_id: str):
    collection = db["ComentariosValoraciones"]
    item = collection.find_one({"_id": ObjectId(comentario_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Comentario/Valoración no encontrado")

# Delete Comentario/Valoración
@router.delete("/ComentariosValoraciones/{comentario_id}")
def delete_Comentario(comentario_id: str):
    collection = db["ComentariosValoraciones"]
    result = collection.delete_one({"_id": ObjectId(comentario_id)})
    if result.deleted_count == 1:
        return {"detail": "Comentario/Valoración eliminado"}
    raise HTTPException(status_code=404, detail="Comentario/Valoración no encontrado")


### RecomendacionProducto CRUD Operations

# Create RecomendacionProducto
@router.post("/RecomendacionProducto", response_model=RecomendacionProducto)
def create_RecomendacionProducto(recomendacion: RecomendacionProducto):
    collection = db["RecomendacionProducto"]
    result = collection.insert_one(recomendacion.dict(by_alias=True))
    if result.inserted_id:
        return recomendacion
    raise HTTPException(status_code=400, detail="Error al insertar Recomendación de Producto")

# Read All RecomendacionProducto
@router.get("/RecomendacionProducto", response_model=List[RecomendacionProducto])
def read_RecomendacionesProducto():
    collection = db["RecomendacionProducto"]
    items = list(collection.find())
    return items

# Read Single RecomendacionProducto
@router.get("/RecomendacionProducto/{recomendacion_id}", response_model=RecomendacionProducto)
def read_RecomendacionProducto(recomendacion_id: str):
    collection = db["RecomendacionProducto"]
    item = collection.find_one({"_id": ObjectId(recomendacion_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Recomendación no encontrada")

# Delete RecomendacionProducto
@router.delete("/RecomendacionProducto/{recomendacion_id}")
def delete_RecomendacionProducto(recomendacion_id: str):
    collection = db["RecomendacionProducto"]
    result = collection.delete_one({"_id": ObjectId(recomendacion_id)})
    if result.deleted_count == 1:
        return {"detail": "Recomendación eliminada"}
    raise HTTPException(status_code=404, detail="Recomendación no encontrada")
