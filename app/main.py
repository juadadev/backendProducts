from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.product import router_product
from app.routes.products_dynamo import router_product_dynamo
from app.routes.s3_routes import router_backup

app = FastAPI()

app.include_router(router_product)
app.include_router(router_product_dynamo)
app.include_router(router_backup)

allow_origins = [
    "http://localhost:5173",  # React en desarrollo
    "https://midominio.com",  # Producción
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
