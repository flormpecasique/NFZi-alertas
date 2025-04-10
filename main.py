from notion_client import Client
import random
from datetime import datetime
import requests
import re
import os

# Verificar credenciales importantes
NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("DATABASE_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Debug para verificar las variables de entorno
print(f"NOTION_SECRET: {NOTION_SECRET}")
print(f"DATABASE_ID: {DATABASE_ID}")
print(f"TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")
print(f"CHAT_ID: {CHAT_ID}")

if not NOTION_SECRET or not DATABASE_ID:
    raise Exception("❌ Faltan las credenciales de Notion.")
if not TELEGRAM_TOKEN or not CHAT_ID:
    raise Exception("❌ Faltan las credenciales de Telegram.")

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

from amazon_api import obtener_precio_amazon

def actualizar_productos():
    try:
        db = notion.databases.query(database_id=DATABASE_ID)
    except Exception as e:
        print(f"❌ Error al consultar la base de datos de Notion: {e}")
        return

    for page in db.get("results", []):
        try:
            props = page["properties"]
            producto = props["Producto"]["title"][0]["plain_text"]
            url_producto = props["URL Amazon"]["url"]
            precio_registrado = props["Precio registrado (€)"]["number"]
            umbral = props["Umbral de alerta (%)"]["number"]

            # Si el umbral está vacío, asignamos un valor por defecto de 0%
            umbral = umbral if umbral is not None else 0

            asin = obtener_asin_de_url(url_producto)
            if not asin:
                print(f"No se pudo extraer el ASIN para el producto {producto} de la URL {url_producto}")
                continue

            nuevo_precio, precio_mostrar = obtener_precio_amazon(asin)
            if nuevo_precio is None:
                continue

            cambio = ((nuevo_precio - precio_registrado) / precio_registrado) * 100
            print(f"{producto}: {nuevo_precio}€ ({cambio:.2f}%)")

            # Verificar si el precio bajó más allá del umbral o si el nuevo precio es menor que el registrado
            if cambio <= umbral or nuevo_precio < precio_registrado:
                mensaje = f"ALERTA: El precio de '{producto}' ha bajado más del {umbral}% o ha bajado por debajo del precio registrado!\n\nNuevo precio: {precio_mostrar}"
                enviar_alerta_telegram(mensaje)
                print(f"ALERTA: {producto} bajó más del umbral definido o por debajo del precio registrado!")

            notion.pages.update(
                page_id=page["id"],
                properties={
                    "Precio actual (€)": {"number": nuevo_precio},
                    "% Cambio": {"number": cambio},
                    "Última actualización": {"date": {"start": datetime.now().isoformat()}}
                }
            )
        except Exception as e:
            print(f"❌ Error procesando producto: {e}")
            continue

if __name__ == "__main__":
    actualizar_productos()
