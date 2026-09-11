import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://es-us.finanzas.yahoo.com/mercados/monedas/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, "html.parser")
tabla = soup.find("table")
datos = []

if tabla:
    filas = tabla.find_all("tr")[1:]

    for fila in filas:
        columnas = fila.find_all("td")

        if len(columnas) >= 3:
            simbolo = columnas[0].text.strip()
            nombre = columnas[1].text.strip()

            fin_streamer = columnas[2].find("fin-streamer")
            precio_actual = fin_streamer.text.strip() if fin_streamer else columnas[2].text.strip()

            datos.append({
                "Símbolo": simbolo,
                "Nombre": nombre,
                "Precio Actual": precio_actual
            })

    df = pd.DataFrame(datos)
    df.to_csv("catalogo_divisas.csv", index=False, encoding="utf-8-sig")
    print("Scraping exitoso y archivo catalogo_divisas.csv creado.")
  
else:
    print("No se encontró ninguna tabla en la página")
  