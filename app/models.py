from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import datetime
from pydantic_core import CoreSchema, core_schema
from typing import Any, List, Annotated


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            raise ValueError("Invalid ObjectId")
        return ObjectId(str(v))

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x),
                return_schema=core_schema.str_schema(),
            ),
        )


PydanticObjectId = Annotated[PyObjectId, None]


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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Pregunta: str
    Cliente: Cliente

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class Producto(BaseModel):
    Cantidad: int
    Nombre: str
    PrecioUnitario: float


class CarritoCompras(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FechaCreacion: datetime
    Cliente: Cliente
    Productos: List[Producto]

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        arbitrary_types_allowed = True


class ComentariosValoraciones(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FechaCreacion: datetime
    Razon: str
    Cliente: Cliente
    Productos: List[Producto]

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        arbitrary_types_allowed = True


class RecomendacionProducto(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FechaComentario: datetime
    Comentario: str
    Valoracion: float
    Cliente: Cliente
    Productos: List[Producto]

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        arbitrary_types_allowed = True
