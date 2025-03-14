from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

def load_BLIP():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    return processor, model


def load_image(image):
    image = Image.open(image)
    return image

def process_image(processor, model, image):
    inputs = processor(images=image, return_tensors="pt")

    outputs = model.generate(**inputs, min_length=20, max_length=50, do_sample=True, temperature=0.05)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def process_caption(caption):
    words = nltk.word_tokenize(caption)
    post_class = nltk.pos_tag(words)

    nouns = [word for word, tag in post_class if tag.startswith('NN')]
    verbs = [word for word, tag in post_class if tag.startswith('VB')]
    adjectives = [word for word, tag in post_class if tag.startswith('JJ')]

    return nouns, verbs, adjectives

print("input file path: ")
image_path = input()

processor, model = load_BLIP()
image = load_image(image_path)
caption = process_image(processor, model, image)
n, v, a = process_caption(caption)

#we have now converted the caption to lists of nouns, verbs, and adjectives while maintaining the original caption
print(caption)
print(n,v,a)
