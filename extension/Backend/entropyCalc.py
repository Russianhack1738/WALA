from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import imagemain as im

def calculate_image(response,url):
    try:
        image_complexity = 0
        # Set a User-Agent header to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # Fetch the HTML content of the webpage with the headers
        
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')
        num_images = len(img_tags)
        print(num_images)

        for img_tag in img_tags:
            # Extract image URL from the img tag
            img_url = img_tag.get('src', '')
            entropy_value = im.calculate_normalized_entropy_from_url(urljoin(url, img_url))
            if entropy_value is not None and entropy_value != 0:
                image_complexity += entropy_value
            else:
                num_images = num_images - 1

        # Calculate average image complexity
        print(num_images)
        if num_images > 0:
            return image_complexity / num_images
        else:
            return 0  # To avoid division by zero if there are no images

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

