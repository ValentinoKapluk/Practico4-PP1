#IMPORTS
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
#SCHEMAS
class ProductoBase(SQLModel):

    nombre: str = Field(index=True)
    tipo_de_producto: str
    marca_id: Optional[int] = Field(default=None, foreign_key="marca.id")
    precio: float
    imagen: str

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marca: Optional[Marca] = Relationship(back_populates="productos")

class ProductoCreate(ProductoBase):
    pass

class ProductoPublic(ProductoBase):
    id: int

class ProductoPublicNested(ProductoPublic):
    marca: Optional[MarcaPublic] = None


class MarcaBase(SQLModel):
    nombre: str = Field(index=True)
    pais: str

class Marca(MarcaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="marca")

class MarcaCreate(MarcaBase):
    pass

class MarcaPublic(MarcaBase):
    id: int

class MarcaPublicNested(MarcaPublic):
    productos: List[ProductoPublic] = []
