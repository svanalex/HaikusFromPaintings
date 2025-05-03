from transformers import pipeline
from .emotion_analysis import get_emotion_zone, analyze_articles
from .news_fetcher import get_weighted_articles, determine_date_range
from .explanation_generator import print_category_distribution, generate_mood_explanation_narrative, generate_system_explanation, format_llm_ready_report
from .config import PERSONALITY_PROFILES
from .mood_report import generate_mood_report


def run_emotion_engine(profile_name: str, api_key: str, total_articles: int = 15, use_single_day: bool = False, include_dev_log: bool = False, mood_strategy: str = "hybrid"):
    """
    Runs the full emotion analysis pipeline using the given personality profile.

    Returns:
        - llm_context: A compact, readable summary dictionary with emotion, explanations, and metadata.
        - mood_report (optional): Full developer report with all raw computations (if include_dev_log=True).
    """
    # --- Load profile ---
    
    active_profile = PERSONALITY_PROFILES[profile_name]

    # --- Retrieve articles based on profile's category weighting ---
    start_date, end_date = determine_date_range(use_single_day=use_single_day)
    articles = get_weighted_articles(api_key, active_profile, total_articles, start_date, end_date, not use_single_day)
    print_category_distribution(articles)

    # --- Analyze emotions in retrieved articles ---
    article_results, emotion_tally, weighted_emotions, all_vads, dev_log = analyze_articles(
        articles=articles,
        profile=active_profile,
        verbose=include_dev_log
    )

    # --- Generate mood report with emotion zone logic ---
    mood_report = generate_mood_report(
        articles=article_results,
        emotion_tally=emotion_tally,
        weighted_emotions=weighted_emotions,
        all_vads=all_vads,
        profile=active_profile,
        developer_log=dev_log if include_dev_log else None,
        mood_strategy=mood_strategy
    )

    # --- Attach metadata and explanations ---
    mood_report["active_profile"] = profile_name
    mood_report["active_profile_details"] = active_profile
    mood_report["narrative_explanation"] = generate_mood_explanation_narrative(mood_report)
    mood_report["system_explanation"] = generate_system_explanation(mood_report)

    # --- Format LLM-ready context ---
    llm_context = format_llm_ready_report(mood_report)

    # Return clean context + optionally full report
    return llm_context, mood_report if include_dev_log else None

