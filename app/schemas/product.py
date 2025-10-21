from pydantic import BaseModel


# ✅ Modelo para Crear Producto (sin ID porque se genera automáticamente)
class ProductCreate(BaseModel):
    id_product: str | None = None  # ID del producto enviado desde el frontend
    name: str
    price: int
    quantity: int
    description: str


# ✅ Modelo para Actualizar Producto (todos los campos opcionales)
class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    quantity: int | None = None
    description: str | None = None


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
