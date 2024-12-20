from fastapi import APIRouter, HTTPException, status, Query
from app.config import db
from app.models import FAQ, Pregunta, CarritoCompras, ComentariosValoraciones, RecomendacionProducto
from typing import List, Dict, Any, Optional
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()


@router.get("/recomendacion-producto-test")
async def obtener_recomendaciones():
    try:
        # Consulta a MongoDB
        collection = db["RecomendacionProducto"]
        resultados = collection.find({
            "Cliente.Correo": {
                "$regex": "@example.com$",
                "$options": "i"
            },
            "Productos": {
                "$elemMatch": {
                    "PrecioUnitario": {"$lt": 50}
                }
            }
        })

        recomendaciones = []
        for doc in resultados:
            doc["_id"] = str(doc["_id"])  # Convertimos ObjectId a string
            recomendaciones.append(doc)
        if not recomendaciones:
            raise HTTPException(
                status_code=404, detail="No se encontraron recomendaciones.")

        return recomendaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recomendacion-producto-test-valoracion")
async def obtener_recomendaciones_valoracion():
    try:
        # Consulta a MongoDB
        collection = db["RecomendacionProducto"]
        resultados = collection.find({
            "Valoracion": {"$gt": 2}
        }).sort([("FechaComentario", -1)]).limit(2)

        recomendaciones = []
        for doc in resultados:
            doc["_id"] = str(doc["_id"])  # Convertimos ObjectId a string
            recomendaciones.append(doc)
        if not recomendaciones:
            raise HTTPException(
                status_code=404, detail="No se encontraron recomendaciones.")

        return recomendaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/CarritoComprasTest/buscar")
async def buscar_carritos(
    precio: Optional[float] = Query(
        None, description="Precio del producto en el carrito"),
    correo: Optional[str] = Query(
        None, description="Correo del cliente asociado al carrito")
):
    try:
        collection = db["CarritoCompras"]
        query = {"$or": []}  # Usar $or para combinar condiciones

        # Filtrar por correo si está presente
        if correo:
            query["$or"].append(
                {"Cliente.Correo": {"$regex": correo, "$options": "i"}})

        # Filtrar productos con precio exacto si está presente
        if precio is not None:
            query["$or"].append(
                {"Productos": {"$elemMatch": {"PrecioUnitario": precio}}})

        # Si no se especifica ningún filtro, devolver todos los carritos
        if not query["$or"]:
            return list(collection.find())  # Devuelve todos los carritos

        carritos = list(collection.find(query))

        # Convertir ObjectId a string para cada carrito (si se utiliza el _id)
        for carrito in carritos:
            carrito["_id"] = str(carrito["_id"])

        # Si no se encontraron carritos, retornar un mensaje adecuado
        if not carritos:
            raise HTTPException(
                status_code=404, detail="No se encontraron carritos con los filtros especificados"
            )

        return carritos

    except Exception as e:
        # Manejo de excepciones en caso de error
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Helper para serializar ObjectId
def serialize_document(document):
    document["_id"] = str(document["_id"])  # Convertir ObjectId a string
    if "pedido" in document and "_id_pedido" in document["pedido"]:
        document["pedido"]["_id_pedido"] = str(
            document["pedido"]["_id_pedido"])  # Convertir ObjectId en pedido
    # Conversión de ObjectId para cualquier campo adicional que requiera serialización
    if "preguntas" in document:
        document["preguntas"] = [str(p) if isinstance(
            p, ObjectId) else p for p in document["preguntas"]]
    if "respuestas" in document:
        for respuesta in document["respuestas"]:
            respuesta["_id"] = str(respuesta["_id"])
            if "pregunta_id" in respuesta:
                respuesta["pregunta_id"] = str(respuesta["pregunta_id"])
    return document

# 1. Agrupar comentarios y valoraciones por razones y fecha de creación
@router.get("/ComentariosValoraciones/agrupar_por_razon_fecha")
async def agrupar_comentarios_por_razon_fecha():
    try:
        collection = db["ComentariosValoraciones"]
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "Razon": "$Razon",
                        "FechaCreacion": {
                            "$dateToString": {"format": "%Y-%m-%d", "date": "$FechaCreacion"}
                        }
                    },
                    "comentarios": {"$push": "$$ROOT"}
                }
            }
        ]
        resultado = list(collection.aggregate(pipeline))

        # Serializamos cada documento del resultado
        for doc in resultado:
            # Convertir ObjectId en _id.Razon si es necesario
            doc["_id"]["Razon"] = str(doc["_id"]["Razon"])
            doc["comentarios"] = [serialize_document(
                comentario) for comentario in doc["comentarios"]]

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )

# 2. Obtener los productos más vendidos en la colección de pedidos
@router.get("/Pedido/productos_mas_vendidos")
async def productos_mas_vendidos():
    try:
        collection = db["Pedido"]
        pipeline = [
            {"$unwind": "$Productos"},
            {"$group": {
                "_id": "$Productos.Nombre",
                "total_vendidos": {"$sum": "$Productos.Cantidad"}
            }},
            {"$project": {"_id": 1, "total_vendidos": 1}},
            {"$sort": {"total_vendidos": -1}},
            {"$limit": 10}
        ]
        resultado = list(collection.aggregate(pipeline))
        return [serialize_document(doc) for doc in resultado]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")

# 3. Listar clientes con más preguntas en el FAQ y sus respectivas preguntas y respuestas
@router.get("/FAQ/clientes_mas_preguntas")
async def clientes_mas_preguntas():
    try:
        collection_pregunta = db["Pregunta"]
        collection_faq = db["FAQ"]
        pipeline = [
            {"$group": {
                "_id": "$Cliente.Correo",
                "total_preguntas": {"$sum": 1},
                "preguntas": {"$push": "$_id"}
            }},
            {"$sort": {"total_preguntas": -1}},
            {"$project": {
                "_id": 1,
                "total_preguntas": 1,
                "preguntas": 1
            }}

        ]
        clientes = list(collection_pregunta.aggregate(pipeline))

        for cliente in clientes:
            # Convertir ObjectId de las preguntas antes de hacer la consulta
            cliente["preguntas"] = [str(pregunta_id)
                                    for pregunta_id in cliente["preguntas"]]

            cliente["respuestas"] = list(collection_faq.find(
                {"pregunta_id": {
                    "$in": [ObjectId(pregunta) for pregunta in cliente["preguntas"]]}}
            ))

            # Serializar cada respuesta para convertir _id de ObjectId a string
            cliente["respuestas"] = [serialize_document(
                resp) for resp in cliente["respuestas"]]

        # Serializar cada cliente para convertir cualquier ObjectId
        return [serialize_document(cliente) for cliente in clientes]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )

# 4. Buscar productos con una valoración igual o mayor a un valor específico en la colección RecomendacionProducto
@router.get("/RecomendacionProducto/productos_por_valoracion")
async def productos_por_valoracion(valoracion: float):
    try:
        collection = db["RecomendacionProducto"]
        query = {"Valoracion": {"$gte": valoracion}}
        productos = list(collection.find(query))
        return [serialize_document(prod) for prod in productos]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")

# 5. Filtrar historial de compras por fecha y cliente
@router.get("/HistorialCompras/filtrar")
async def filtrar_historial(correo: Optional[str] = None, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
    try:
        # Colección de HistorialCompras
        collection_historial = db["HistorialCompras"]

        # Construir la consulta
        query = {}

        # Filtrar por correo del cliente si se proporciona
        if correo:
            query["Cliente.Correo"] = {"$regex": correo, "$options": "i"}

        # Filtrar por rango de fechas si se proporciona
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
                fecha_fin_dt = datetime.fromisoformat(fecha_fin)
                query["FechaCreacion"] = {
                    "$gte": fecha_inicio_dt, "$lte": fecha_fin_dt}
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Formato de fecha incorrecto. Debe ser ISO 8601.")

        # Buscar en la colección HistorialCompras con el filtro construido
        historial_compras = list(collection_historial.find(query))

        # Serializar los resultados y devolver
        return [serialize_document(historial) for historial in historial_compras]

    except Exception as e:
        # Enviar mensaje de error detallado si ocurre una excepción
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )

# 6. Obtener productos de carrito de compras por rango de precio
@router.get("/CarritoCompras/productos_por_rango_precio")
async def productos_por_rango_precio(min_precio: float, max_precio: float):
    try:
        collection = db["CarritoCompras"]
        pipeline = [
            {"$unwind": "$Productos"},
            {"$match": {
                "Productos.PrecioUnitario": {"$gte": min_precio, "$lte": max_precio}
            }},
            {"$group": {
                "_id": "$_id",
                "Cliente": {"$first": "$Cliente"},
                "Productos": {"$push": "$Productos"}
            }}
        ]
        carritos = list(collection.aggregate(pipeline))
        return [serialize_document(carrito) for carrito in carritos]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")

# 7. Listar pedidos por cliente y rango de fecha de creación
@router.get("/Pedido/filtrar_por_cliente_fecha")
async def pedidos_por_cliente_fecha(correo: Optional[str] = None, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
    try:
        # Colección de HistorialCompras
        collection_historial = db["HistorialCompras"]

        # Query base
        query = {}

        # Si se pasa el correo, se busca por ese campo en los registros de HistorialCompras
        if correo:
            query["Cliente.Correo"] = {"$regex": correo, "$options": "i"}

        # Si se pasa el rango de fechas, filtramos también por las fechas de creación
        if fecha_inicio and fecha_fin:
            query["FechaCreacion"] = {
                "$gte": datetime.fromisoformat(fecha_inicio),
                "$lte": datetime.fromisoformat(fecha_fin)
            }

        # Buscar registros en HistorialCompras que coincidan con el filtro
        historial_compras = list(collection_historial.find(query))

        # Si no hay resultados, devolver una lista vacía
        if not historial_compras:
            return []

        # Si encontramos un historial, extraemos los _id_pedido correspondientes
        pedido_ids = [historial["pedido"]["_id_pedido"]
                      for historial in historial_compras]

        # Ahora buscar en la colección Pedido, usando los _id_pedido encontrados
        collection_pedido = db["Pedido"]
        pedidos = list(collection_pedido.find({"_id": {"$in": pedido_ids}}))

        return [serialize_document(pedido) for pedido in pedidos]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/ComentariosValoraciones/contar_por_satisfaccion")
async def contar_por_satisfaccion():
    try:
        collection = db["RecomendacionProducto"]

        # Pipeline para agrupar por rango de la valoración
        pipeline = [
            {
                "$bucket": {
                    "groupBy": "$Valoracion",  # Agrupar por valoracion numérica
                    # Rango de satisfacción: [0-2, 2-4, 4-5]
                    "boundaries": [0, 2, 4, 5],
                    "default": "Sin clasificar",  # Valor predeterminado para fuera de rango
                    "output": {
                        # Contar la cantidad de registros en cada grupo
                        "conteo": {"$sum": 1}
                    }
                }
            },
            # Mapear los rangos numéricos a descripciones
            {
                "$project": {
                    "_id": {
                        "$switch": {
                            "branches": [
                                {"case": {"$eq": ["$_id", 0]}, "then": "Bajo"},
                                {"case": {"$eq": ["$_id", 2]},
                                    "then": "Medio"},
                                {"case": {"$eq": ["$_id", 4]}, "then": "Alto"}
                            ],
                            "default": "Sin clasificar"
                        }
                    },
                    "conteo": 1
                }
            }
        ]

        resultado = list(collection.aggregate(pipeline))
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )
