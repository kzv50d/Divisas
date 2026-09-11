import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

script_code = """import requests
import re
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

        if len(columnas) >= 4:
            simbolo = columnas[0].text.strip()
            nombre = columnas[1].text.strip()
            texto_precio = columnas[3].text.strip()

            precio = re.match(r"([\\d,.\\-]+)", texto_precio)
            precio_actual = precio.group(1) if precio else texto_precio

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
"""

with open("divisas.py", "w", encoding="utf-8") as f:
    f.write(script_code)
