from flask import Flask, render_template, request
from components.emotion_engine.engine import run_emotion_engine
import os
import json

app = Flask(__name__)

# Load your API key from environment variables
API_KEY = os.getenv("NEWS_API_KEY")



# List of available profiles (should match keys in PERSONALITY_PROFILES)
AVAILABLE_PROFILES = [
    "melancholic",
    "stoic",
    "exuberant",
    "curious",
    "balanced"
]

USE_SINGLE_DAY = False # Promote to UI? #For LLM to be chosen?
TOTAL_ARTICLES = 20  # You can adjust this as needed
MOOD_STRATEGY = "hybrid" #default #max_influence


@app.route("/", methods=["GET", "POST"])
def index():
    selected_profile = None
    mood_result = None

    if request.method == "POST":
        selected_profile = request.form.get("profile")
        if selected_profile:
            llm_context, dev_report = run_emotion_engine(profile_name=selected_profile, api_key=API_KEY, total_articles=TOTAL_ARTICLES, use_single_day=USE_SINGLE_DAY, include_dev_log=True, mood_strategy=MOOD_STRATEGY)
            mood_result = llm_context
    
        # Optional full raw developer log
            if dev_report:
                print("\n Full Developer Mood Report:\n")
                print(json.dumps(dev_report, indent=2))

    return render_template("index.html", profiles=AVAILABLE_PROFILES, selected=selected_profile, mood=mood_result)

if __name__ == "__main__":
    app.run(debug=True)
