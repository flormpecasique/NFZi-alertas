import os
from amazon_paapi import AmazonAPI

# Obtén las credenciales de las variables de entorno
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ASSOCIATE_TAG = os.getenv("AWS_ASSOCIATE_TAG")

def obtener_precio_amazon(asin):
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_ASSOCIATE_TAG:
        print("Error: Credenciales de Amazon API no configuradas correctamente.")
        return None

    # Instancia de AmazonAPI usando las credenciales
    amazon = AmazonAPI(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, region="eu-west-1")

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
