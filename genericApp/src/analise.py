from transformers import pipeline
from openai import OpenAI

import json

client = OpenAI()


def is_valid_json(s: str) -> bool:
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False


def analise_description(json_string):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # modelo mais barato da openai por api
        messages=[
            {"role": "system", "content": "voce é um analisador de filmes"},  # instruções iniciais do sistema
            {
                "role": "user",
                "content": f"o que os filmes a seguir tem em comum: {json_string}"  # meu prompt
            }
        ]
    )

    res = completion.choices[0].message['content']

    return res
