from collections import Counter
from .config import PERSONALITY_SUMMARIES
from .mood_report import get_emotion_influencers, get_top_overall_influencers, get_top_emotion_scores

def print_category_distribution(articles):
    category_distribution = Counter([a["category"] for a in articles])
    print("\n Article Distribution by Category:")
    for cat, count in category_distribution.items():
        print(f"  - {cat.title()}: {count} articles")

def generate_mood_explanation_report(mood_report):
    final_emotion = mood_report["final_emotion"]
    valence = mood_report["valence"]
    arousal = mood_report["arousal"]
    profile = mood_report["active_profile"]

    top_emotion_articles = mood_report.get("top_articles", [])
    top_overall_articles = mood_report.get("top_overall_influencers", [])
    top_emotion_scores = mood_report.get("top_emotion_scores", [])

    def describe_valence_old(val):
        if val > 0.6:
            return "very positive"
        elif val > 0.2:
            return "somewhat positive"
        elif val < -0.6:
            return "very negative"
        elif val < -0.2:
            return "somewhat negative"
        else:
            return "emotionally neutral"

    def describe_arousal(ar):
        if ar > 0.8:
            return "highly energized"
        elif ar > 0.5:
            return "moderately alert"
        elif ar < 0.3:
            return "calm and subdued"
        else:
            return "mildly active"

    valence_desc = describe_valence_old(valence)
    arousal_desc = describe_arousal(arousal)

    # --- Final Emotion Influencers ---
    emotion_article_str = "\n".join(
        f"• \"{a['title']}\" (weight: {round(a['influence_weight'], 3)}, confidence: {a['confidence']})"
        for a in top_emotion_articles
    ) if top_emotion_articles else "No articles clearly aligned with this emotion."

    # --- Top Overall Influencers ---
    top_article_str = "\n".join(
        f"• \"{a['title']}\" → {a['raw_emotion']} (weight: {round(a['influence_weight'], 3)})"
        for a in top_overall_articles
    ) if top_overall_articles else "No highly influential articles found."

    # --- Emotion Scores Summary ---
    top_emotion_str = "\n".join(
        f"• {emo}: {round(score, 3)}"
        for emo, score in top_emotion_scores
    ) if top_emotion_scores else "No emotions scored above threshold."

    explanation = (
        f"**Emotional Self-Assessment**\n\n"
        f"As a **{profile}**-oriented personality, I interpreted the news with a lens sensitive to certain emotional traits.\n\n"
        f"My current mood is **{final_emotion}**, formed by news that felt **{valence_desc}** and **{arousal_desc}**.\n\n"
        f"---\n\n"
        f"**Top Articles Driving the Mood ({final_emotion})**\n{emotion_article_str}\n\n"
        f"**Other Influential Articles**\n{top_article_str}\n\n"
        f"**Top Emotion Scores Considered**\n{top_emotion_str}\n\n"
        f"These insights contributed to my emotional state."
    )

    return explanation

def generate_mood_explanation_narrative(mood_report):
    final_emotion = mood_report["final_emotion"]
    valence = mood_report["valence"]
    arousal = mood_report["arousal"]
    profile = mood_report["active_profile"]

    top_emotion_articles = mood_report.get("top_articles", [])
    top_overall_articles = mood_report.get("top_overall_influencers", [])
    top_emotion_scores = mood_report.get("top_emotion_scores", [])

    def describe_valence(val):
        if val > 0.6: return "very positive"
        elif val > 0.2: return "somewhat positive"
        elif val < -0.6: return "very negative"
        elif val < -0.2: return "somewhat negative"
        else: return "emotionally neutral"

    def describe_arousal(ar):
        if ar > 0.8: return "highly energized"
        elif ar > 0.5: return "moderately alert"
        elif ar < 0.3: return "calm and subdued"
        else: return "mildly active"

    valence_desc = describe_valence(valence)
    arousal_desc = describe_arousal(arousal)

    summary_lines = []
    for a in top_emotion_articles:
        line = f'One key article, titled "{a["title"]}", contributed to this mood by evoking **{a["raw_emotion"]}** with a confidence of {a["confidence"]}, and was classified as especially impactful.'
        description = a.get("description")
        if description and len(description) > 20:
            line += f" It discussed: {a['description'][:200].rstrip()}..."
        summary_lines.append(line)

    top_score_lines = [f"{emo} ({round(score, 2)})" for emo, score in top_emotion_scores]

    explanation = (
        f"My current mood is **{final_emotion}**, shaped by recent readings, this emotion emerged as the dominant response based on emotional signals from the most impactful articles I read. On a valence-arousal scale this feeling can be categorized as **{valence_desc}** and **{arousal_desc}**.\n\n"
        f"As a **{profile}**-oriented personality, I give more weight to particular emotional tones and categories. "
        f"This led certain news articles to resonate more deeply.\n\n"
        f"{' '.join(summary_lines)}\n\n"
        f"In addition to these, other highly influential articles expressed emotions like "
        f"{', '.join([f'{a['raw_emotion']} (“{a['title']}”)' for a in top_overall_articles if a not in top_emotion_articles])}.\n\n"
        f"Based on my internal scoring, the most dominant emotional signals detected were: "
        f"{', '.join(top_score_lines)}."
    )

    return explanation

def generate_system_explanation_report():
    explanation = (
        "This system simulates a form of emotional context-setting by reading and evaluating real-world news articles.\n\n"
        "1. **Personality Profiles**: The system is governed by a personality model (e.g., melancholic, exuberant, curious) that defines its sensitivity to certain emotions, emotional zones, and content categories.\n\n"
        "2. **News Intake**: It reads 15 total articles from various categories (e.g., politics, tech, sports). The number of articles per category is determined by the personality's category preferences.\n\n"
        "3. **Emotion Classification**: Each article's title and description are passed to a language model trained on the GoEmotions dataset to detect nuanced emotional signals.\n\n"
        "4. **Emotion Scoring**: For every article, the system calculates an influence score based on:\n"
        "   - Emotion classification confidence\n"
        "   - Trigger words from grouped emotion categories (fear, grief, joy, hope)\n"
        "   - The weight the personality assigns to that content category\n\n"
        "5. **Mood Formation**: The system computes a weighted average of all valence-arousal pairs and determines which emotion has the strongest weighted impact, adjusting for personality preferences. The dominant emotion becomes the system's temporary emotional state.\n\n"
        "The result is a mood report that includes a raw emotional score, a human-readable explanation, and framing data. This mood influences how the LLM might respond in further interactions, serving as a dynamic emotional context."
    )
    return explanation

def generate_system_explanation(mood_report):
    profile_name = mood_report["active_profile"]
    profile_summary = PERSONALITY_SUMMARIES.get(profile_name, "No summary available.")
    return f"""
This system simulates a dynamic emotional model influenced by real-world news input.

**Current Personality Profile: {profile_name.capitalize()}**
{profile_summary}

This profile influences the system’s:
- **Emotional Biases** (through zone_weights and trigger_sensitivity)
- **News Preferences** (via category_weights)
- **Decision Heuristics** (hybrid blending and frequency scaling)

**Process Overview**:
1. **Article Intake**: News from six categories is selected and weighted by personality.
2. **Emotion Detection**: Each article is analyzed for emotion using GoEmotions + trigger word sensitivity.
3. **Mood Formation**: Articles influence mood via weighted scores combining emotion confidence, trigger sensitivity, category weight, and emotional zone.
4. **Strategy Logic**: The final mood is determined by a personality-informed strategy (e.g., weighted average, hybrid, or max influence).
5. **Narrative Generation**: A reflective explanation is generated with contextual insights.

The system adapts dynamically based on the personality traits selected.
"""

def format_llm_ready_report(mood_report):
    final_emotion = mood_report["final_emotion"]
    narrative_explanation = mood_report["narrative_explanation"]
    system_explanation = mood_report.get("system_explanation", "System explanation not provided.")
    profile_name = mood_report["active_profile"]
    profile_summary = PERSONALITY_SUMMARIES.get(profile_name, "No summary available for this profile.")

    formatted = {
          "final_emotion": final_emotion,
          "personality_profile": profile_name,
          "profile_summary": profile_summary,
          "narrative_explanation": narrative_explanation,
          "system_explanation": system_explanation
    }
    return formatted


