#IMPORTS
from fastapi import APIRouter
from fastapi import Path, Query, Body
from fastapi import HTTPException, Depends
from typing import Annotated
from database import get_db
from models.productos_models import Producto, ProductoCreate, ProductoPublic, ProductoPublicNested, Marca, MarcaPublicNested, MarcaPublic, MarcaCreate
from sqlmodel import Session, select

router = APIRouter()


#PATH OPERATIONS
#Mostrar todos los productos
@router.get("/all", tags=["Productos"], response_model=list[ProductoPublic])
def productos_all(db: Session = Depends(get_db)) -> list[Producto]:
    return db.exec(select(Producto)).all()

#Mostrar producto especifico por id
@router.get("/{id}", tags=["Productos"], response_model=ProductoPublicNested)
def obtener_producto_by_id(id: Annotated[int, Path(gt=0, lt=1000)], db:Session = Depends(get_db)) -> Producto:
    producto_obtenido = db.get(Producto, id)
    if not producto_obtenido:
        raise HTTPException(
            status_code=404, detail="No se encontro el producto buscado")
    return producto_obtenido

#Mostrar productos filtrados por nombre
@router.get("/", tags=["Productos"], response_model=list[ProductoPublic])
def productos_by_nombre(nombre: Annotated[str, Query(min_length=1, max_length=50)], db: Session = Depends(get_db)) -> list[Producto]:
    producto_obtenido = db.get(Producto, nombre)
    if not producto_obtenido:
        raise HTTPException(
            status_code=404, detail="No se encontro el producto buscado")
    return producto_obtenido

#Agregar un nuevo producto a productos
@router.post("/nuevo_producto", tags=["Productos"], response_model=ProductoPublic)
def nuevo_producto(producto:ProductoCreate, db: Session = Depends(get_db)) -> Producto:
    nuevo_producto = Producto(
        nombre = producto.nombre,
        tipo_de_producto = producto.tipo_de_producto,
        marca_id = producto.marca_id,
        precio = producto.precio,
        imagen = producto.imagen
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto #raise HTTPException(status_code=400, detail="El producto a agregar ya existe")

#Actualizar un producto
@router.put("/actualizar_producto", tags=["Productos"], response_model=ProductoPublic)
def actualizar_producto(
    producto_id: Annotated[int, Body(gt=0)], producto: ProductoCreate, db: Session = Depends(get_db)):
    producto_obtenido = db.get(Producto, producto_id)
    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="No se encontro el producto buscado")
    producto_obtenido.nombre = producto.nombre
    producto_obtenido.tipo_de_producto = producto.tipo_de_producto
    producto_obtenido.marca_id = producto.marca_id
    producto_obtenido.precio = producto.precio
    producto_obtenido.imagen = producto.imagen
    db.commit()
    db.refresh(producto_obtenido)
    return producto_obtenido

#Borrar producto de productos
@router.delete("/borrar_producto", tags=["Productos"], response_model= ProductoPublic)
def borrar_producto(producto_id: Annotated[int, Body(gt=0)], db: Session = Depends(get_db)) -> Producto:
    producto_obtenido = db.get(Producto, producto_id)
    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="No se encontro el producto buscado")
    db.delete(producto_obtenido)
    db.commit()
    return producto_obtenido



@router.get("/marcas/{marca_id}", tags=["Marcas"], response_model=MarcaPublicNested)
def read_marca(marca_id:int, db: Session = Depends(get_db)):
    marca = db.get(Marca, marca_id)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

@router.post("/nueva_marca", tags=["Marcas"], response_model= MarcaPublic)
def nueva_marca(marca:MarcaCreate, db: Session = Depends(get_db)) -> Marca:
    nueva_marca = Marca(
        nombre = marca.nombre,
        pais = marca.pais
    )
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    return nueva_marca #raise HTTPException(status_code=400, detail="La marca a agregar ya existe")