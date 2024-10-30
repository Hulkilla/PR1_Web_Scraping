import requests
from bs4 import BeautifulSoup
import json
import time
import random
import csv
import os

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



def tecnocasaWebpages(url):
    """
    This function connects to a specified Tecnocasa web page URL, retrieves its HTML content,
    and extracts categorized property links such as 'Pisos en venta' and 'Casas en venta'.
    The function organizes this information in a dictionary with categories as keys 
    and lists of link dictionaries as values.
    
    Args:
    - url (str): Web page URL as a string.
    
    Returns:
    - dict: A dictionary where keys are category names (e.g., 'Pisos en venta'),
      and values are lists of dictionaries, each containing:
        - 'nombre' (str): Text of the link, e.g., 'Pisos en venta Almería'.
        - 'url' (str): URL of the link.
      Returns None if there is an error in connecting to the page.
    """

    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        categorias = {}
        
        for section in soup.find_all("div", class_="static-block p-2 flex-fill"):
            # Extraer el nombre de la categoría del encabezado <h2>
            categoria_nombre = section.find("h2").get_text(strip=True)
            
            # Extraer enlaces y sus nombres
            enlaces = []
            for item in section.find_all("li"):
                enlace = item.find("a")
                texto = enlace.get_text(" ", strip=True)  # Obtener texto del enlace
                url = enlace["href"]  # Obtener URL del enlace
                enlaces.append({"nombre": texto, "url": url})
            
            # Añadir a la categoría en el diccionario
            categorias[categoria_nombre] = enlaces
        
        return categorias
    else:
        print(f"Error al cargar la página: {response.status_code}")
        return None 



def urlExtraction(data):
    """
    Extracts all URLs from a dictionary of categorized links.
    
    Args:
    - data (dict): Dictionary with categories as keys and lists of link dictionaries as values.
    
    Returns:
    - list: List of all URLs in the dictionary.
    """
    urls = []
    for enlaces in data.values():
        for enlace in enlaces:
            urls.append(enlace["url"])
    return urls



def dataExtraction(url):
    """
    This function connects to a given URL, retrieves the HTML content,
    finds JSON data embedded within, and extracts key real estate details 
    into a dictionary format.
    
    Args:
    - url (str): URL of the real estate listing page as a string.
    
    Returns:
    - dict: A dictionary containing the extracted property details, 
            or None if there was an error.
    """

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
      
        json_data_script = soup.find("estate-show-v2")
        json_text = json_data_script[':estate'] if json_data_script else None


        # Convertir el JSON en un diccionario de Python
        if json_text:
            try:
                json_data = json.loads(json_text)
                # Extracción de los datos
               
                datos_inmueble = {
                    "Pais":json_data.get("country"),
                    "ciudad": json_data.get("city", {}).get("title"),
                    "zona": json_data.get("district", {}).get("title"),
                    "calle":json_data.get("address"),
                    "contrato": json_data.get("contract", {}).get("title"),
                    "dormitorios": json_data.get("features", {}).get("bedrooms"),
                    "metros_cuadrados": json_data.get("numeric_surface"),
                    "baños": json_data.get("bathrooms"),
                    "tipo_inmueble": json_data.get("features", {}).get("category"),
                    "ascensor": json_data.get("features", {}).get("elevator"),
                    "calefaccion": json_data.get("features", {}).get("heating"),
                    "planta/piso": json_data.get("features", {}).get("floor"),
                    "año_construcción": json_data.get("dates", {}).get("build_year"),
                    "Clase_energia":json_data.get("energy_data",{}).get("class"),
                    "consumo_energia": json_data.get("energy_data", {}).get("efficiency"),
                    "precio_venta": json_data.get("numeric_price"),
                    "Fecha_publicación": json_data.get("last_published_at")
                }   
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



def pagesIteration(urlBase, max_pages=150, delay_min=1, delay_max=5, max_empty_pages = 150):
    products = []
    empty_page_count = 0

    for i in range(100, max_pages + 1):
        url = f"{urlBase}{i}.html"
        print(f"Extrayendo datos de {url}")
        productos_pagina = dataExtraction(url)
        
        if productos_pagina:
            products.extend(productos_pagina)
            empty_page_count = 0  # Reinicia el contador si encuentra datos
        else:
            empty_page_count += 1
            print(f"No se encontraron datos en la página {i}. Páginas vacías consecutivas: {empty_page_count}")
            
            if empty_page_count >= max_empty_pages:
                print("Demasiadas páginas vacías consecutivas. Deteniendo la extracción.")
                break  # Sale del bucle si hay error o no hay datos
    
    # Añade un retardo aleatorio entre cada solicitud
        delay = random.uniform(delay_min, delay_max)
        print(f"Esperando {delay:.2f} segundos antes de la próxima solicitud.")
        time.sleep(delay)

    return products



def dictFlatten(data, parent_key='', sep='_'):
    """
    Flattens a nested dictionary.

    Args:
    - data (dict): The dictionary to flatten.
    - parent_key (str): The base key to prepend to the flattened keys.
    - sep (str): Separator between parent and child keys.

    Returns:
    - dict: A flattened dictionary.
    """
    items = {}
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(dictFlatten(value, new_key, sep=sep))
        else:
            items[new_key] = value
    return items



def csvExport(data, file_path="prueba.csv", header=None):
    """
    Exports various structures of JSON-like data to a CSV file.
    
    Args:
    - data (list or dict): Data in JSON format (list of dicts or dict of lists).
    - file_path (str): Complete path (folder + filename) where the CSV file will be saved.
    - header (list): Optional list of headers for the CSV file.
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    # Try to detect the structure of the data
    try:
        rows = []

        if isinstance(data, dict):
        # Si el diccionario es simple, convierte a una lista de una fila
            flattened_item = dictFlatten(data)
            rows.append(flattened_item)

        elif isinstance(data, dict):
            # If it's a dict of lists
            
            for category, items in data.items():
                for item in items:
                    flattened_item = dictFlatten(item)
                    flattened_item['Categoria'] = category
                    rows.append(flattened_item)
        
        elif isinstance(data, list):
            # If it's a list of dicts
            rows = [dictFlatten(item) for item in data]

        else:
            raise ValueError("Unsupported data format: Must be a list or dictionary")

        # Use a default header if none is provided
        if header is None:
            header = set()
            for row in rows:
                header.update(row.keys())
            header = list(header)

        # Open CSV file for writing
        with open(file_path, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Exported to {file_path}")

    except Exception as e:
        print(f"An error occurred while exporting data: {e}")



