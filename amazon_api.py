import os
import boto3
from botocore.exceptions import NoCredentialsError

# Ya no necesitamos: from dotenv import load_dotenv ni load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ASSOCIATE_TAG = os.getenv("AWS_ASSOCIATE_TAG")

def obtener_precio_amazon(asin):
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_ASSOCIATE_TAG:
        print("Error: Credenciales de Amazon API no configuradas correctamente.")
        return None

    client = boto3.client(
        'paapi5',
        region_name='eu-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    try:
        response = client.get_items(
            ItemIds=[asin],
            Resources=["ItemInfo.Title", "Offers.Listings.Price"],
            PartnerTag=AWS_ASSOCIATE_TAG,
            PartnerType='Associates'
        )

        if response['ItemsResult']['Items']:
            item = response['ItemsResult']['Items'][0]
            title = item['ItemInfo']['Title']['DisplayValue']
            price = item['Offers']['Listings'][0]['Price']['Amount']
            print(f"Producto: {title}, Precio: {price}€")
            return price
        else:
            print(f"No se encontraron resultados para el ASIN: {asin}")
            return None

    except NoCredentialsError:
        print("Error: No se han configurado las credenciales correctamente.")
        return None
    except Exception as e:
        print(f"Error al obtener el precio para el ASIN {asin}: {str(e)}")
        return None
