from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import threading
import textComp as tx
import imageText as it
import vicramCalc as vc
import whiteSpace as ws
import EntropyCalc as im
import requests
from selenium import webdriver

# Function to get screen size using Selenium
def get_screen_size():
    try:
        # Initialize a Selenium webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Open the browser window maximized
        driver = webdriver.Chrome(
            options=options)  # You may need to adjust this based on your browser and webdriver setup

        # Open a webpage
        driver.get('https://www.example.com')  # Open any webpage

        # Get window size
        window_size = driver.get_window_size()

        # Extract width and height
        width = window_size['width']
        height = window_size['height']

        # Close the webdriver
        driver.quit()

        return width, height
    except Exception as e:
        print("Error getting screen size:", e)
        return None


app = Flask(__name__)

cors = CORS(app)


@app.route('/')
def hello():
    return render_template('popup.html')


@app.route("/scan", methods=['GET'])
def Scan():
    result = {
        "Visual Complexity": 0,
        "Distinguishablity": 0,
        "Text Image Ratio": 0,
        "Text Complexity": 0,
        "Image Complexity": 0,
    }
    url = request.args.get('data1')
    visualcomp = request.args.get('data2')
    distin = request.args.get('data3')
    text_image = request.args.get('data4')
    textc = request.args.get('data5')
    image = request.args.get('data6')
    print("DATAA", url, visualcomp, distin, text_image, textc, image)
    response = requests.get(url)

    def calculate_visual_complexity():
        if visualcomp == "true":
            result["Visual Complexity"] = vc.vicramcalc1("example_role", url)
        else:
            result["Visual Complexity"] = "NA"

    def calculate_distinguishability():
        if distin == "true":
            result["Distinguishablity"] = ws.vicramcalc("example_role", url)
        else:
            result["Distinguishability"] = "NA"

    def calculate_text_image_ratio():
        if text_image == "true":
            result["Text Image Ratio"] = it.calculate_image_text_ratio(response)
        else:
            result["Text Image Ratio"] = "NA"

    def calculate_text_complexity():
        if textc == "true":
            result["Text Complexity"] = tx.text_complexity(response)
        else:
            result["Text Complexity"] = "NA"

    def calculate_image_complexity():
        if image == "true":
            screen_size = get_screen_size()
            if screen_size:
                response = requests.get(url)
                complexity_score = im.calculate_image_complexity(response, url, screen_size)
                result["Image Complexity"] = complexity_score
                print("Image Complexity score:", complexity_score)
            else:
                print("Failed to get screen size.")
        else:
            result["Image Complexity"] = "NA"

    threads = []
    threads.append(threading.Thread(target=calculate_visual_complexity))
    threads.append(threading.Thread(target=calculate_distinguishability))
    threads.append(threading.Thread(target=calculate_text_image_ratio))
    threads.append(threading.Thread(target=calculate_text_complexity))
    threads.append(threading.Thread(target=calculate_image_complexity))

    # Start Threads
    for thread in threads:
        thread.start()

    # Wait Threads
    for thread in threads:
        thread.join()

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

    # get methods as shown in CNG 445
