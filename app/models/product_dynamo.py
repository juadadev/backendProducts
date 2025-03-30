from pydantic import BaseModel
from typing import Optional

# 🔹 Modelo Pydantic para DynamoDB
class ProductDynamo(BaseModel):
    id: str  # DynamoDB usa strings como clave primaria
    name: str
    price: int
    quantity: int
    description: str

class ProductUpdateDynamo(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
