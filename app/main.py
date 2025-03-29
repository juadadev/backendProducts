from fastapi import FastAPI
from .routes.product import router_product

app = FastAPI()

app.include_router(router_product)
