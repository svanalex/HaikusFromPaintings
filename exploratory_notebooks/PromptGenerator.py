import random

# Example image analysis data
image_analysis = {
    "colors": ["dark blue", "gray", "black", "soft yellow"],
    "objects": ["cliff", "night sky", "wolf"],
    "composition": ["unbalanced"],
    "colors_sentiment": ["moody", "dull"]
}

# Function to generate haiku prompts
def generate_haiku_prompts(image_data, emotion):
    used_elements = {"colors": set(), "objects": set(), "composition": set(), "colors_sentiment": set()}
    prompts = []

    prompt_templates = {
        "instructional": (
            "Create a haiku that embodies the {composition} composition of the painting. Use the feeling {emotion} as the emotional foundation, "
            "incorporate the emotions of {colors_sentiment}, and describe a {object} from the painting. Avoid over-explanation; "
            "focus on evocative imagery and natural flow."
        ),
        "contextual": (
            "A painting portrays a scene with a composition of {composition}. The color sentiment analysis suggests it is {colors_sentiment}, "
            "and the focal objects include {object}. Using these elements and with a mood bias of {emotion}, compose a haiku that "
            "inspired by the painting's emotional and visual essence."
        ),
        "role_based": (
            "You are a seasoned haiku poet, deeply attuned to the interplay between art and poetry. A painting with a {composition} atmosphere, "
            "{colors_sentiment} emotional tones, and objects like {objects} stands before you. You are feeling {emotion} today, and it influences "
            "how this painting inspires you. Craft a haiku that captures its essence, using subtle and vivid language."
        ),
        "example_driven": (
            "I am going to give you an example hiaku to learn from so that you can write an original haiku:\n"
            "Just use this example to learn the structure and poetic elements that create an effective haiku. Don't mimic it's imagery in your original. —\n"
            "A world of dew,\n"
            "And within every dewdrop\n"
            "A world of struggle.\n"
            "—\n"
            "Now, I will give you details about a painting that will inspire your new haiku:\n"
            "Color Sentiment: {colors_sentiment}\n"
            "Objects: {object}\n"
            "Composition: {composition}\n"
            "Mood: {emotion}\n"
            "Following the structure and style of the example, generate a new haiku inspired by this painting."
        ),
        "iterative": (
            "Step 1: Identify the dominant emotion and imagery in the painting based on "
            "colors ({colors_sentiment}), objects ({object}), and composition ({composition}), "
            "consider the mood you have when you are looking at the painting ({emotion}).\n"
            "Step 2: Write a rough draft of a haiku that reflects these elements.\n"
            "Step 3: Refine the haiku by enhancing its imagery, flow, and emotional resonance.\n"
            "Step 4: Present the final haiku, ensuring it aligns with the painting’s artistic tone."
        )
    }

    # Distribute elements across the prompts to ensure full coverage
    color_cycle = iter(image_data["colors"])
    object_cycle = iter(image_data["objects"])

    for key, template in prompt_templates.items():
        # Get the next color and object, cycling back if needed
        color = next(color_cycle, random.choice(image_data["colors"]))
        object_ = next(object_cycle, random.choice(image_data["objects"]))

        used_elements["colors"].add(color)
        used_elements["objects"].add(object_)

        # Format the template
        prompt = template.format(
            emotion=emotion,
            object=object_,
            color=color,
            composition=", ".join(image_data["composition"]),  # Ensure composition is a string
            colors_sentiment=", ".join(image_data["colors_sentiment"]),
            objects=", ".join(image_data["objects"])
        )
        prompts.append(prompt)

    return prompts

# Example usage
emotion = "bored"
haiku_prompts = generate_haiku_prompts(image_analysis, emotion)
for prompt in haiku_prompts:
    print(prompt)
    print()
