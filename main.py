from notion_client import Client
import random
from datetime import datetime
import requests
import re
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Credenciales de Notion desde .env
NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("DATABASE_ID")

# Credenciales de Telegram desde .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

notion = Client(auth=NOTION_SECRET)

# Función para enviar alertas a Telegram
def enviar_alerta_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": mensaje,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error al enviar el mensaje a Telegram:", response.text)

# Función para extraer el ASIN de la URL de Amazon
def obtener_asin_de_url(url):
    if "amazon" not in url:
        print(f"URL no válida para Amazon: {url}")
        return None

    match = re.search(r"(?:/dp/|/gp/product/)([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    else:
        print(f"No se pudo extraer el ASIN de la URL: {url}")
        return None

# Precio para cada producto con API real
from amazon_api import obtener_precio_amazon

def actualizar_productos():
    db = notion.databases.query(database_id=DATABASE_ID)
    for page in db["results"]:
        props = page["properties"]
        producto = props["Producto"]["title"][0]["plain_text"]
        url_producto = props["URL Amazon"]["url"]
        precio_registrado = props["Precio registrado (€)"]["number"]
        umbral = props["Umbral de alerta (%)"]["number"]

        asin = obtener_asin_de_url(url_producto)
        if not asin:
            print(f"No se pudo extraer el ASIN para el producto {producto} de la URL {url_producto}")
            continue

        # Obtenemos el precio de Amazon usando la API
        nuevo_precio = obtener_precio_amazon(asin)
        if nuevo_precio is None:
            continue

        # Calculamos el cambio porcentual en el precio
        cambio = ((nuevo_precio - precio_registrado) / precio_registrado) * 100

        print(f"{producto}: {nuevo_precio}€ ({cambio:.2f}%)")

        # Verificamos si el cambio supera el umbral para enviar una alerta
        if cambio <= umbral:
            mensaje = f"ALERTA: El precio de '{producto}' ha bajado más del {umbral}%!\n\nNuevo precio: {nuevo_precio}€"
            enviar_alerta_telegram(mensaje)
            print(f"ALERTA: {producto} bajó más del umbral definido!")

        # Actualizamos los datos en Notion
        notion.pages.update(
            page_id=page["id"],
            properties={
                "Precio actual (€)": {"number": nuevo_precio},
                "% Cambio": {"number": cambio},
                "Última actualización": {"date": {"start": datetime.now().isoformat()}}
            }
        )

# Llamada a la función para actualizar los productos
actualizar_productos()

