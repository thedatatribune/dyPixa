import os
import requests
import hashlib
import json
import csv
from ColorExtraction import color_checker


def get_image(emotion, api_key, download_directory):
    # Define the search query
    query = f"{emotion} emotion"

    # Define the API endpoint
    endpoint = "https://api.unsplash.com/search/photos"

    # Set up the request headers with your API key
    headers = {
        "Authorization": f"Client-ID {api_key}"
    }

    # Parameters for the search
    params = {
        "query": query,
        "per_page": 10  # Number of images to fetch per emotion
    }

    # Send the request to the Unsplash API
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        images = []
        for i, image_info in enumerate(data["results"]):
            image_url = image_info["urls"]["regular"]
            image_hash = hashlib.md5(image_url.encode()).hexdigest()
            response = requests.get(image_url)

            if response.status_code == 200:
                with open(f"{download_directory}/{emotion}_{i}.jpg", "wb") as file:
                    file.write(response.content)
                images.append({"image_url": image_url, "image_hash": image_hash})
        return images
    return []


def make_csv(csv_dataset, file_path):
    with open(file_path, mode="w", newline="") as csv_file:
        fieldnames = ["emotion", "image_url", "image_hash"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_dataset)


def make_json(json_dataset, file_path):
    with open(file_path, "w") as json_file:
        json.dump(json_dataset, json_file, indent=4)


def create_emotion_dataset(api_key, emotions, download_directory):
    json_dataset = []
    csv_dataset = []

    for emotion in emotions:
        images = get_image(emotion, api_key, download_directory)

        if images:
            for image in images:
                image_url = image["image_url"]
                image_hash = image["image_hash"]

                # Process the downloaded image
                color_hues = color_checker(image_url, showImg=False)

                # Append the data to the CSV dataset
                csv_dataset.append({
                    "emotion": emotion,
                    "image_url": image_url,
                    "image_hash": image_hash
                })

                # Add data to the JSON dataset
                json_dataset.append({
                    emotion: {
                        image_hash: {
                            "HEX": color_hues,
                            "RGB": [tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for color in color_hues]
                        }
                    }
                })

        else:
            print(f"Failed to download images for {emotion}")

    make_csv(csv_dataset, "./data/emotion_dataset.csv")
    make_json(json_dataset, "./data/emotion_hues.json")
    print("Successfully completed")


# Replace these with your actual values
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
    "neutral",
    "surprise",
]

# Directory to save the downloaded images
download_directory = "emotion_images"

# Create the directory if it doesn't exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

create_emotion_dataset(UNSPLASH_API_KEY, emotions, download_directory)
