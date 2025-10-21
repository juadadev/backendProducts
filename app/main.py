from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routes.product import router_product
from app.routes.products_dynamo import router_product_dynamo
from app.routes.s3_routes import router_backup

app = FastAPI()

app.include_router(router_product)
app.include_router(router_product_dynamo)
app.include_router(router_backup)

allow_origins = [
    "http://localhost:5173",  # React en desarrollo
    "http://127.0.0.1:5173",  # React en desarrollo
    "https://midominio.com",  # Producción
    "*",
]

Base.metadata.create_all(bind=engine)  # Create tables in the database


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
