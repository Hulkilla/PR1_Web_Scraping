from functions import RobotsReading
from functions import userAgentRequests
from functions import dataExtraction
from functions import tecnocasaWebpages
from functions import urlsFilter
from functions import detailUrls
from functions import csvExport
from functions import filterUrlsByLocation
from functions import pagesIteration


url = "https://www.tecnocasa.es/"

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


data_ejemplo = dataExtraction('https://www.tecnocasa.es/venta/piso/valladolid/valladolid/598033.html')  

csvExport(data_ejemplo, "dataset/apartment_valladolid.csv")


properties_urls_valladolid = filterUrlsByLocation(properties_urls_spain, location_type='ciudad', location_value='Valladolid')

inmuebles_valladolid = pagesIteration(properties_urls_valladolid)

csvExport(inmuebles_valladolid, "dataset/properties_valladolid.csv")

properties_spain = pagesIteration(properties_urls_spain)

csvExport(properties_spain, "dataset/properties_Spain.csv")
