import os
import random
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from core.haiku_orchestrator import generate_emotionally_influenced_haiku
from components.emotion_engine.config import PERSONALITY_SUMMARIES, ALL_PROFILES

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuration
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Environment Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EXAMPLE_IMAGE_PATH = os.path.join("static", "example.jpg")

def is_allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    haiku_data = None
    uploaded_image = None
    used_example = False
    uploaded_image_path=None
    image_path=None
    selected_profile=None

    if request.method == "POST":
        selected_profile = random.choice(ALL_PROFILES)
        action = request.form.get("action")

        if action == "Run Example":
            image_path = EXAMPLE_IMAGE_PATH
            used_example = True

        elif action == "Run Custom":
            image_file = request.files.get("image")
            if not image_file:
                return render_template("index.html", error="Please upload an image.")
            filename = secure_filename(image_file.filename)

            if not is_allowed_file(filename):
                return render_template("index.html", error="Only .jpg, .jpeg, or .png files are allowed.")
            
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(save_path)

            image_path = save_path
            uploaded_image_path = url_for('static', filename=f"uploads/{filename}")
            uploaded_image = filename
        else:
            return render_template("index.html", error="Invalid action.")

        # Run full haiku generation pipeline
        haiku_data = generate_emotionally_influenced_haiku(
            image_path=image_path,
            profile_name=selected_profile,
            news_api_key=NEWS_API_KEY,
            total_articles=15,
            use_single_day=True,
            mood_strategy="hybrid",
            prompt_template=None,
            include_dev_log=True,   
        )
    if selected_profile is None:
        selected_profile = random.choice(ALL_PROFILES)

    if haiku_data:
        colors = list(dict.fromkeys(haiku_data.get("image_features").get("color_names", [])))[:5]
        print(colors)

    

    return render_template(
        "index.html",
        haiku_data=haiku_data,
        uploaded_image=uploaded_image,
        uploaded_image_path=uploaded_image_path,
        used_example=used_example,
        personality_profile = selected_profile,
        personality_summary=PERSONALITY_SUMMARIES[selected_profile],
        source="example" if used_example else "custom"
    )

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, use_reloader=False)