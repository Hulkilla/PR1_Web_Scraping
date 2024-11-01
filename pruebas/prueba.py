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

