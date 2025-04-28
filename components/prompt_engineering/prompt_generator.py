import random

def generate_haiku_prompt(image_data, emotion, template_type=None):
    # Extract fields from image_data
    nouns = image_data.get("nouns", [])
    adjectives = image_data.get("adjectives", [])
    colors = image_data.get("color_names", [])
    top_color = image_data.get("top_color", "a subtle shade")
    caption = image_data.get("caption", "")
    composition = image_data.get("composition", ["undefined"])  # optional future field
    colors_sentiment = image_data.get("colors_sentiment", adjectives[:2])  # fallback
    noun = nouns[0] if nouns else "image"


    prompt_templates = {
        "instructional": (
            "Create a haiku that embodies the {composition} of the painting. Use the feeling {emotion} as the emotional foundation, "
            "incorporate the emotions of {colors_sentiment}, and describe a {noun} from the painting. Avoid over-explanation; "
            "focus on evocative imagery and natural flow."
        ),
        "contextual": (
            "A painting portrays a scene with a composition of {composition}. The color sentiment analysis suggests it is {colors_sentiment}, "
            "and the focal objects include {noun}. Using these elements and with a mood bias of {emotion}, compose a haiku that "
            "is inspired by the painting's emotional and visual essence."
        ),
        "role_based": (
            "You are a seasoned haiku poet, deeply attuned to the interplay between art and poetry. A painting with a {composition} atmosphere, "
            "{colors_sentiment} emotional tones, and objects like {noun} stands before you. You are feeling {emotion} today, and it influences "
            "how this painting inspires you. Craft a haiku that captures its essence, using subtle and vivid language."
        ),
        "example_driven": (
            "I am going to give you an example haiku to learn from so that you can write an original haiku:\n"
            "Just use this example to learn the structure and poetic elements that create an effective haiku. Don't mimic its imagery in your original. —\n"
            "A world of dew,\n"
            "And within every dewdrop\n"
            "A world of struggle.\n"
            "—\n"
            "Now, I will give you details about a painting that will inspire your new haiku:\n"
            "Color Sentiment: {colors_sentiment}\n"
            "Objects: {noun}\n"
            "Composition: {composition}\n"
            "Mood: {emotion}\n"
            "Following the structure and style of the example, generate a new haiku inspired by this painting."
        ),
        "iterative": (
            "Step 1: Identify the dominant emotion and imagery in the painting based on "
            "colors ({colors_sentiment}), objects ({noun}), and composition ({composition}), "
            "consider the mood you have when you are looking at the painting ({emotion}).\n"
            "Step 2: Write a rough draft of a haiku that reflects these elements.\n"
            "Step 3: Refine the haiku by enhancing its imagery, flow, and emotional resonance.\n"
            "Step 4: Present the final haiku, ensuring it aligns with the painting’s artistic tone."
        )
    }

    # Choose the template
    if template_type is None:
        template_type = random.choice(list(prompt_templates.keys()))

    template = prompt_templates[template_type]

    noun = nouns[0] if nouns else "image"
    prompt = template.format(
        caption=caption,
        emotion=emotion,
        noun=noun,
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

