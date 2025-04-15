# components/image_analysis/image_analysis.py

from .color_analysis import analyze_colors
from .caption_creation import analyze_caption

def analyze_image(image_path):
    color_info = analyze_colors(image_path)
    caption_info = analyze_caption(image_path)

    return {
        "caption": caption_info["caption"],
        "nouns": caption_info["nouns"],
        "verbs": caption_info["verbs"],
        "adjectives": caption_info["adjectives"],
        "color_names": color_info["color_names"],
        "top_color": color_info["top_color"],
        "num_color_clusters": color_info["num_clusters"]
    }
