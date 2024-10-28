from source.functions import webConnect
from source.functions import RobotsReading
from source.functions import userAgentRequests

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


htmlContent = webConnect(url)
if htmlContent:
    print("Connection successful and HTML obtained")
