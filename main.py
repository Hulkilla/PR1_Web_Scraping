from source.functions import RobotsReading
from source.functions import userAgentRequests
from source.functions import dataExtraction
from source.functions import tecnocasaWebpages
from source.functions import urlsFilter
from source.functions import detailUrls
from source.functions import csvExport
from source.functions import filterUrlsByLocation
from source.functions import pagesIteration


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

filtered_urls = urlsFilter(urls_tecnocasa)


properties_urls_spain = detailUrls(filtered_urls)

csvExport(urls_tecnocasa, "pruebas/url_tecnocasa.csv")


data_ejemplo = dataExtraction('https://www.tecnocasa.es/venta/piso/valladolid/valladolid/598033.html')  

csvExport(data_ejemplo, "pruebas/piso_valladolid_unitario.csv")


properties_urls_valladolid = filterUrlsByLocation(properties_urls_spain, location_type='ciudad', location_value='Valladolid')

inmuebles_valladolid = pagesIteration(properties_urls_valladolid)

csvExport(inmuebles_valladolid, "dataset/inmuebles_valladolid.csv")

properties_spain = pagesIteration(properties_urls_spain)

csvExport(properties_spain, "dataset/inmuebles_espanna.csv")