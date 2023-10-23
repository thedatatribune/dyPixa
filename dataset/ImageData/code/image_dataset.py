import os
import requests
from ColorExtraction import color_checker  # Replace with your color extraction function
import csv

# Replace with your Unsplash API key
UNSPLASH_API_KEY = "TOKEN"  # insert your token

# List of emotions
emotions = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
    "neutral"
]

# Directory to save the downloaded images
download_directory = "emotion_images"

# Create the directory if it doesn't exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Initialize the dataset
emotion_dataset = []

# Fetch images for each emotion and process them
for emotion in emotions:
    # Define the search query
    query = f"{emotion} emotion"

    # Define the API endpoint
    endpoint = "https://api.unsplash.com/search/photos"

    # Set up the request headers with your API key
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_API_KEY}"
    }

    # Parameters for the search
    params = {
        "query": query,
        "per_page": 1  # Number of images to fetch per emotion
    }

    # Send the request to the Unsplash API
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        for i, image_info in enumerate(data["results"]):
            image_url = image_info["urls"]["regular"]
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(f"{download_directory}/{emotion}_{i}.jpg", "wb") as file:
                    file.write(response.content)

                # Process the downloaded image
                image_path = f"{download_directory}/{emotion}_{i}.jpg"

                # Call the color extraction function to get color hues
                color_hues = color_checker(image_path, showImg=False)

                # Append the data to the dataset
                emotion_dataset.append({
                    "emotion": emotion,
                    "color_hues": color_hues,
                    "image_url": image_url
                })
            else:
                print(f"Failed to download image for {emotion} - Image {i}")
    else:
        print(f"Failed to fetch images for {emotion}")

print("Downloaded images and extracted color hues for all emotions.")

# Define the path where you want to save the CSV file
csv_file_path = "emotion_dataset.csv"

# Write the dataset to a CSV file
with open(csv_file_path, mode="w", newline="") as csv_file:
    fieldnames = ["emotion", "color_hues", "image_url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for entry in emotion_dataset:
        writer.writerow(entry)

print(f"Dataset saved as {csv_file_path}.")

