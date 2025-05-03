import random

def generate_haiku_prompt(image_data, emotion, template_type=None):
    # Extract fields from image_data with safe defaults
    nouns = image_data.get("nouns", [])
    adjectives = image_data.get("adjectives", [])
    colors = list(dict.fromkeys(image_data.get("color_names", [])))[:5]  # Fixed from "color_names" to match test data
    top_color = image_data.get("top_color", "a subtle shade")
    caption = image_data.get("caption", "")
    composition = image_data.get("composition", ["undefined"])
    colors_sentiment = image_data.get("colors_sentiment", adjectives[:2])
    noun = nouns[0] if nouns else "image"

    #TODO add dominant color to all prompts (make sure prompts have access to same info), find out why the colors aren't being listed in prompts

    # Define prompt templates
    prompt_templates = {
        "instructional": (
            "Create a haiku that embodies the caption description of a painting. That caption is '{caption}'. "
            "Use the feeling '{emotion}' as the emotional foundation, and incorporate one or more of these colors: '{colors}'."
            "The dominant color is '{top_color}'"
            "Avoid over-explanation; focus on evocative imagery and natural flow."
        ),
        "contextual": (
            "A painting is captioned as '{caption}'. The color analysis suggests it has these colors: '{colors}', and "
            "{top_color} is the most prominent color. Using these elements and with a mood bias of '{emotion}', compose a haiku that "
            "is inspired by the painting's emotional and visual essence."
        ),
        "role_based": (
            "You are a seasoned haiku poet, and your work is often inspired by artwork you encounter. You are admiring a painting described as: '{caption}'. "
            "The canvas is filled with the colors {colors}, with {top_color} being the strongest. You are feeling very {emotion} today, and it influences "
            "how this painting inspires you. Craft a haiku that captures the painting's essence and your current mood using subtle and vivid language."
        ),
        "example_driven": (
            "I am going to give you an example haiku to learn from so that you can write an original haiku:\n"
            "Just use this example to learn the structure and poetic elements that create an effective haiku. Don't mimic its imagery in your original. —\n"
            "A world of dew,\n"
            "And within every dewdrop\n"
            "A world of struggle.\n"
            "—\n"
            "Now, I will give you details about a painting that will inspire your new haiku:\n"
            "Colors: {colors}\n"
            "Main color: '{top_color}'\n"
            "Painting description: {caption}\n"
            "Your mood: {emotion}\n"
            "Following the structure and style of the example, generate a new haiku inspired by this painting and your mood."
        ),
        "iterative": (
            "Step 1: Identify the dominant emotion and imagery in the painting based on "
            "colors ({colors}), dominant color '{top_color}', and painting description ('{caption}').\n"
            "Consider the mood you have ({emotion}) as it will influence your interpretation.\n"
            "Step 2: Write a rough draft of a haiku that reflects these elements.\n"
            "Step 3: Refine the haiku by enhancing its imagery, flow, and emotional resonance.\n"
            "Step 4: Present the final haiku, ensuring it aligns with the painting’s artistic tone."
        )
    }

    # Choose or randomly select a template
    if template_type not in prompt_templates:
        template_type = random.choice(list(prompt_templates.keys()))

    template = prompt_templates[template_type]

    # Build and return the prompt
    prompt = template.format(
        caption=caption,
        emotion=emotion,
        noun=noun,
        colors=", ".join(colors),
        top_color=top_color,
        colors_sentiment=", ".join(colors_sentiment),
        composition=", ".join(composition)
    )

    return prompt, template_type

def build_emotion_classification_prompt(text):
    emotion_list = [
        "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire",
        "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy",
        "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise"#, "neutral"
    ]
    
    emotion_string = ", ".join(emotion_list)

    prompt = f"""You are an emotion classification assistant.

Analyze the following text and determine its **dominant emotion**.

You must select **only one** emotion from this list (there is no neutral):
[{emotion_string}]

Respond **only** with a pure JSON object, no explanations, no code formatting, no backticks.

Format:
{{
  "emotion": "<selected_emotion>",
  "confidence": <confidence_score_between_0_and_1>
}}

Text to classify:
\"{text}\"
"""

    return prompt

