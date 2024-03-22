import subprocess
import json

def get_effective_image_sizes(webpage_url, screen_size):
    try:
        process = subprocess.Popen(['node', 'relativeImageSize.js', webpage_url, str(screen_size[0]), str(screen_size[1])], stdout=subprocess.PIPE)
        output, _ = process.communicate()

        image_data = json.loads(output)

        return image_data
    except Exception as e:
        print(f"Error: {e}")
        return []

