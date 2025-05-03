GOEMOTIONS_VAD = {
    "admiration": (0.7, 0.5),       # warm positivity, not intense
    "amusement": (0.8, 0.6),        # high pleasure, moderate arousal
    "anger": (-0.8, 0.9),           # strong negative, very high arousal
    "annoyance": (-0.4, 0.6),       # mildly negative, medium-high arousal
    "approval": (0.6, 0.4),         # positive, mild arousal
    "caring": (0.8, 0.4),           # high valence, low arousal empathy
    "confusion": (-0.3, 0.7),       # slightly negative, mentally activated
    "curiosity": (0.3, 0.8),        # slightly positive, highly active
    "desire": (0.7, 0.7),           # pleasant but motivationally intense
    "disappointment": (-0.6, 0.4),  # low valence, passive sadness
    "disapproval": (-0.6, 0.5),     # negative judgment, medium arousal
    "disgust": (-0.8, 0.7),         # strong aversion
    "embarrassment": (-0.5, 0.8),   # shameful but socially active
    "excitement": (0.9, 1.0),       # very positive, very high arousal
    "fear": (-0.9, 0.95),           # very negative, high survival arousal
    "gratitude": (0.8, 0.5),        # positive but not hyperactive
    "grief": (-0.9, 0.6),           # intense sadness, lower arousal than fear
    "joy": (0.95, 0.85),            # extremely positive, strong energy
    "love": (0.9, 0.6),             # deep positive feeling, calm activation
    "nervousness": (-0.5, 0.9),     # anxious activation
    "optimism": (0.8, 0.6),         # positive future orientation
    "pride": (0.7, 0.6),            # socially positive, mildly intense
    "realization": (0.2, 0.7),      # neutral-positive insight, mental activation
    "relief": (0.7, 0.3),           # high valence, low arousal
    "remorse": (-0.7, 0.6),         # moral sadness, shame
    "sadness": (-0.8, 0.5),         # core low-valence emotion, lower arousal than anger
    "surprise": (0.2, 0.9),         # highly activating, valence varies
    "neutral": (0.0, 0.0)           # baseline
}

PERSONALITY_PROFILES = {
    "melancholic": {
        "zone_weights": {
            "low_pleasure_low_energy": 2.0,
            "low_pleasure_high_energy": 1.7,
            "neutral_or_balanced": 0.5,
            "high_pleasure_low_energy": 0.4,
            "high_pleasure_high_energy": 0.3,
            "flat_neutral": 0.5
        },
        "trigger_sensitivity": {
          "fear": 1.6,
          "grief": 1.8,
          "joy": 0.5,
          "hope": 0.6
        },
        "category_weights": {
            "politics": 2.0,
            "general": 1.5,
            "business": 1.2,
            "technology": 1.0,
            "sports": 0.5,
            "entertainment": 0.6
        },
        "decision_parameters":{
            "hybrid_blend_weight": 0.6,
            "freq_boost_factor": 0.15
        }
    },
    "stoic": {
        "zone_weights": {
            "low_pleasure_low_energy": 0.8,
            "low_pleasure_high_energy": 0.7,
            "neutral_or_balanced": 1.2,
            "high_pleasure_low_energy": 1.1,
            "high_pleasure_high_energy": 0.9,
            "flat_neutral": 1.0
        },
        "trigger_sensitivity": {
            "fear": 0.6,
            "grief": 0.6,
            "joy": 0.8,
            "hope": 0.9
        },
        "category_weights": {
            "politics": 1.0,
            "general": 1.0,
            "business": 1.0,
            "technology": 1.0,
            "sports": 1.0,
            "entertainment": 1.0
        },
        "decision_parameters": {
            "hybrid_blend_weight": 0.95,
            "freq_boost_factor": 0.05
        }
    },
    "exuberant": {
        "zone_weights": {
            "high_pleasure_high_energy": 1.5,
            "high_pleasure_low_energy": 1.3,
            "neutral_or_balanced": 0.8,
            "low_pleasure_high_energy": 0.7,
            "low_pleasure_low_energy": 0.6,
            "flat_neutral": 0.4
        },
        "trigger_sensitivity": {
            "fear": 0.7,
            "grief": 0.6,
            "joy": 1.5,
            "hope": 1.4
        },
        "category_weights": {
            "entertainment": 1.2,
            "sports": 1.1,
            "technology": 1.0,
            "general": 1.0,
            "politics": 0.6,
            "business": 0.7
        },
        "decision_parameters": {
            "hybrid_blend_weight": 0.7,
            "freq_boost_factor": 0.25
        }
    },
    "curious": {
        "zone_weights": {
            "neutral_or_balanced": 1.4,
            "high_pleasure_low_energy": 1.2,
            "low_pleasure_high_energy": 1.0,
            "low_pleasure_low_energy": 0.9,
            "high_pleasure_high_energy": 1.0,
            "flat_neutral": 0.6
        },
        "trigger_sensitivity": {
            "fear": 1.0,
            "grief": 1.0,
            "joy": 1.1,
            "hope": 1.1
        },

        "category_weights": {
            "technology": 1.4,
            "general": 1.2,
            "politics": 1.0,
            "business": 0.8,
            "entertainment": 0.8,
            "sports": 0.7
        },
        "decision_parameters": {
            "hybrid_blend_weight": 0.85,
            "freq_boost_factor": 0.1
        }
    },
    "balanced": {
        "zone_weights": {
            "low_pleasure_low_energy": 1.0,
            "low_pleasure_high_energy": 1.0,
            "neutral_or_balanced": 1.0,
            "high_pleasure_low_energy": 1.0,
            "high_pleasure_high_energy": 1.0,
            "flat_neutral": 1.0
        },
        "trigger_sensitivity": {
            "fear": 1.0,
            "grief": 1.0,
            "joy": 1.0,
            "hope": 1.0
        },

        "category_weights": {
            "politics": 1.0,
            "general": 1.0,
            "business": 1.0,
            "technology": 1.0,
            "sports": 1.0,
            "entertainment": 1.0
        },
        "decision_parameters": {
            "hybrid_blend_weight": 0.8,
            "freq_boost_factor": 0.1
        }
    }
}

PERSONALITY_SUMMARIES = {
    "melancholic": (
        "Emotionally reflective and attuned to hardship. Strongly influenced by low-valence emotions like grief and fear, "
        "this personality leans toward somber interpretations of world events. Prioritizes political and societal categories, "
        "and weighs emotionally heavy content zones more heavily. Has a heightened sensitivity to grief-related and fear-based triggers, "
        "with a moderate tolerance for joy or optimism. Tends to be emotionally impacted even by subtle signals of sadness or distress."
    ),
    "stoic": (
        "Calm, composed, and minimally reactive. The stoic personality avoids extremes of joy or despair, instead favoring "
        "emotional neutrality. Assigns relatively even importance to all news categories and is resistant to emotional manipulation "
        "via trigger words. This profile is ideal for emotionally stable mood readings with low sensitivity to fleeting or volatile events."
    ),
    "exuberant": (
        "Highly responsive to excitement, joy, and hope. This personality thrives on high-valence, high-energy stimuli and "
        "assigns more influence to entertainment, sports, and tech categories. Strongly rewards emotions like joy, excitement, and gratitude, "
        "while discounting more somber or fearful emotions. Reacts quickly to uplifting or energetic emotional cues, making moods feel lively and expressive."
    ),
    "curious": (
        "Intellectually driven and emotionally open. Prioritizes novelty, insight, and complexity over raw sentiment. Highly weighted "
        "toward technology and general knowledge topics. Emotions such as curiosity, realization, and surprise are emphasized, with balanced sensitivity "
        "across both hopeful and troubling emotional triggers. Blends analytical focus with emotional nuance to form reflective moods."
    ),
    "balanced": (
        "The neutral observer. All emotional zones, content categories, and emotional triggers are treated with equal importance. "
        "No single type of stimulus dominates. This personality offers a baseline perspective with no strong biases, providing the most stable, "
        "even-handed mood formation possible."
    )
}

ALL_PROFILES = list(PERSONALITY_SUMMARIES.keys())

TRIGGER_WORD_GROUPS = {
    "fear": [
        "terror", "kill", "crisis", "war", "attack", "shooting", "disaster", "bomb",
        "explosion", "assault", "hostage", "threat", "invasion", "massacre", "hijack"
    ],
    "grief": [
        "mourning", "tragedy", "loss", "death", "suicide", "collapse", "eviction",
        "displaced", "funeral", "grief", "suffering", "casualty"
    ],
    "joy": [
        "celebration", "victory", "miracle", "wedding", "birth", "breakthrough", "discovery",
        "rescue", "champion", "cheers", "award", "happy", "surprise"
    ],
    "hope": [
        "gratitude", "peace", "comfort", "recovery", "reunion", "unity", "healing",
        "solidarity", "compassion", "care", "generosity", "rebuild", "optimism"
    ]
}

# EMOTION_ZONE_WEIGHTS = {
#     "high_pleasure_high_energy": 1.2,
#     "low_pleasure_high_energy": 1.3,
#     "low_pleasure_low_energy": 1.2,
#     "high_pleasure_low_energy": 1.0,
#     "neutral_or_balanced": 0.8,
#     "flat_neutral": 0.5
# }

CATEGORY_QUERIES = {
    "technology": "technology OR AI OR robotics",
    "sports": "sports OR football OR tennis",
    "entertainment": "movies OR celebrities OR music",
    "business": "stocks OR finance OR economy",
    "politics": "election OR government OR law",
    "general": "news OR world events"
}
