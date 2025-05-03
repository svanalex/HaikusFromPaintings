from .evaluator import haikuEvaluation
from .evaluator import syllable_counter

def analyze_haiku(haiku):
    haiku_eval = haikuEvaluation(haiku)
    syllable_count = syllable_counter(haiku)
    return {
        "syllable_count": syllable_count,
        "best haiku ": haiku_eval.score_haiku(haiku_eval.extract_flexible_haikus(syllable_count)),
        "best haiku": haiku_eval.model_evaluation(haiku)
    }
