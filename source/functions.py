import requests
from bs4 import BeautifulSoup
import json
import time
import random
import csv
import os
import logging
import sys

log_format = '[%(process)d]\t%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
handlers=[logging.StreamHandler(sys.stdout)])

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
            logging.info(f"Error: Could not access robots.txt file of {url}, status code {response.status_code}")
            return None
    except Exception as e:
        logging.info(f"An error occurred while accessing robots.txt {e}")
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
        logging.info("The User-Agent used in the requests:", HEADERS["User-Agent"])
        return None
    else:
        logging.info(f"Error {response.status_code}: It could not connect to {url}")
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
        url_connected = requests.get(url, headers = HEADERS)
        if url_connected.status_code == 200:
            logging.info(f"Established connection of {url}")
            return url_connected.text
        else:
            logging.info(f"Error: Could not connect to the website {url}, code: {url_connected.status_code}")
            return None
    except Exception as e:
        logging.info(f"An error occurred while connecting: {e}")
        return None



def tecnocasaWebpages(url, delay_min=1, delay_max=3):
    """
    This function connects to a specified Tecnocasa web page URL, retrieves its HTML content,
    and extracts categorized property links such as 'Pisos en venta' and 'Casas en venta'.
       
    Args:
    - url (str): Web page URL as a string.
    - delay_min (float): Minimum wait time between retries (in seconds).
    - delay_max (float): Maximum wait time between retries (in seconds).

    Returns:
    - dict: A dictionary with categories as keys (e.g., 'Pisos en venta') and values as lists of
      dictionaries, each containing 'name' (str) for the link text and 'url' (str) for the link.
      Returns None if there is an error connecting to the page.
    """

    html_content = webConnect(url)
        
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        
        categories = {}
        
        for section in soup.find_all("div", class_="static-block p-2 flex-fill"):
            # Extract category name from <h2> header
            category_name = section.find("h2").get_text(strip=True)
            
            # Extract links and their names
            links = []
            for item in section.find_all("li"):
                link = item.find("a")
                text = link.get_text(" ", strip=True) 
                url = link["href"] 
                links.append({"name": text, "url": url})
            
            categories[category_name] = links
        
        delay = random.uniform(delay_min, delay_max)
        logging.info(f"Waiting {delay:.2f} seconds before next request.")
        time.sleep(delay)
        
        return categories
    else:
        logging.info("An error occurred while connecting")
        return None 



def urlsFilter(categories, keywords = ['en venta', 'en alquiler']):
    """
    Filters the URLs based on specified keywords in the 'name' field.
    
    Args:
    - categories (dict): Dictionary with category names as keys and list of URLs with names as values.
    - keywords (list): List of keywords to search in 'name' field for filtering.
    
    Returns:
    - list: A list of URLs (str) that match the keyword criteria.
    """
    filtered_urls = []
    for category, links in categories.items():
        for link in links:
            if any(keyword.lower() in link['name'].lower() for keyword in keywords):
                filtered_urls.append(link['url'])
    return filtered_urls



def detailUrls(urls, delay_min=1, delay_max=2):
    """
    This function takes a list of URLs of webpages containing property listings, 
    makes HTTP GET requests to those URLs, extracts the JSON data 
    containing property details, and returns a list of URLs for each property detail page.

    Parameters:
    urls (list): A list of URLs to scrape.

    Returns:
    list: A list of property detail URLs.
    """
    all_detail_urls = []  # Initialize a list for all detail URLs

    for url in urls:
        try:
            html_content = webConnect(url)
        
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")

            # Find the block containing the estate information
            json_data_script = soup.find("estates-index")
            json_text = json_data_script[':estates'] if json_data_script else None
            
            # Return an empty list if JSON was not found
            if json_text is None:
                logging.info(f"No detailed webs found for {url}.")
                continue

            # Load the JSON
            id_finder = json.loads(json_text)
            
            # Extract detail URLs
            detail_urls = [property['detail_url'] for property in id_finder if 'detail_url' in property]
            all_detail_urls.extend(detail_urls)  # Add detail URLs to the main list

            delay = random.uniform(delay_min, delay_max)
            logging.info(f"Waiting {delay:.2f} seconds before next request.")
            time.sleep(delay)
        
        except requests.exceptions.RequestException as e:
            logging.info(f"Request error for {url}: {e}")
        except json.JSONDecodeError:
            logging.info(f"Error decoding JSON for {url}.")
    
    return all_detail_urls  # Return the combined list of detail URLs



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

    html_content = webConnect(url)
        
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
      
        json_data_script = soup.find("estate-show-v2")
        json_text = json_data_script[':estate'] if json_data_script else None


        # Convert JSON to a Python Dictionary
        if json_text:
            try:
                json_data = json.loads(json_text)
                # Data extraction
               
                property_data = {
                    "Reference":json_data.get("id"),
                    "Country":json_data.get("country"),
                    "Autonomous_Community": json_data.get("region", {}).get("title"),
                    "City": json_data.get("city", {}).get("title"),
                    "Zone": json_data.get("district", {}).get("title"),
                    "Street":json_data.get("address"),
                    "Contrat": json_data.get("contract", {}).get("title"),
                    "Bedrooms": json_data.get("rooms"),
                    "Surface": json_data.get("numeric_surface"),
                    "Bathrooms": json_data.get("bathrooms"),
                    "Property_Type": json_data.get("features", {}).get("category"),
                    "Elevator": json_data.get("features", {}).get("elevator"),
                    "Heating": json_data.get("features", {}).get("heating"),
                    "Floor": json_data.get("features", {}).get("floor"),
                    "Year_Construction": json_data.get("dates", {}).get("build_year"),
                    "Energy_Class":json_data.get("energy_data",{}).get("class"),
                    "Energy_Consumption": json_data.get("energy_data", {}).get("efficiency"),
                    "Sale_Price": json_data.get("numeric_price"),
                    "Publish_date": json_data.get("last_published_at")
                }  

                logging.info("Data extracted successfully") 
                return property_data
            except json.JSONDecodeError:
                logging.info("Error decoding JSON")
                return None
        else:
            logging.info("JSON data script not found")
            return None
    else:
        logging.info(f"An error occurred while connecting")
        return None



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



def pagesIteration(urls, delay_min=1, delay_max=2, max_empty_attempts=50):
    """
    Iterates through a list of URLs and extracts products from each one, respecting delay parameters.

    Args:
    - urls (list): List of URLs to extract data from.
    - delay_min (float): Minimum wait time between requests.
    - delay_max (float): Maximum wait time between requests.
    - max_empty_attempts (int): Maximum number of consecutive empty attempts before stopping extraction.

    Returns:
    - list: List of extracted products from all URLs.
    """
    products = []
    empty_attempts = 0
    
    for url in urls:
        logging.info(f"Extracting data from {url}")
        
        # Call the data extraction function for each URL
        products_page = dataExtraction(url)
        
        if products_page:
            if isinstance(products_page, dict):
                products.append(products_page)
            elif isinstance(products_page, list):
                products.extend(products_page)
            else:
                logging.info(f"Unexpected data format for {url}")
            empty_attempts = 0 
        else:
            empty_attempts += 1
            logging.info(f"No data found for {url}. Consecutive empty attempts: {empty_attempts}")
            
            if empty_attempts >= max_empty_attempts:
                logging.info("Too many consecutive empty attempts. Stopping extraction.")
                break  
        
        # Add a random delay between each request
        delay = random.uniform(delay_min, delay_max)
        logging.info(f"Waiting {delay:.2f} seconds before the next request.")
        time.sleep(delay)
    
    return products




def filterUrlsByLocation(links, location_type=None, location_value=None):
    """
    Filters property URLs based on specified location type and value.

    Args:
    - links (list): List of links.
    - location_type (str): Type of location ('provincia' or 'ciudad').
    - location_value (str): Value of the location (province or city name) of Spain.

    Returns:
    - list: List of URLs filtered by location and keywords.
    """
    filtered_urls = []
    for link in links:
            # Filter by keywords in the name
                url_parts = link.split('/')
                
                # Filter by province or city based on provided location type
                if location_type == "provincia" and url_parts[5].lower() == location_value.lower().replace(" ", "-"):
                    filtered_urls.append(link)
                elif location_type == "ciudad" and url_parts[6].lower() == location_value.lower().replace(" ", "-"):
                    filtered_urls.append(link)
                elif location_type is None:  # If no location specified, include all URLs filtered by keywords
                    filtered_urls.append(link)
    
    return filtered_urls



def csvExport(data, file_path="prueba.csv", header=None):
    """
    Exports various structures of JSON-like data to a CSV file.
    
    Args:
    - data (list or dict): Data in JSON format (list of dicts or dict of lists).
    - file_path (str): Complete path (folder + filename) where the CSV file will be saved.
    - header (list): Optional list of headers for the CSV file.
    """
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    try:
        rows = []

        if isinstance(data, dict):
            flattened_item = dictFlatten(data)
            rows.append(flattened_item)

        elif isinstance(data, dict):            
            for category, items in data.items():
                for item in items:
                    flattened_item = dictFlatten(item)
                    flattened_item['Category'] = category
                    rows.append(flattened_item)
        
        elif isinstance(data, list):
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

        logging.info(f"Exported to {file_path}")

    except Exception as e:
        logging.info(f"An error occurred while exporting data: {e}")



