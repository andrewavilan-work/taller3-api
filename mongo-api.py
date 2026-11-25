from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Conexion al cluster Admonsis (157.253.236.88:8087).
# La URI con usuario y contraseña se lee de la variable de entorno MONGO_URI
# (se configura en el PC para probar local y en Render para el despliegue),
# asi la contraseña no queda escrita en el repositorio de GitHub.
client = MongoClient(os.environ["MONGO_URI"])

# Base de datos Admonsis (tiene el mismo nombre del usuario)
db = client["ISIS2304C05202620"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    # se buscan los comentarios del bar y se quita el _id porque no se puede pasar a JSON
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id}, {"_id": 0}))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

# GET /bares/{bar_id}/eventos
# Retorna todos los eventos del bar desde la coleccion 'eventos'
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db["eventos"].find({"bar_id": bar_id}, {"_id": 0}))
    return eventos

# POST /bares/{bar_id}/eventos
# Inserta el evento en la coleccion 'eventos' con bar_id y fecha_creacion
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}
