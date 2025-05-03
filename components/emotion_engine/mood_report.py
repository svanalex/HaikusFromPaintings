from .config import GOEMOTIONS_VAD
from .emotion_analysis import get_emotion_zone

def generate_mood_report(
    articles,
    emotion_tally,
    weighted_emotions,
    all_vads,
    profile,
    developer_log=None,
    mood_strategy="hybrid"
):
    if not all_vads:
        return {
            "final_emotion": "neutral",
            "valence": 0.0,
            "arousal": 0.0,
            "summary": "No emotional signal detected.",
            "top_articles": [],
            "emotion_log": dict(emotion_tally),
            "developer_log": developer_log or [],
            "active_profile": "none",
            "mood_strategy": mood_strategy
        }

    # Step 1: Score emotions using personality profile parameters
    emotion_scores = score_emotions(weighted_emotions, emotion_tally, profile)

    # Step 2: Determine final emotion based on strategy
    final_emotion, emotion_scores = select_final_emotion(
        emotion_scores, articles, mood_strategy, profile
    )
    #print(articles)
    # Step 3: Select top articles that contributed to the final emotion
    top_articles = get_emotion_influencers(articles, final_emotion)
    top_overall_influencers = get_top_overall_influencers(articles, top_articles)
    top_emotion_scores = get_top_emotion_scores(emotion_scores)

    # Step 4: Construct natural language summary
    reasons = [
        f"- '{a['title']}' (emotion: {a['raw_emotion']}, confidence: {a['confidence']}, triggers: {a.get('trigger_words', {})})"
        for a in top_articles
    ]
    reason_text = "\\n".join(reasons)
    summary = (
        f"The system felt predominantly '{final_emotion}' today.\\n"
        f"Most influential articles:\\n{reason_text}"
    )

    # Step 5: Add developer transparency info
    if developer_log is not None:
        developer_log.append({
            "final_emotion_scores": emotion_scores,
            "final_selected_emotion": final_emotion
        })

    # Final mood report dictionary
    return {
        "final_emotion": final_emotion,
        "valence": GOEMOTIONS_VAD.get(final_emotion, (0.0, 0.0))[0],
        "arousal": GOEMOTIONS_VAD.get(final_emotion, (0.0, 0.0))[1],
        "summary": summary,
        "top_articles": top_articles,
        "top_overall_influencers": top_overall_influencers,
        "top_emotion_scores": top_emotion_scores,
        "emotion_log": dict(emotion_tally),
        "developer_log": developer_log or [],
        "active_profile": profile.get("name", "unknown"),
        "mood_strategy": mood_strategy
    }


def score_emotions(weighted_emotions, emotion_tally, profile):
    import math
    freq_boost_factor = profile.get("decision_parameters", {}).get("freq_boost_factor", 0.1)
    emotion_scores = {}
    for emotion, influence in weighted_emotions.items():
        base_zone = get_emotion_zone(*GOEMOTIONS_VAD.get(emotion, (0.0, 0.0)))
        zone_weight = profile["zone_weights"].get(base_zone, 1.0)
        freq = emotion_tally[emotion]
        frequency_scaling = 1 + freq_boost_factor * math.log(1 + freq)
        emotion_scores[emotion] = influence * zone_weight * frequency_scaling
    return emotion_scores


def select_final_emotion(emotion_scores, articles, mood_strategy, profile):
    hybrid_blend_weight = profile.get("decision_parameters", {}).get("hybrid_blend_weight", 0.5)
    default_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]

    if mood_strategy == "max_influence":
        max_entry = max(
            (entry for entry in articles if isinstance(entry, dict) and "influence_weight" in entry),
            key=lambda x: x["influence_weight"],
            default=None
        )
        return max_entry["raw_emotion"] if max_entry else default_emotion, emotion_scores

    elif mood_strategy == "hybrid":
        max_entry = max(
            (entry for entry in articles if isinstance(entry, dict) and "influence_weight" in entry),
            key=lambda x: x["influence_weight"],
            default=None
        )
        if max_entry:
            dominant_emotion = max_entry["raw_emotion"]
            if dominant_emotion in emotion_scores:
                emotion_scores[dominant_emotion] = (
                    (1 - hybrid_blend_weight) * emotion_scores[dominant_emotion] +
                    hybrid_blend_weight * max(emotion_scores.values())
                )
        return max(emotion_scores.items(), key=lambda x: x[1])[0], emotion_scores

    return default_emotion, emotion_scores



def get_top_overall_influencers(articles, top_mood_articles=None, top_n=5):
    exclude_titles = {a["title"] for a in (top_mood_articles or [])}

    filtered = [
        entry for entry in articles
        if isinstance(entry, dict)
        and "influence_weight" in entry
        and entry.get("title") not in exclude_titles
    ]

    return sorted(filtered, key=lambda x: x["influence_weight"], reverse=True)[:top_n]


def get_emotion_influencers(articles, final_emotion, top_n=5):
    matching = [
        entry for entry in articles
        if isinstance(entry, dict)
        and entry.get("raw_emotion") == final_emotion
        and "influence_weight" in entry
    ]
    return sorted(matching, key=lambda x: x["influence_weight"], reverse=True)[:top_n]


def get_top_emotion_scores(emotion_scores, top_n=5):
    return sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]



