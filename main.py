from source.functions import webConnect
from source.functions import RobotsReading
from source.functions import userAgentRequests
from source.functions import htmlToTXT
from source.functions import dataExtraction

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


htmlContent = webConnect('https://www.tecnocasa.es/venta/piso/valladolid/valladolid/598545.html')
if htmlContent:
    htmlToTXT(htmlContent, archive="prueba_tecnocasa.txt")
    print("Connection successful and HTML obtained")

data = dataExtraction('https://www.tecnocasa.es/venta/piso/valladolid/valladolid/598545.html')   
