# components/image_analysis/caption_analysis.py

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import nltk

nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def load_image(image_path):
    return Image.open(image_path).convert("RGB")

def generate_caption(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.generate(**inputs, min_length=20, max_length=50, do_sample=True, temperature=0.05)
    return processor.decode(outputs[0], skip_special_tokens=True)

def extract_semantics(caption):
    words = nltk.word_tokenize(caption)
    pos = nltk.pos_tag(words)
    nouns = [word for word, tag in pos if tag.startswith("NN")]
    verbs = [word for word, tag in pos if tag.startswith("VB")]
    adjectives = [word for word, tag in pos if tag.startswith("JJ")]
    return nouns, verbs, adjectives

def analyze_caption(image_path):
    image = load_image(image_path)
    caption = generate_caption(image)
    nouns, verbs, adjectives = extract_semantics(caption)
    return {
        "caption": caption,
        "nouns": nouns,
        "verbs": verbs,
        "adjectives": adjectives
    }
