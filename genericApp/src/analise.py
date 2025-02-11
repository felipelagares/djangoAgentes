import sys
from transformers import pipeline
from huggingface_hub import login

sys.path.append(r"C:\Users\go2445ps\Documents\GitHub\djangoAgentes\.env")

import settings

hf_token = settings.HF_TOKEN

login(hf_token)

generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")

import json

def is_valid_json(s: str) -> bool:
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False


def analise_description(json_string):

    prompt =  "Você é um analisador de filmes. "
    "Receberá nomes e descrições de filmes em JSON e identificará temas em comum.\n"
    f"{json_string}\n"
    "Com base na descrição, o que esses filmes têm em comum?"
    # max_input = 1000
    # prompt = prompt[:max_input]
    res = generator(prompt, max_new_tokens=50)
    print(res[0]['generated_text'])
    return res[0]["generated_text"]
