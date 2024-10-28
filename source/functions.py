import requests
import csv
from bs4 import BeautifulSoup
import json

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

def RobotsReading(url):
    """
    This function reads the robots.txt file of a website and returns its contents.
    
    Args:
    - url (str): Website URL (without `/robots.txt`).
    
    Returns:
    - str: The content of the robots.txt file or an error message.
    """

    url_robots = url.rstrip('/') + '/robots.txt'
    try:
        response = requests.get(url_robots, headers = HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Could not access robots.txt file of {url}, status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while accessing robots.txt {e}")
        return None
    


def userAgentRequests(url):
    """
    This function check the user agent used in the requests.
    
    Args:
    - url (str): Website URL (without `/robots.txt`).
    
    Returns:
    - str: The user agent used.
    """

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print("The User-Agent used in the requests:", HEADERS["User-Agent"])
        return None
    else:
        print(f"Error {response.status_code}: It could not connect to {url}")
        return None



def webConnect(url):
    """
    This function allow a web connection and return HTML content.
    
    Args:
    - url (str): web page URL as string.
    
    Returns:
    - str: HTML content or a message error.
    """

    try:
        url = requests.get(url, headers = HEADERS)
        if url.status_code == 200:
            return url.text
        else:
            print(f"Error: Could not connect to the website {url}, code: {url.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while connecting: {e}")
        return None

def htmlToTXT(htmlContent, archive="pagina.txt"):
    with open(archive, "w", encoding="utf-8") as archivo:
        archivo.write(htmlContent)
    print(f"Contenido HTML guardado en {archive}")   


def dataExtraction(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
      
        json_data_script = soup.find("estate-show-v2")
        json_text = json_data_script[':estate'] if json_data_script else None

        # Convertir el JSON en un diccionario de Python
        if json_text:
            try:
                json_data = json.loads(json_text)

                # Extraer los datos solicitados
                datos_inmueble = {
                    "zona": json_data.get("district", {}).get("title"),
                    "ciudad": json_data.get("city", {}).get("title"),
                    "dormitorios": json_data.get("data")[7]["valore"] if "data" in json_data and len(json_data["data"]) > 7 else None,
                    "metros_cuadrados": json_data.get("data")[8]["valore"] if "data" in json_data and len(json_data["data"]) > 7 else None,
                    "baños": json_data.get("bathrooms"),
                    "tipo_inmueble": json_data.get("data")[6]["valore"] if "data" in json_data and len(json_data["data"]) > 6 else None,
                    "ascensor": "Sí" if json_data.get("features", {}).get("elevator") else "No",
                    "año_construcción": json_data.get("dates", {}).get("build_year"),
                    "consumo_energia": json_data.get("energy_data", {}).get("efficiency"),
                    "precio_venta": json_data.get("costs", {}).get("price")
                }   
                print("Datos del inmueble:", datos_inmueble)
                return datos_inmueble
            except json.JSONDecodeError:
                print("Error al decodificar el JSON")
                return None
        else:
            print("No se encontró el script de datos JSON")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def iterar_paginas(base_url, max_paginas=5):
    todos_los_productos = []
    for i in range(1, max_paginas + 1):
        url = f"{base_url}?page={i}"
        print(f"Extrayendo datos de {url}")
        productos_pagina = dataExtraction(url)
        
        if productos_pagina:
            todos_los_productos.extend(productos_pagina)
        else:
            break  # Sale del bucle si hay error o no hay datos

    return todos_los_productos

# Llamada a la función con la URL base
productos = iterar_paginas("https://ejemplo.com/productos")
