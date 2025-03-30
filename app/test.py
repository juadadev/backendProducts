import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # Ajusta la región si es diferente
table = dynamodb.Table("product")

response = table.get_item(Key={"id_product": "1"})  # Asegúrate de que el nombre del campo sea correcto
print(response)
