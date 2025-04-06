# amazon_api.py
from amazon_paapi import AmazonApi
import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ASSOCIATE_TAG = os.getenv("AWS_ASSOCIATE_TAG")

# Inicializa AmazonAPI con las credenciales
amazon = AmazonApi(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_ASSOCIATE_TAG, region="eu-west-1")

def obtener_precio_amazon(asin):
    try:
        # Usamos el método `get_items` para obtener información del producto
        items = amazon.get_items(asin)
        if items:
            title = items[0].title
            price = items[0].price_and_currency[0]  # Obtiene el precio y la moneda
            print(f"Producto: {title}, Precio: {price}")
            return price
        else:
            print(f"No se encontraron resultados para el ASIN: {asin}")
            return None
    except Exception as e:
        print(f"Error al obtener el precio para el ASIN {asin}: {str(e)}")
        return None
