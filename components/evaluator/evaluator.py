import re
import nltk
#nltk.download('cmudict')
from nltk.corpus import cmudict

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



    def syllable_count(word):
        word = word.lower()
        if word in self.cmu_dict:
            # Take the first pronunciation
            pronunciation = self.cmu_dict[word][0]
            syllables = len([ph for ph in pronunciation if ph[-1].isdigit()])
            return syllables
        else:
            return self.estimate_syllables(word)


    def preprocess(sentence):
        # Remove punctuation and special characters
        return re.sub('[^A-Za-z0-9 ]+', '', sentence)

    def line_counter(sentence):
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

    def syll_sentence(sentence):
        syll_line = []
        for line in sentence.split("\n"):
            syll_line.append((self.line_counter(line), line))
        return syll_line

    def extract_flexible_haikus(syll_lines):
        haikus = []

        for i in range(1, len(syll_lines) - 1):
            prev_syll, prev_line = syll_lines[i - 1]
            curr_syll, curr_line = syll_lines[i]
            next_syll, next_line = syll_lines[i + 1]

            if 4 <= prev_syll <= 6 and 6 <= curr_syll <= 8 and 4 <= next_syll <= 6:
                haikus.append((f"{prev_line}\n{curr_line}\n{next_line}", [prev_syll, curr_syll, next_syll]))
                break
        return haikus if haikus else [("no/improper haiku", [0,0,0])]

    def score_haiku(haiku):
        score = sum([x-y for x,y in zip([5,7,5], haiku[1])])
        return score

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig

import torch

class haikuEvaluation:
    def __init__(self):
        #bringing in a quantized model to save on memory
        self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
        self.quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        self.quantized_model = AutoModelForCausalLM.from_pretrained(self.model_id, device_map="auto", torch_dtype=torch.bfloat16, quantization_config=quantization_config)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
    
    def model_evaluation(haikus, quantized_model, tokenizer):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional haiku competition judge. "
                    "Your job is to evaluate three haikus based on their poetic quality, emotional impact, imagery, and adherence to the traditional haiku structure. "
                    "After evaluating, choose the best haiku and explain your reasoning in 2-3 sentences."
                )
            },
            {
                "role": "user",
                "content": (
                    "Here are three haikus:\n\n"
                    f"1. {haikus[0]}"
                    f"2. {haikus[1]}"
                    f"3. {haikus[2]}"
                    "Please select the best one and explain why."
                )
            }
        ]

    

        input_ids = tokenizer.encode(messages[1]['content'], return_tensors="pt").to("cuda")

        outputs = quantized_model.generate(input_ids, max_new_tokens=256)

        return tokenizer.decode(outputs[0], skip_special_tokens=True)