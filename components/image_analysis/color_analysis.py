# components/image_analysis/color_analysis.py

import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import webcolors

#print(dir(webcolors))

HEX_NAME_MAP = [(webcolors.name_to_hex(name), name) for name in webcolors.names()]

def image_preprocess(image):
    """Resize and reshape the image into RGB pixels."""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    small_image = cv2.resize(image, (250, 250))
    small_pixels = small_image.reshape(-1, 3)
    return small_pixels


def get_dominant_colors(pixels):
    """Cluster image pixels and extract dominant RGB colors."""
    dbscan = DBSCAN(eps=4, min_samples=20, metric='euclidean')
    labels = dbscan.fit_predict(pixels)

    unique_labels = np.unique(labels)
    clusters = [pixels[labels == label] for label in unique_labels if label != -1]
    dominant_rgbs = [np.mean(cluster, axis=0).astype(int) for cluster in clusters]

    return dominant_rgbs


def closest_colour_name(rgb):
    """Find the closest color name using Euclidean distance."""
    min_distance = float("inf")
    closest_name = "unknown"
    for name in webcolors.names():
        try:
            r_c, g_c, b_c = webcolors.hex_to_rgb(webcolors.name_to_hex(name))
            distance = (r_c - rgb[0])**2 + (g_c - rgb[1])**2 + (b_c - rgb[2])**2
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        except ValueError:
            continue
    return closest_name


def rgb_to_color_name(rgb):
    try:
        return webcolors.rgb_to_name(tuple(rgb))
    except ValueError:
        # Fall back to closest color name based on Euclidean distance
        min_colors = {}
        for hex_code, name in HEX_NAME_MAP:
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
            distance = (r_c - rgb[0])**2 + (g_c - rgb[1])**2 + (b_c - rgb[2])**2
            min_colors[distance] = name
        return min_colors[min(min_colors.keys())]



def analyze_colors(image_path):
    """Extract dominant color names from an image file path."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at path: {image_path}")

    pixels = image_preprocess(image)
    dominant_rgbs = get_dominant_colors(pixels)
    color_names = [rgb_to_color_name(rgb) for rgb in dominant_rgbs]

    return {
        "color_names": color_names,
        "color_rgb_values": dominant_rgbs,
        "num_clusters": len(dominant_rgbs),
        "top_color": color_names[0] if color_names else "unknown"
    }
