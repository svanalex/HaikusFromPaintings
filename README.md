# HaikusFromPaintings

<p align="center">
  <img src="static/haiku_logo.png" alt="HAIKU Logo" width="500"/>
</p>

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-web--app-green.svg)
![LLM](https://img.shields.io/badge/LLM-Groq%20%2F%20LLaMA-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Description
HAIKU is a multimodal, AI-driven poetry system that generates emotionally resonant haikus inspired by visual art and the current emotional climate of the world. It combines news-based mood detection, image understanding, and creative language generation to simulate computational creativity.

## Features
- **News-Based Emotion Modeling**: Analyzes recent news articles to determine a dominant emotional state using an LLM-based classifier and a psychologically-informed emotion model (VAD).
- **Image-Driven Inspiration**: Extracts salient features (colors, descriptive image caption) from uploaded images using vision-language models.
- **Dynamic Prompt Engineering**: Dynamically generates poetic prompts using five distinct strategies tailored to the image and emotional context.
- **LLM-Generated Poetry**: Crafts multiple haikus using LLMs and selects the best one based on structural and aesthetic evaluation.
- **Narrative Explanations**: Provides readable emotional narratives showing how the mood was shaped and why a haiku was selected.
- **Web Interface**: A clean, intuitive GUI where users can run the system on example images or upload their own.


## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/svanalex/HaikusFromPaintings.git
cd HaikusFromPaintings
```
2. **Create a virtual environment**
```bash
python -m venv venv
```
3. **Activate the environemnt**
On macOS/Linux:
```bash
source venv/bin/activate        
```
On Windows:
```bash
venv\Scripts\activate 
```
4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```
5. **Set up your API keys**

This project requires access to a news API (e.g., NewsAPI.org) and an LLM backend (e.g., Groq). To claim your API keys, please follow the instructions on the respective sources:

- News API Key: [https://newsapi.org/](https://newsapi.org/) (under *"Get API Key"*)
- Groq API Key: [https://groq.com/#](https://groq.com/#) (under *"Developers" → "Free API Key"*)

6. **Set up the .env file**

In the root directory of the project, create a file named `.env`:
```bash
# You can do this manually or using the terminal
touch .env # for macOS/Linux
```
```bash
New-Item -Path . -Name ".env" -ItemType "File" # for Windows
```
Paste the following as the content of your `.env` file (using your real API keys from Step 5):
```bash
# .env (Do NOT commit this file!)
NEWS_API_KEY=your_news_api_key_here
GROQ_API_KEY=your_groq_api_key_here
LLAMA_MODEL_ID=meta-llama/llama-4-scout-17b-16e-instruct # we used this version of llama but you can try different ones
```

7. **Run the app**
```bash
python app.py
```
Open your browser and go to: http://127.0.0.1:5000

## How to Use
1. Open the app in your browser
2. Click "Run with Example Image" to see how the system works on a predefined image
3. Upload a custom image and click "Run with Uploaded Image" to create a unique haiku for it

## Project Structure

### `components/` – Modular system components
- **`emotion_engine/`** – Handles emotional profiling and mood generation using news articles and personality profiles (GoEmotions, VAD scoring, personality weightings).
- **`evaluator/`** – Evaluates haikus based on structure, emotion alignment, and poetic quality.
- **`haiku_generator/`** – Interfaces with an LLM (e.g., LLaMA via Groq) to generate haikus from prompts.
- **`image_analysis/`** – Runs BLIP captioning and color palette extraction on the image.
- **`prompt_engineering/`** – Creates multiple types of prompts (instructional, contextual, role-based, etc.) for haiku generation.

---

### `core/`
- **`haiku_orchestrator.py`** – Central orchestrator script that runs the full haiku generation pipeline, combining emotion, image, prompt, and haiku logic.

---

### `exploratory_notebooks/`
- Archived and experimental notebooks and scripts for reference and testing purposes.

---

### `static/`
- Publicly served static assets:
  - **`styles.css`** – Custom styling for frontend.
  - **`example.jpg`**, **`uploads/`** – Image assets and user uploads (uploads should be `.gitignored`).

---

### `templates/`
- **`index.html`** – Main frontend HTML template rendered with Jinja2 via Flask. Displays input, haikus, emotion summaries, and image analysis results.

---

### Other Root Files
- **`.gitignore`** – Excludes `.env`, `uploads/`, virtual environments, etc.
- **`app.py`** – Flask app entry point and route logic.
- **`requirements.txt`** – Lists all Python dependencies.

## Notes
The system is modular: You can swap out models or APIs with minimal changes.

Currently optimized for educational and experimental use - not for production deployment.

## Credits
Built in Spring 2025 by Alexander Svancara, Andreas Kramer, and Courtney Bodily for the course Advanced Computational Creativity, taught by Paul Bodily, Ph.D at Idaho State University.

