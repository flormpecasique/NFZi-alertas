# amazon_api.py
from amazon_paapi import AmazonProductAPI
import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ASSOCIATE_TAG = os.getenv("AWS_ASSOCIATE_TAG")

# ✅ IMPORTANTE: Añade el parámetro `country`
amazon = AmazonProductAPI(
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_ASSOCIATE_TAG,
    country="ES",        # o "es" también funciona
    region="eu-west-1"
)

def obtener_precio_amazon(asin):
    try:
        items = amazon.get_items(asin)
        if items:
            title = items[0].title
            price = items[0].price_and_currency[0]
            print(f"Producto: {title}, Precio: {price}")
            return price
        else:
            print(f"No se encontraron resultados para el ASIN: {asin}")
            return None
    except Exception as e:
        print(f"Error al obtener el precio para el ASIN {asin}: {str(e)}")
        return None

