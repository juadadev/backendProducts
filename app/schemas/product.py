from pydantic import BaseModel
from typing import Optional


# ✅ Modelo para Crear Producto (sin ID porque se genera automáticamente)
class ProductCreate(BaseModel):
    id_product: str  # ID del producto enviado desde el frontend
    name: str
    price: int
    quantity: int
    description: str


# ✅ Modelo para Actualizar Producto (todos los campos opcionales)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    description: Optional[str] = None


# ✅ Modelo para Borrar Producto (solo se necesita el ID)
class ProductDelete(BaseModel):
    id_product: str


# ✅ Modelo para Consultar un Producto (devuelve toda la info)
class ProductResponse(BaseModel):
    id_product: str
    name: str
    price: int
    quantity: int
    description: str

    class Config:
        from_attributes = True  # Permite convertir SQLAlchemy models a Pydantic
