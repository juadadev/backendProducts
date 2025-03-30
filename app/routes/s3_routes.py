from io import BytesIO
import os
import json
import boto3
from ..database.s3 import s3
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from ..database.database import get_db
from ..models.product import Product
 
# 📌 Configurar el router
router_backup = APIRouter(
    prefix="/backup",
    tags=["backup"],
    responses={404: {"description": "Not found"}},
)
 
 
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
 
@router_backup.get("/backup")
def backup_data(db: Session = Depends(get_db)):
    # Obtener los datos de la base de datos
    productos = db.query(Product).all()
    data = [{"id": p.id, "name": p.name , "price": p.price, "quantity": p.quantity , "description": p.description} for p in productos]
 
    # Guardar en un archivo temporal
    #file_path = "/tmp/backup.json"
    #with open(file_path, "w") as f:
    #    json.dump(data, f)
 
   # Convertir a JSON en memoria
    json_data = json.dumps(data)
    json_bytes = BytesIO(json_data.encode("utf-8"))
 
    # Subir directamente a S3
    try:
        s3.upload_fileobj(json_bytes, BUCKET_NAME, "backup.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo a S3: {str(e)}")
 
    return JSONResponse(content={"mensaje": "Backup subido a S3 con éxito"})