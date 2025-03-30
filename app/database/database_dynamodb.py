import os
import boto3
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde .env

# 🔹 Configurar la conexión a DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# 🔹 Conectar con la tabla de productos
TABLE_NAME = "product"  # Asegúrate de que esta tabla existe en DynamoDB
table = dynamodb.Table(TABLE_NAME)
