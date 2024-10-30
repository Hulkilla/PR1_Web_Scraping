from source.functions import webConnect
from source.functions import RobotsReading
from source.functions import userAgentRequests
from source.functions import dataExtraction
from source.functions import tecnocasaWebpages
from source.functions import csvExport
from source.functions import urlExtraction

url = "https://www.tecnocasa.es/"

#Mercado libre se puede usar: https://mercadolibre.com/
#Fotocasa no tiene robots.txt
#tecnocasa no permite labores de mantenimiento pero admite todo tipo de bots


robots = RobotsReading(url)
if robots:
    print("The robots.txt is: \n")
    print(robots)


userAgent = userAgentRequests(url)
if userAgent:
    print(userAgent)


urls_tecnocasa = tecnocasaWebpages(url)


urlList = urlExtraction(urls_tecnocasa)

csvExport(urls_tecnocasa, "pruebas/url_tecnocasa.csv")


data_ejemplo = dataExtraction(['https://www.tecnocasa.es/venta/piso/valladolid/valladolid/598033.html'])  
print(data_ejemplo) 
csvExport(data_ejemplo, "pruebas/piso_prueba.csv")

#Llamada a la función con la URL base
productos = pagesIteration("https://www.tecnocasa.es/venta/piso/valladolid/valladolid/598")