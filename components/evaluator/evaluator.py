import re
import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict
import os
from dotenv import load_dotenv
import requests
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

class syllable_counter:
    def __init__(self):
        self.cmu_dict = cmudict.dict()

    def estimate_syllables(self, word):
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word and word[0] in vowels:
            count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count


    def syllable_count(self, word):
        word = word.lower()
        if word in self.cmu_dict:
            # Take the first pronunciation
            pronunciation = self.cmu_dict[word][0]
            syllables = len([ph for ph in pronunciation if ph[-1].isdigit()])
            return syllables
        else:
            return self.estimate_syllables(word)


    def preprocess(self, sentence):
        # Remove punctuation and special characters
        return re.sub('[^A-Za-z0-9 ]+', '', sentence)

    def line_counter(self, sentence):
        #need to make words from sentences
        sentence = self.preprocess(sentence)
        #print(sentence)
        sentence_syllables = 0
        words = sentence.split()
        for word in words:
            #print(word, syllable_count(word))
            sentence_syllables += self.syllable_count(word)
            #sentence_syllables += count_syllables(word)
        return sentence_syllables

    def syll_sentence(self, sentence):
        syll_line = []
        for line in sentence.split("\n"):
            syll_line.append((self.line_counter(line), line))
        return syll_line

    def extract_flexible_haikus(self, syll_lines):
        haikus = []

        for i in range(1, len(syll_lines) - 1):
            prev_syll, prev_line = syll_lines[i - 1]
            curr_syll, curr_line = syll_lines[i]
            next_syll, next_line = syll_lines[i + 1]

            if 4 <= prev_syll <= 6 and 6 <= curr_syll <= 8 and 4 <= next_syll <= 6:
                haikus.append((f"{prev_line}\n{curr_line}\n{next_line}", [prev_syll, curr_syll, next_syll]))
                break
        return haikus if haikus else [("no/improper haiku", [0,0,0])]

    def score_haiku(self, haiku):
        score = sum([x-y for x,y in zip([5,7,5], haiku)])
        return score, haiku
    

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL_ID = os.getenv("LLAMA_MODEL_ID", "llama-3.1-8b-instant")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_haiku(prompt, system_instruction=None, haikus=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    if isinstance(prompt, list):
        prompt = "\n\n".join(prompt)

    messages = []
    if system_instruction:
        messages.append({"role": "system",
                "content": (
                    "You are a professional haiku competition judge. "
                    "Your job is to evaluate three haikus based on their poetic quality, emotional impact, imagery, and adherence to the traditional haiku structure. "
                    "After evaluating, choose the best haiku and explain your reasoning in 2-3 sentences."
                )})
    messages.append({"role": "user",
                "content": (
                    "Here are three haikus:\n\n"
                    f"1. {haikus[0]}"
                    f"2. {haikus[1]}"
                    f"3. {haikus[2]}"
                    "Please select the best one and explain why."
                )})

    payload = {
        "model": LLAMA_MODEL_ID,
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 100
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Error generating haiku:", response.text)
        return "Haiku generation failed."

class haikuEvaluation:

    
    def model_evaluation(self, haikus):

            
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        #if isinstance(prompt, list):
        #    prompt = "\n\n".join(prompt)

        messages = []
        
        messages.append({"role": "system",
                    "content": (
                        "You are a professional haiku competition judge. "
                        "Your job is to evaluate three haikus based on their poetic quality, emotional impact, imagery, and adherence to the traditional haiku structure. "
                        "After evaluating, choose the best haiku and explain your reasoning in 2-3 sentences."
                    )})
        messages.append({"role": "user",
                    "content": (
                        "Here are three haikus:\n\n"
                        f"1. {haikus[0]}"
                        f"2. {haikus[1]}"
                        f"3. {haikus[2]}"
                        "Please select the best one and explain why."
                    )})

        payload = {
            "model": LLAMA_MODEL_ID,
            "messages": messages,
            "temperature": 0.9,
            "max_tokens": 100
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        try:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print("Error evaluating haikus:", response.text)
            return "Haiku evaluation failed."