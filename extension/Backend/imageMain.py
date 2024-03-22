import numpy as np
from scipy.stats import entropy
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_image_direct_urls(page_url):
    direct_urls = []
    # Fetch webpage content
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image elements
    image_elements = soup.find_all('img')

    # Extract direct URL of each image
    for img in image_elements:
        if 'src' in img.attrs:
            img_url = img['src']
            # Convert relative URL to absolute URL
            img_url = urljoin(page_url, img_url)
            direct_urls.append(img_url)

    return direct_urls

def calculate_normalized_entropy_from_url(image_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print("Error fetching image from URL:", e)
        return None

    # Read the image using PIL
    try:
        img = Image.open(BytesIO(response.content)).convert('L')
    except Exception as e:
        print("Error reading image:", e)
        return None

    # Convert PIL image to numpy array
    img_array = np.array(img)

    # Flatten the image into a 1D array
    flat_img = img_array.flatten()

    # Calculate histogram
    hist, _ = np.histogram(flat_img, bins=256, range=[0, 256])

    # Normalize histogram to get probability distribution
    prob_dist = hist / np.sum(hist)

    # Calculate Shannon's entropy
    entropy_value = entropy(prob_dist, base=2)

    # Normalize entropy to the range [0, 1]
    normalized_entropy = entropy_value / np.log2(len(prob_dist))

    print("Normalized Entropy:", normalized_entropy)
    print(" URL: ", image_url)

    return normalized_entropy
