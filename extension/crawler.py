import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    return base_url


def crawler(url):
    inner_urls = set()
    base_url = get_base_url(url)
    response = requests.get(url) # Getting URLs from here
    parse = BeautifulSoup(response.text, 'html.parser') # Using BS4 for parsing
    for link in parse.find_all('a', href=True): # Getting a tags with href and traversing them
        inner_url = link.get('href') # Get href attribute which contains URL actually
        inner_url = urljoin(url, inner_url) # Join the inner URL with the base URL
        if inner_url.startswith(base_url) and inner_url != url and inner_url != base_url and '#' not in inner_url: # Check if the URL starts with the base URL 
            inner_urls.add(inner_url) # Put into list

    return list(inner_urls)
