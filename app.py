from flask import Flask, render_template, request
import json
import os
from components.emotion_engine.engine import run_emotion_engine
from core.haiku_orchestrator import generate_emotionally_influenced_haiku
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
USE_SINGLE_DAY = False
TOTAL_ARTICLES = 20
MOOD_STRATEGY = "hybrid"
HAIKU_PROMPT_TEMPLATES = ["instructional","contextual","role_based","example_driven","iterative"]
AVAILABLE_PROFILES = ["melancholic", "stoic", "exuberant", "curious", "balanced"]
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    selected_profile = None
    mood_result = None
    haiku_result = None
    uploaded_image = None

    if request.method == "POST":
        selected_profile = request.form.get("profile")
        image_file = request.files.get("image")
        prompt_template = request.form.get("prompt_template")
        action = request.form.get("action")  # Check which button was pressed

        if action == "Generate Mood Only" and selected_profile:
            llm_context, dev_report = run_emotion_engine(
                profile_name=selected_profile,
                api_key=NEWS_API_KEY,
                total_articles=TOTAL_ARTICLES,
                use_single_day=USE_SINGLE_DAY,
                include_dev_log=True,
                mood_strategy=MOOD_STRATEGY
            )
            mood_result = llm_context

        elif action == "Generate Haiku" and selected_profile and image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)


            haiku_data = generate_emotionally_influenced_haiku(
                image_path=image_path,
                profile_name=selected_profile,
                news_api_key=NEWS_API_KEY,
                total_articles=TOTAL_ARTICLES,
                use_single_day=USE_SINGLE_DAY,
                mood_strategy=MOOD_STRATEGY,
                prompt_template=prompt_template,
                include_dev_log=True
            )

            haiku_result = haiku_data
            mood_result = haiku_data["mood"]  # reuse mood display
            uploaded_image = filename

    return render_template(
        "index2.html",
        profiles=AVAILABLE_PROFILES,
        selected=selected_profile,
        mood=mood_result,
        haiku_data=haiku_result,
        uploaded_image=uploaded_image
    )

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)