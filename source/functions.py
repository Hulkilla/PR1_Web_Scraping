import requests


def RobotsReading(url):
    """
    This function reads the robots.txt file of a website and returns its contents.
    
    Args:
    - url (str): Website URL (without `/robots.txt`).
    
    Returns:
    - str: The content of the robots.txt file or an error message.
    """

    url_robots = url.rstrip('/') + '/robots.txt'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }
    try:
        response = requests.get(url_robots, headers = headers)
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("The User-Agent used in the requests:", headers["User-Agent"])
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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }
    try:
        url = requests.get(url, headers = headers)
        if url.status_code == 200:
            return url.text
        else:
            print(f"Error: Could not connect to the website {url}, code: {url.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while connecting: {e}")
        return None