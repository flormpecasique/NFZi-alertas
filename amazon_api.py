# amazon_api.py
from amazon_paapi import AmazonProductAPI
import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ASSOCIATE_TAG = os.getenv("AWS_ASSOCIATE_TAG")

# Inicializa AmazonProductAPI con las credenciales
amazon = AmazonProductAPI(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_ASSOCIATE_TAG, region="eu-west-1")

def obtener_precio_amazon(asin):
    try:
        # Usamos el método `get_items` con el parámetro correcto (una lista de ASINs)
        items = amazon.get_items(asins=[asin])
        if items:
            item = items[0]
            title = item.title
            price = item.prices.price.amount
            currency = item.prices.price.currency
            print(f"Producto: {title}, Precio: {price} {currency}")
            return price
        else:
            print(f"No se encontraron resultados para el ASIN: {asin}")
            return None
    except Exception as e:
        print(f"Error al obtener el precio para el ASIN {asin}: {str(e)}")
        return None
