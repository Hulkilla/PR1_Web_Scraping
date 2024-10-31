import requests
from bs4 import BeautifulSoup
import json

# URL de la página a raspar
url = "https://www.tecnocasa.es/venta/piso/jaen/jaen.html"

# Hacer la solicitud a la página
response = requests.get(url)
response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

# Parsear el contenido HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar el bloque donde se encuentra la información de estates
json_data_script = soup.find("estates-index")
json_text = json_data_script[':estates'] if json_data_script else None
id_finder = json.loads(json_text)
for i in range(len(id_finder)):
    print(id_finder[i]['detail_url'])
    
#ids = [id_finder['id'] for id in id_finder if 'id' in id]
#print(ids)
# Extraer el contenido de la etiqueta <script> y convertirlo a JSON
##if estates_script:
##    # Aquí estamos asumiendo que el contenido es un string en JSON
##    json_text = estates_script.string
##    json_text = json_text[json_text.find('['):json_text.rfind(']') + 1]  # Extraer solo la parte del JSON
##    estates_data = json.loads(json_text)
##
##    # Base de la URL a la que se le agregará el ID
##    base_url = "https://www.tecnocasa.es/venta/piso/jaen/"
##
##    # Procesar los datos de las propiedades
##    for estate in estates_data:
##        # Extraer los campos necesarios
##        estate_id = estate.get('id')
##        titulo = estate.get('title')
##        precio = estate.get('price')
##        superficie = estate.get('surface')
##        habitaciones = estate.get('rooms')
##
##        # Construir la URL completa
##        detail_url = f"{base_url}{estate_id}.html"
##
##        # Imprimir los resultados
##        print(f"Título: {titulo}, Precio: {precio}, Superficie: {superficie}, Habitaciones: {habitaciones}, Detalle: {detail_url}")
##else:
##    print("No se encontró el bloque de estates.")
##