import requests
import time  # Don't forget to import the time module

def vicramcalc(role, url):
    port = "8081"
    server = "http://localhost:"
    url = url
    width = 1920
    height = 1800
    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0"
    explainRoles = False

    # In case of fails, limit retries to 3
    sleep_time = 2
    num_retries = 3

    for retry in range(0, num_retries):
        req = requests.post(server + port, json={
            "url": url,
            "width": width,
            "height": height,
            "agent": agent,
            "explainRoles": explainRoles
        })

        if req.status_code == 200:
            print("Success")
            print(req.json())  # Use req.json() to properly deserialize the JSON response
            last_whitespace_ratio = find_last_whitespace_ratio(req.json())
            return last_whitespace_ratio
            break
        else:
            print(f"Request failed (Attempt {retry + 1}/{num_retries})")
            if retry < num_retries - 1:
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Exiting.")

def find_last_whitespace_ratio(data):
    if isinstance(data, list):
        # If the data is a list, recursively call the function on the last element
        return find_last_whitespace_ratio(data[-1])
    elif isinstance(data, dict):
        # If the data is a dictionary, check if it contains the 'whiteSpaceRatio' key
        if 'whiteSpaceRatio' in data:
            return data['whiteSpaceRatio']
        else:
            # If not, recursively call the function on the values of the dictionary
            values = data.values()
            return find_last_whitespace_ratio(list(values)[-1])
    else:
        # If the data is neither a list nor a dictionary, return None
        return None

#role = "example_role"
#url = "https://www.chip.de/"
#score = vicramcalc(role, url)
#print("Your score :",score)
#
