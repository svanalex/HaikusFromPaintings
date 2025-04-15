# emotion_analysis.py
from collections import defaultdict
from .config import GOEMOTIONS_VAD, TRIGGER_WORD_GROUPS
from .model import emotion_classifier
from datetime import datetime

def get_trigger_group_hits(text, group_dict):
    """
    Returns a dictionary with group: [trigger words] that were found in the text.
    """
    hits = {}
    lowered = text.lower()
    for group, words in group_dict.items():
        found = [word for word in words if word in lowered]
        if found:
            hits[group] = found
    return hits

def get_trigger_multiplier(text, profile):
    group_hits = get_trigger_group_hits(text, TRIGGER_WORD_GROUPS)
    multiplier = 1.0

    for group, words in group_hits.items():
        group_sensitivity = profile.get("trigger_sensitivity", {}).get(group, 1.0)
        multiplier += group_sensitivity * len(words) * 0.1  # you can tune the 0.1 factor
        # print(f"Group: {group}, Words: {words}, Multiplier: {multiplier}")

    return multiplier, group_hits

def get_emotion_zone(valence, arousal):
    if abs(valence) < 0.05 and abs(arousal) < 0.05:
        return "flat_neutral"
    if valence >= 0.6 and arousal >= 0.7:
        return "high_pleasure_high_energy"
    if valence <= -0.5 and arousal >= 0.7:
        return "low_pleasure_high_energy"
    if valence <= -0.5 and arousal < 0.7:
        return "low_pleasure_low_energy"
    if valence >= 0.6 and arousal < 0.7:
        return "high_pleasure_low_energy"
    return "neutral_or_balanced"

# Process and score articles
def analyze_articles(articles, category="general", profile=None, verbose=False):
    article_results = []
    emotion_tally = defaultdict(int)
    weighted_emotions = defaultdict(float)
    all_vads = []
    developer_log = []

    for article in articles:
        title = article.get("title", "")
        description = article.get("description") or ""
        url = article.get("url", "")

        if len(description.split()) < 5:
            continue

        combined_text = f"{title}. {description}"
        emotions = emotion_classifier(combined_text[:512])[0]

        # Pick strongest non-neutral emotion
        top_emotion = next((e for e in emotions if e['label'] != "neutral"), emotions[0])
        label = top_emotion['label']
        score = top_emotion['score']
        valence, arousal = GOEMOTIONS_VAD.get(label, (0.0, 0.0))

        # Compute influence weight
        trigger_multiplier, triggers_hit = get_trigger_multiplier(combined_text, profile)

        article_category = article.get("category", "general")
        category_multiplier = profile["category_weights"].get(article_category, 1.0)

        influence_weight = score * trigger_multiplier * category_multiplier

        # Tally
        emotion_tally[label] += 1
        weighted_emotions[label] += influence_weight
        all_vads.append((valence, arousal, influence_weight))

        # Parse and standardize publication date
        raw_date = article.get("publishedAt", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            formatted_date = "unknown"

        article_results.append({
            "title": title,
            "url": url,
            "description": description,
            "category": category,
            "raw_emotion": label,
            "valence": round(valence, 2),   # raw VAD
            "arousal": round(arousal, 2),
            "confidence": round(score, 2),
            "influence_weight" : round(influence_weight, 3),
            "trigger_words": triggers_hit
        })

        if verbose:
            developer_log.append({
                "title": title,
                "raw_emotion": label,
                "confidence": round(score, 2),
                "vad": (valence, arousal),
                "trigger_words": triggers_hit,
                "category_multiplier": category_multiplier,
                "influence_weight": round(influence_weight, 3),
                "published_at": formatted_date
            })

    return article_results, emotion_tally, weighted_emotions, all_vads, developer_log


