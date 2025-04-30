import os
from components.emotion_engine.engine import run_emotion_engine
from components.image_analysis import analyze_image
from components.prompt_engineering.prompt_generator import generate_haiku_prompt
from components.haiku_generator.llama_haiku_generator import generate_haiku
from components.evaluator.evaluator import haikuEvaluation
from components.evaluator.evaluator import syllable_counter
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
    # Step 3: Combine into interpretive prompts
    final_emotion = mood_result["final_emotion"]
    prompt, style = generate_haiku_prompt(image_features, final_emotion, prompt_template)
    # separate into system instructions and prompts

    # Step 4: Generate haikus from prompts

    #NOTE: we have only generated one haiku from a random prompt for now. We need to refactor this to iterate over all prompts and generate 5 total haikus. Testing below code runs properly using garbage data plus one real prompt
    haikus = [generate_haiku(prompt) for _ in range(5)]

    # Step 5: Evaluation placeholder (currently returns all)
    #step 1: syllable count. This should return the top 3 haikus based on syllable count
    haiku_eval = haikuEvaluation()
    syllable_eval = syllable_counter()
    evaluated_haikus = []
    for haiku in haikus:
        sen = syllable_eval.syll_sentence(haiku)
        haiku = syllable_eval.extract_flexible_haikus(sen)
        evaluated_haikus.append(haiku)

    scores = []
    for i in range(5):
        scores.append(syllable_eval.score_haiku(evaluated_haikus[i][0][1]))

    for i in range(2):
        min_score = min(scores)
        min_index = scores.index(min_score)
        scores.pop(min_index)
        evaluated_haikus.pop(min_index)

    best_haiku = haiku_eval.model_evaluation(haikus)
    
    print("best haiku", best_haiku)
    
    # best_haiku, feedback = evaluate_haikus(haikus, context=mood_report)

    return {
        "haiku": haikus,
        "best_haiku": best_haiku,
        #"feedback": feedback,
        "mood": mood_result,
        "prompt": prompt,
        "image_features": image_features
    }