from fastapi import FastAPI
from app.routes.product import router_product 
from app.routes.products_dynamo import router_product_dynamo 
from app.routes.s3_routes import router_backup

app = FastAPI()

app.include_router(router_product)
app.include_router(router_product_dynamo)
app.include_router(router_backup)