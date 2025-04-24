import os
from components.emotion_engine.engine import run_emotion_engine
from components.image_analysis import analyze_image
from components.prompt_engineering.prompt_generator import generate_haiku_prompt
from components.haiku_generator.llama_haiku_generator import generate_haiku
#from components.eval.haiku_evaluator import evaluate_haikus (to be implemented)


def generate_emotionally_influenced_haiku(image_path, profile_name, news_api_key, total_articles=15, use_single_day=False, mood_strategy="hybrid", prompt_template=None, include_dev_log=False):
    """
    Main orchestrator function that:
    1. Gathers emotional context from news
    2. Analyzes the uploaded image
    3. Engineers prompts from both sources
    4. Generates haikus via LLM (e.g., LLaMA via Groq API)
    5. Optionally returns haikus and context
    """

    # Step 1: Run emotion engine
    mood_report, dev_report = run_emotion_engine(
        profile_name=profile_name,
        api_key=news_api_key,
        total_articles=total_articles,
        use_single_day=use_single_day,
        include_dev_log=include_dev_log,
        mood_strategy=mood_strategy
    )
    mood_result = mood_report

    if not mood_result or "final_emotion" not in mood_result:
        raise ValueError("Failed to generate mood report. Please check emotion engine output.")

    # Step 2: Run image analysis
    image_features = analyze_image(image_path)  # { colors, objects, composition, etc }
    print(image_features)
    # Step 3: create mood bias
    final_emotion = mood_result["final_emotion"]

    # Step 4: Generate 5 prompts and haikus
    template_types = ["instructional", "contextual", "role_based", "example_driven", "iterative"]
    all_haikus = {}

    for template_type in template_types:
        print(f"\n🧠 Generating for template: {template_type}")
    
        prompt, _ = generate_haiku_prompt(image_features, final_emotion, template_type)
        haiku = generate_haiku(prompt)

        all_haikus[template_type] = {
            "prompt": prompt,
            "haiku": haiku
        }

    # Step 5: Evaluation placeholder (currently returns all)
    # best_haiku, feedback = evaluate_haikus(haikus, context=mood_report)

    return {
        "haiku": haiku,
        #"best_haiku": best_haiku,
        #"feedback": feedback,
        "mood": mood_result,
        "prompt": prompt,
        "image_features": image_features
    }