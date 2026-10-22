#IMPORTS
from fastapi import APIRouter
from fastapi import Path, Query, Body
from fastapi import HTTPException, Depends
from typing import Annotated
from database import get_db
from sqlalchemy.orm import Session
from models.productos_models import Producto
from schemas.productos_schemas import ProductoSchema, ProductoUpdateSchema
router = APIRouter()


#PATH OPERATIONS
#Mostrar todos los productos
@router.get("/all", tags=["Productos"], response_model=list[ProductoSchema])
def productos_all(db: Session = Depends(get_db)) -> list[ProductoSchema]:
    return db.query(Producto).all()

#Mostrar producto especifico por id
@router.get("/{id}", tags=["Productos"], response_model=ProductoSchema)
def obtener_producto_by_id(id: Annotated[int, Path(gt=0, lt=1000)], db:Session = Depends(get_db)) -> ProductoSchema:
    producto_obtenido = db.query(Producto).filter(Producto.id == id).first()
    if not producto_obtenido:
        raise HTTPException(
            status_code=404, detail="No se encontro el producto buscado")
    return producto_obtenido

#Mostrar productos filtrados por nombre
@router.get("/", tags=["Productos"], response_model=list[ProductoSchema])
def productos_by_nombre(nombre: Annotated[str, Query(min_length=1, max_length=50)], db: Session = Depends(get_db)) -> list[ProductoSchema]:
    producto_obtenido = db.query(Producto).filter(Producto.nombre == nombre).all()
    if not producto_obtenido:
        raise HTTPException(
            status_code=404, detail="No se encontro el producto buscado")
    return producto_obtenido

#Agregar un nuevo producto a productos
@router.post("/nuevo", response_model=ProductoSchema)
def nuevo_producto(producto:ProductoSchema, db: Session = Depends(get_db)) -> ProductoSchema:
    nuevo_producto = Producto(
        nombre = producto.nombre,
        tipo_de_producto = producto.tipo_de_producto,
        marca = producto.marca,
        precio = producto.precio,
        imagen = producto.imagen
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto #raise HTTPException(status_code=400, detail="El producto a agregar ya existe")

#Actualizar un producto
@router.put("/actualizar", tags=["Productos"], response_model=ProductoUpdateSchema)
def actualizar_producto(
    producto_id: Annotated[int, Body(gt=0)], producto: ProductoUpdateSchema, db: Session = Depends(get_db)):
    producto_obtenido = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="No se encontro el producto buscado")
    producto_obtenido.nombre = producto.nombre,
    producto_obtenido.tipo_de_producto = producto.tipo_de_producto,
    producto_obtenido.marca = producto.marca,
    producto_obtenido.precio = producto.precio,
    producto_obtenido.imagen = producto.imagen
    db.commit()
    db.refresh(nuevo_producto)
    return producto_obtenido

#Borrar producto de productos
@router.delete("/borrar", tags=["Productos"], response_model= list[ProductoSchema])
def borrar_producto(producto_id: Annotated[int, Body(gt=0)], db: Session = Depends(get_db)) -> ProductoSchema:
    producto_obtenido = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="No se encontro el producto buscado")
    db.delete(producto_obtenido)
    db.commit()


