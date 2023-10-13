## Objective

This section stores data and code related to colors, images, and thumbnails.

### Code

The [`./code/`](./code/) directory serves as the repository for all the code related to images and data used to train the model for image and color generation.

1. [`ColorExtraction.py`](./code/ColorExtraction.py): This script takes an image path or URL and identifies the 5 most dominant colors within it. This solution utilizes the **KMeans clustering** method to recommend colors that can be later used for:

   - Creating datasets for colors
   - Generating abstract art/images
   - Designing solutions for mapping sentiment to image colors

2. [`Dominant-color.py`](./code/Dominant-color.py): This script takes an image (path) as input and filters out the most frequent color shades.
