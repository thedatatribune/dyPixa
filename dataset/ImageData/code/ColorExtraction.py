### library base
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt
import cv2

### supproting functions

def extract_dominant_colors(image_path, num_colors=5):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image from BGR to RGB (OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Flatten the image to a list of RGB tuples
    pixels = img_rgb.reshape(-1, 3)

    # Perform K-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_

    # Convert RGB to hex format
    hex_colors = ['#' + ''.join(f'{int(channel):02x}' for channel in color) for color in dominant_colors]

    return hex_colors

def colorChecker(image_path=None, printCol=False, showImg=True):
  if image_path is None:
    # Ask user for the image file path
    image_path = input("Enter the image file path: ")

  # Extract dominant colors
  dominant_colors = extract_dominant_colors(image_path)
  col = []

  # Display the dominant colors and their hex values
  for i, color in enumerate(dominant_colors, start=1):
    col.append(color)
    if printCol:
      print(f"Dominant Color {i}: {color}")

  if showImg:
    # Display the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
  
  ## returning
  return col



# ## HOW TO USE?
# if __name__ == "__main__":
#   # test run
#   colorChecker()