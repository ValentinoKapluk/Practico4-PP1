from fastapi import FastAPI
from routers.productos import router
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlmodel import SQLModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router, prefix="/productos")

app.title = "Tienda de Musica"
app.summary = "Venta de instrumentos"
app.version = "0.0"

#SQLModel.metadata.create_all(engine)