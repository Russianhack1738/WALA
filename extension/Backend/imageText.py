import requests
from bs4 import BeautifulSoup

def calculate_image_text_ratio(response):
    try:
        # Fetch the HTML content of the webpage
       
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Count the number of image and text elements
        num_images = len(soup.find_all('img'))
        num_text_elements = len(soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'a', 'span', 'li', 'td']))

        # Calculate the image-to-text ratio
        image_text_ratio = num_text_elements / num_images   if num_images > 0 else 0

        return image_text_ratio

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

# Example usage
#url = "https://www.chip.de/"
#ratio = calculate_image_text_ratio(url)

#if ratio is not None:
   # print(f"Image-to-text ratio for {url}: {ratio}")
#else:
    #print("Failed to calculate image-to-text ratio.")

