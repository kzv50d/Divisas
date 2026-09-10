import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Configurar la URL específica de monedas y los encabezados de simulación
url = "https://yahoo.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Realizar la petición y definir la variable 'response
response = requests.get(url, headers=headers)

# 2. Parsear el documento HTML con BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar la tabla principal de mercados en el HTML
tabla = soup.find("table")
datos = []

if tabla:
    # Recorrer todas las filas saltándonos los encabezados
    filas = tabla.find_all("tr")[1:]

    for fila in filas:
        columnas = fila.find_all("td")

        # Estructurar la fila si cuenta con el mínimo de datos requerido
        if len(columnas) >= 3:
            simbolo = columnas[0].text.strip()
            nombre = columnas[1].text.strip()

            # Buscar el precio en vivo dentro de la etiqueta 'fin-streamer' si existe
            fin_streamer = columnas[2].find("fin-streamer")
            precio_actual = fin_streamer.text.strip() if fin_streamer else columnas[2].text.strip()

            datos.append({
                "Símbolo": simbolo,
                "Nombre": nombre,
                "Precio Actual": precio_actual
            })

    # 3. Guardar la estructura en un archivo CSV reutilizable
    if datos:
        df = pd.DataFrame(datos)
        df.to_csv("catalogo_divisas.csv", index=False, encoding="utf-8-sig")
        print(f"¡Scraping exitoso! Se procesaron {len(df)} divisas y se guardaron en 'catalogo_divisas.csv'.")
        print(df.head()) # Muestra un pequeño resumen en la consola
    else:
        print("Error: No se lograron extraer filas con datos válidos de la tabla.")
else:
    print("Error: No se localizó ninguna estructura de tabla (<table>) en el código HTML.")
