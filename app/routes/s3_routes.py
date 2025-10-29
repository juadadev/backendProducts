import json
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.database import get_db
from app.database.s3 import (  # 👈 importa también el nombre del bucket
    S3_BUCKET_NAME,
    s3,
)
from app.models.product import Product

router_backup = APIRouter(
    prefix="/backup",
    tags=["backup"],
    responses={404: {"description": "Not found"}},
)


@router_backup.get("/backup")
def backup_data(db: Session = Depends(get_db)):
    productos = db.query(Product).all()
    data = [
        {
            "id_product": p.id_product,
            "name": p.name,
            "price": p.price,
            "quantity": p.quantity,
            "description": p.description,
        }
        for p in productos
    ]

    json_data = json.dumps(data)
    json_bytes = BytesIO(json_data.encode("utf-8"))

    try:
        s3.upload_fileobj(
            json_bytes, S3_BUCKET_NAME, "backup.json"
        )  # 👈 usa el nombre real del bucket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo a S3: {str(e)}")

    return JSONResponse(content={"mensaje": "Backup subido a S3 con éxito"})
