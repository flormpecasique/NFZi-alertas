# amazon_api.py
from amazon_paapi import AmazonApi
import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ASSOCIATE_TAG = os.getenv("AWS_ASSOCIATE_TAG")

# Inicializa AmazonApi con país y región
amazon = AmazonApi(
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_ASSOCIATE_TAG,
    country="ES",  # España (puedes cambiarlo si lo deseas)
    region="eu-west-1"  # Región de Europa Occidental
)

def obtener_precio_amazon(asin):
    try:
        # Obtener información del producto usando el ASIN
        items = amazon.get_items(asin)
        if items:
            title = items[0].title  # Título del producto
            price, currency = items[0].price_and_currency  # Precio y moneda
            precio_formateado = f"{price} {currency}"  # Formato del precio
            print(f"Producto: {title}, Precio: {precio_formateado}")
            return price, precio_formateado  # Retorna el precio y el formato
        else:
            print(f"No se encontraron resultados para el ASIN: {asin}")
            return None, None  # No se encontraron productos
    except Exception as e:
        print(f"Error al obtener el precio para el ASIN {asin}: {str(e)}")
        return None, None  # Error en la obtención de datos
