import os
import numpy as np
import cv2
from sklearn.cluster import KMeans
import requests
from io import BytesIO
import matplotlib.pyplot as plt


def load_image(input_source):
    """
    Load an image from either a URL or a local file.
    """
    try:
        if input_source.startswith(('http://', 'https://')):
            # Download the image from the URL
            response = requests.get(input_source)
            response.raise_for_status()  # Raise an exception for bad requests
            image_data = BytesIO(response.content)
            img = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), -1)
        else:
            # Read the image from a local file
            img = cv2.imread(input_source)

        return img

    except requests.exceptions.HTTPError as errh:
        raise ValueError(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise ValueError(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        raise ValueError(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        raise ValueError(f"Something went wrong: {err}")


def extract_dominant_colors(image, num_colors=5):
    # Convert the image from BGR to RGB (OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Flatten the image to a list of RGB tuples
    pixels = img_rgb.reshape(-1, 3)

    # Perform K-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_

    # Convert RGB to hex format
    hex_colors = ['#' + ''.join(f'{int(channel):02x}' for channel in color) for color in dominant_colors]

    return hex_colors


####   serving app
def color_checker(image_path=None, printCol=False, showImg=True):
    try:
        if image_path is None:
            # Ask user for the image URL or file path
            input_source = input("Enter the image URL or file path: ")

        # Load the image from URL or file
        img = load_image(input_source)

        # Check if the image was successfully loaded
        if img is None:
            raise ValueError("Could not open or find the image. Please check the URL or file path.")

        # Extract dominant colors
        dominant_colors = extract_dominant_colors(img, 5)
        col = []

        # Display the dominant colors and their hex values
        for i, color in enumerate(dominant_colors, start=1):
            col.append(color)
            if printCol:
                print(f"Dominant Color {i}: {color}")

        if showImg:
            # Display the image
            plt.imshow(img)
            plt.axis('off')
            plt.show()

        ## returning
        return col

    except ValueError as e:
        print(str(e))
        return False



# ## HOW TO USE?
# if __name__ == "__main__":
#   # test run
#   # color_checker()
