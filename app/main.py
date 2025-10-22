import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import create_database_and_table, wait_for_db
from app.routes.product import router_product
from app.routes.products_dynamo import router_product_dynamo
from app.routes.s3_routes import router_backup

logger = logging.getLogger(__name__)

app = FastAPI()

# Routers
app.include_router(router_product)
app.include_router(router_product_dynamo)
app.include_router(router_backup)

# CORS
allow_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:80",
    "https://midominio.com",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Startup event: create database and tables
@app.on_event("startup")
def on_startup():
    wait_for_db()
    create_database_and_table()
    logger.info("Database tables ensured at startup ")
