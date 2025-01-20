from pprint import pprint

import pandas as pd
from gpt4all import GPT4All
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Carregar os dados
data = pd.read_csv(r"C:\Users\felip\Desktop\workspace\djangoAgentes\media\mba_decision_dataset.csv")

# Exemplo: Predizer salário pós-MBA baseado em anos de experiência e pontuação GMAT
X = data[['Years of Work Experience', 'GRE/GMAT Score']]
y = data['Expected Post-MBA Salary']

# Modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Obter coeficientes
coefs = model.coef_

# Usar LLM para explicar os coeficientes
prompt = f"""
Os coeficientes do modelo de regressão são:
- Anos de experiência de trabalho: {coefs[0]}
- Pontuação GRE/GMAT: {coefs[1]}

Explique como esses fatores influenciam o salário esperado pós-MBA em uma linguagem simples.
"""

path = r"C:\Users\felip\AppData\Local\nomic.ai\GPT4All\Llama-3.2-1B-Instruct-Q4_0.gguf"
model = GPT4All(model_name=path, model_path=path)

# Enviar para o LLM
response = model.generate(prompt)

pprint(response)
