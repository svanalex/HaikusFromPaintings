#dependencies
import cv2
import numpy as np
import matplotlib.pyplot as plt
import webcolors
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

#note, these must be ran from terminal for dependencies
#pip install scikit-learn
#pip install webcolors



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
  dominant_colors = [smallPixels[labels == label].mean(axis=0) for label in unique_labels if label != -1]

  dominant_colors = np.array(dominant_colors, dtype="uint8")
  return dominant_colors

def rgb_to_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        min_colors = {}
        for hex_code, name in hex_names:
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
            distance = (r_c - rgb[0]) ** 2 + (g_c - rgb[1]) ** 2 + (b_c - rgb[2]) ** 2
            min_colors[distance] = name
        return min_colors[min(min_colors.keys())]

def colors_to_set(dominant_colors):
  color_set = set()
  for color in dominant_colors:
    color_set.add(rgb_to_color_name(color))
  return color_set

#okay run the whole thing now!
if __name__ == "__main__":

    hex_names = []
    for name in webcolors.names():
        hex_names.append([webcolors.name_to_hex(name), name]) 

    image = cv2.imread("C:\Users\alexs\OneDrive\Pictures\Wallpapers\ce8b9ee46fa699101c2d31f2b4a9622e.jpg")
    pixels = image_preprocess(image)
    dominant_colors = get_dominant_colors(pixels)
    color_set = colors_to_set(dominant_colors)
    print(color_set)