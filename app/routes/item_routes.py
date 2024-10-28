# app/routes/item_routes.py
from fastapi import APIRouter, HTTPException
from app.config import db
from app.models import Item
from typing import List

router = APIRouter()

@router.post("/items/insert", response_model=Item)
def create_item(item: Item):
    collection = db["items"]
    result = collection.insert_one(item.dict())
    if result.inserted_id:
        return item
    raise HTTPException(status_code=400, detail="Error al insertar un registro")

@router.get("/items", response_model=List[Item])
def read_items():
    collection = db["items"]
    items = list(collection.find())
    return items

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str):
    collection = db["items"]    
    item = collection.find_one({"_id": item_id})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

@router.delete("/items/{item_id}")
def delete_item(item_id: str):
    collection = db["items"]
    result = collection.delete_one({"_id": item_id})
    if result.deleted_count == 1:
        return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item no encontrado")
