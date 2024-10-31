from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

# Definimos un tipo personalizado para el ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Definimos el modelo de datos
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = False

class Question(BaseModel):
    Respuesta: str
    pregunta_id: PyObjectId = Field(..., alias="pregunta_id")  # Alias opcional para compatibilidad con MongoDB

    class Config:
        json_encoders = {ObjectId: str}  # Esto convierte el ObjectId a string al devolverlo en JSON
