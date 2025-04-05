from notion_client import Client
from datetime import datetime
import requests, re, os
from amazon_api import obtener_precio_amazon

NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("DATABASE_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

notion = Client(auth=NOTION_SECRET)

def enviar_alerta_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": mensaje})

def obtener_asin_de_url(url):
    match = re.search(r"(?:/dp/|/gp/product/)([A-Z0-9]{10})", url)
    return match.group(1) if match else None

def handler(request):
    db = notion.databases.query(database_id=DATABASE_ID)
    for page in db["results"]:
        props = page["properties"]
        producto = props["Producto"]["title"][0]["plain_text"]
        url_producto = props["URL Amazon"]["url"]
        precio_registrado = props["Precio registrado (€)"]["number"]
        umbral = props["Umbral de alerta (%)"]["number"]

        asin = obtener_asin_de_url(url_producto)
        if not asin:
            continue

        nuevo_precio = obtener_precio_amazon(asin)
        if nuevo_precio is None:
            continue

        cambio = ((nuevo_precio - precio_registrado) / precio_registrado) * 100
        if cambio <= umbral:
            enviar_alerta_telegram(
                f"ALERTA: El precio de '{producto}' bajó más del {umbral}%!\nNuevo precio: {nuevo_precio}€"
            )

        notion.pages.update(
            page_id=page["id"],
            properties={
                "Precio actual (€)": {"number": nuevo_precio},
                "% Cambio": {"number": cambio},
                "Última actualización": {"date": {"start": datetime.now().isoformat()}}
            }
        )

    return {"statusCode": 200, "body": "Precios actualizados"}
