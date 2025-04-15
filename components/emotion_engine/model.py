from transformers import pipeline

# Define the model pipeline once and reuse
emotion_classifier = pipeline(
    task="text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)
