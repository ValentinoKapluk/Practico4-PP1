#IMPORTS
from sqlalchemy import Integer, String, Column
from database import Base

#SCHEMAS
class Producto(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo_de_producto = Column(String)
    marca = Column(String)
    precio = Column(Integer)
    imagen = Column(String)
