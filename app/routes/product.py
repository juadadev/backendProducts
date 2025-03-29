from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..database.database import get_db

router_product = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


# 📌 Obtener todos los productos
@router_product.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# 📌 Obtener un producto por ID
@router_product.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 📌 Crear un nuevo producto
@router_product.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# 📌 Actualizar un producto existente
@router_product.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Actualizamos solo los campos proporcionados
    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(existing_product, key, value)

    db.commit()
    db.refresh(existing_product)
    return existing_product


# 📌 Eliminar un producto
@router_product.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
