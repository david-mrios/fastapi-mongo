from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

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
class FAQ(BaseModel):
    Respuesta: str
    pregunta_id: PyObjectId = Field(..., alias="pregunta_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class Cliente(BaseModel):
    Nombre: str
    Correo: EmailStr
    Direccion: str

class Pregunta(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Pregunta: str
    Cliente: Cliente

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class Producto(BaseModel):
    Cantidad: int
    Nombre: str
    PrecioUnitario: float

class CarritoCompras(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FechaCreacion: datetime
    Cliente: Cliente
    Productos: List[Producto]

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        arbitrary_types_allowed = True

class ComentariosValoraciones(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FechaCreacion: datetime
    Razon: str
    Cliente: Cliente
    Productos: List[Producto]

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        arbitrary_types_allowed = True

class RecomendacionProducto(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FechaComentario: datetime
    Comentario: str
    Valoracion: float
    Cliente: Cliente
    Productos: List[Producto]

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        arbitrary_types_allowed = True
