import os
import openai
from dotenv import load_dotenv

class LocalLLM:
    def __init__(self, rules_file='resources/rules_of_soccer.txt', model_name='gpt-3.5-turbo'):
        load_dotenv()

        self.rules_file = rules_file
        self.model_name = model_name
        self.content = self._load_content()

        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("A chave OPENAI_API_KEY não está definida. Defina no .env ou como variável de ambiente.")

    def _load_content(self):
        with open(self.rules_file, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_answer(self, user_query):
        prompt = f"""Você é um assistente que responde somente sobre futebol, com foco em regras e campeonatos como a Champions League e a Libertadores.
Use o seguinte contexto para responder de forma sucinta e clara:
{self.content}

Pergunta do usuário: {user_query}
Se a pergunta não tiver relação com futebol, responda: 'Desculpe, só respondo perguntas sobre futebol.'
Resposta:
"""

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "Você é um especialista em futebol. Responda apenas perguntas sobre futebol. Se a pergunta não for sobre futebol, responda: 'Desculpe, só respondo perguntas sobre futebol.'"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3,
        )

        answer = response.choices[0].message['content'].strip()
        return answer
