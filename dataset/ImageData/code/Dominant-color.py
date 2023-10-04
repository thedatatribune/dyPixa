import cv2
import numpy as np
from collections import Counter


def extract_dominant_color(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image from BGR to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a list of pixels
    pixels = image.reshape(-1, 3)

    # Use Counter to count the frequency of each color
    color_counter = Counter(map(tuple, pixels))

    # Get the most common color
    most_common_color = color_counter.most_common(1)[0][0]

    # Convert the most common color to hex format
    hex_color = '#{:02X}{:02X}{:02X}'.format(*most_common_color)

    return hex_color


def main():
    image_path = ''  # Replace with the path to your input image

    dominant_color = extract_dominant_color(image_path)

    print(f"Top Dominant Color: {dominant_color}")


if __name__ == "__main__":
    main()
