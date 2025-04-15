#dependencies
import cv2
import numpy as np
import matplotlib.pyplot as plt
import webcolors
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt


# Build hex-to-name lookup once
HEX_NAME_MAP = [
    (webcolors.name_to_hex(name), name) for name in webcolors.CSS3_NAMES_TO_HEX
]

def rgb_to_color_name(rgb):
    """Convert RGB to closest known color name using Euclidean distance."""
    try:
        return webcolors.rgb_to_name(tuple(rgb))
    except ValueError:
        min_colors = {}
        for hex_code, name in HEX_NAME_MAP:
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
            distance = (r_c - rgb[0]) ** 2 + (g_c - rgb[1]) ** 2 + (b_c - rgb[2]) ** 2
            min_colors[distance] = name
        return min_colors[min(min_colors.keys())]


def image_preprocess(image):
  #image = cv2.imread("/content/ce8b9ee46fa699101c2d31f2b4a9622e.jpg")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  smallImage = cv2.resize(image, (250, 250))
  smallPixels = smallImage.reshape(-1, 3)
  return smallPixels


def get_dominant_colors(smallPixels):
  dbscan = DBSCAN(eps=4, min_samples=20, metric='euclidean')
  labels = dbscan.fit_predict(smallPixels)

  unique_labels = np.unique(labels)
  clusters = [smallPixels[labels == label] for label in unique_labels if label != -1]
  
  dominant_rgbs = [np.mean(cluster, axis=0).astype(int) for cluster in clusters]
  return dominant_rgbs, labels


def rgb_to_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        min_colors = {}
        for hex_code, name in HEX_NAME_MAP:
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
            distance = (r_c - rgb[0]) ** 2 + (g_c - rgb[1]) ** 2 + (b_c - rgb[2]) ** 2
            min_colors[distance] = name
        return min_colors[min(min_colors.keys())]


def get_dominant_colors(pixels):
    """Cluster image pixels and extract dominant RGB colors."""
    dbscan = DBSCAN(eps=4, min_samples=20, metric='euclidean')
    labels = dbscan.fit_predict(pixels)

    unique_labels = np.unique(labels)
    # Filter out noise cluster -1
    clusters = [pixels[labels == label] for label in unique_labels if label != -1]
    dominant_rgbs = [np.mean(cluster, axis=0).astype(int) for cluster in clusters]

    return dominant_rgbs, labels


def analyze_colors(image_path):
    """Main function to extract named dominant colors from an image."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at path: {image_path}")

    pixels = image_preprocess(image)
    dominant_rgbs, labels = get_dominant_colors(pixels)

    color_names = [rgb_to_color_name(rgb) for rgb in dominant_rgbs]

    top_color = color_names[0] if color_names else "unknown"
    num_clusters = len(dominant_rgbs)

    return {
        "color_names": color_names,
        "color_rgb_values": dominant_rgbs,
        "num_clusters": num_clusters,
        "top_color": top_color
    }