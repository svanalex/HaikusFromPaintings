import os
from components.emotion_engine.engine import run_emotion_engine
from components.image_analysis import analyze_image
from components.prompt_engineering.prompt_generator import generate_haiku_prompt
from components.haiku_generator.llama_haiku_generator import generate_haiku
from components.evaluator.evaluator import haikuEvaluation, syllable_counter
# from components.eval.haiku_evaluator import evaluate_haikus (to be implemented)


def generate_emotionally_influenced_haiku(image_path, profile_name, news_api_key, total_articles=15, use_single_day=False, mood_strategy="hybrid", prompt_template=None, include_dev_log=False):
    """
    Main orchestrator function that:
    1. Gathers emotional context from news
    2. Analyzes the uploaded image
    3. Engineers prompts from both sources
    4. Generates haikus via LLM (e.g., LLaMA via Groq API)
    5. Evaluates and returns the best haiku
    """

    # Step 1: Run emotion engine
    print("\n[Step 1] Running emotion engine...")
    mood_report, dev_report = run_emotion_engine(
        profile_name=profile_name,
        api_key=news_api_key,
        total_articles=total_articles,
        use_single_day=use_single_day,
        include_dev_log=include_dev_log,
        mood_strategy=mood_strategy
    )
    mood_result = mood_report
    print(f"Generated Mood Result:\n{mood_result}")

    if not mood_result or "final_emotion" not in mood_result:
        raise ValueError("Failed to generate mood report. Please check emotion engine output.")

    # Step 2: Run image analysis
    print("\n[Step 2] Running image analysis...")
    image_features = analyze_image(image_path)
    print(f"Extracted Image Features:\n{image_features}")

    # Step 3: Final emotion for prompt generation
    final_emotion = mood_result["final_emotion"]
    print(f"\n[Step 3] Final Emotion from News Context: {final_emotion}")

    # Step 4: Generate prompts and haikus for each template type
    template_types = ["instructional", "contextual", "role_based", "example_driven", "iterative"]
    haiku_collection = {}
    raw_haikus = []

    print("\n[Step 4] Generating prompts and haikus for each template type...")
    for template_type in template_types:
        print(f"\n-- Template Type: {template_type} --")
        prompt, _ = generate_haiku_prompt(image_features, final_emotion, template_type)
        print(f"Generated Prompt:\n{prompt}")
        haiku = generate_haiku(prompt)
        print(f"Generated Haiku:\n{haiku}")
        haiku_collection[template_type] = {
            "prompt": prompt,
            "haiku": haiku
        }
        raw_haikus.append(haiku)

    # Step 5: Evaluate haikus
    print("\n[Step 5] Evaluating haikus...")
    syll_eval = syllable_counter()
    haiku_eval = haikuEvaluation()

    structured_haikus = []
    for haiku in raw_haikus:
        lines = syll_eval.syll_sentence(haiku)
        extracted = syll_eval.extract_flexible_haikus(lines)
        structured_haikus.append(extracted[0][1])  # Take best syllable-matched version

    scores = [syll_eval.score_haiku(h) for h in structured_haikus]

    # Select top 3 haikus
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]
    top_haikus = [raw_haikus[i] for i in top_indices]

    best_haiku = haiku_eval.model_evaluation(top_haikus)

    print(f"\nBest Haiku:\n{best_haiku}")

    return {
        "mood": mood_result,
        "image_features": image_features,
        "haikus_and_prompts": haiku_collection,
        "top_haiku": best_haiku
    }
