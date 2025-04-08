from fastapi import APIRouter, HTTPException
from app.database.database_dynamodb import table, dynamodb
from app.models.product_dynamo import ProductDynamo, ProductUpdateDynamo
from boto3.dynamodb.conditions import Key
from decimal import Decimal

router_product_dynamo = APIRouter(
    prefix="/products-dynamo",
    tags=["products-dynamo"],
    responses={404: {"description": "Not found"}},
)


# 📌 Obtener todos los productos
@router_product_dynamo.get("/")
def get_all_products():
    response = table.scan()
    return response.get("Items", [])


# 🔥 Función para convertir Decimal a float
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)  # Convierte los Decimals en float
    return obj


# 📌 Obtener un producto por ID
@router_product_dynamo.get("/{product_id}")
def get_product(product_id: str):
    response = table.get_item(Key={"id_product": product_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Product not found")

    product = response["Item"]
    return convert_decimals(product)


# 📌 Crear un nuevo producto
@router_product_dynamo.post("/")
def create_product(product: ProductDynamo):
    table.put_item(Item=product.model_dump())
    return {"message": "Product created", "product": product}


from fastapi import HTTPException
from boto3.dynamodb.conditions import Key


# 📌 Actualizar un producto existente
@router_product_dynamo.put("/{product_id}")
def update_product(product_id: str, product_update: ProductUpdateDynamo):
    existing_product = table.get_item(Key={"id_product": product_id})

    if "Item" not in existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Inicializamos la expresión de actualización y los valores
    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}

    # Iteramos sobre los campos a actualizar
    for key, value in product_update.model_dump(exclude_unset=True).items():
        # Verificamos si la clave es una palabra reservada
        if key == "name":
            expression_attribute_names["#name"] = key
            update_expression += "#name = :name, "
        else:
            update_expression += f"{key} = :{key}, "

        # Agregamos el valor al diccionario de valores
        expression_attribute_values[f":{key}"] = value

    # Quitamos la última coma de la expresión de actualización
    update_expression = update_expression.rstrip(", ")

    # Ejecutamos la actualización en DynamoDB
    try:
        table.update_item(
            Key={"id_product": product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

    return {"message": "Product updated"}


# 📌 Eliminar un producto
@router_product_dynamo.delete("/{product_id}")
def delete_product(product_id: str):
    table.delete_item(Key={"id_product": product_id})
    return {"message": "Product deleted"}
