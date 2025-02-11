from transformers import pipeline

generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")

import json

def is_valid_json(s: str) -> bool:
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False


def analise_description(json):

    prompt = f'''
    Você é um analisador de filmes, receberá os nomes e descrição de filmes
    e retornará o que eles têm em comum com base na descrição.
    {json}
    '''

    res = generator(prompt, max_length=300)
    return res[0]["generated_text"]