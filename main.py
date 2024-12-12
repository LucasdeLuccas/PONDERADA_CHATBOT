import os
import tkinter as tk
from model import LocalLLM
from gui import ChatGUI

def handle_user_query(user_query):
    # Lista de palavras-chave relacionadas a futebol
    keywords = ["futebol", "bola", "árbitro", "jogador", "time", "campeonato", "gol",
                "libertadores", "champions", "cartão", "falta", "pênalti", "penalti",
                "goleiro", "campo", "fifa", "ifab", "técnico", "treinador", "estádio",
                "torcida", "federacao", "liga", "defesa", "ataque", "zagueiro", "meio-campo",
                "atacante", "lateral", "escanteio", "tiro de meta", "árbitros assistentes","liberta",
                "impedimento", "drible", "cabeceio", "passe", "chute", "voleio", "bicicleta", "escalação",
                "tática", "formação", "posse de bola", "marcação", "zonal", "homem a homem", "linha de fundo",
                "trave", "travessão", "lateral", "escanteio", "tiro livre", "marcação cerrada", "var", "árbitro de vídeo",
                "cartão amarelo", "cartão vermelho", "impedimento", "jogo limpo", "fair play", "fairplay", "juiz de linha", "árbitro assistente de vídeo",
                "arbitragens controversas", "penalidades", "acréscimos", "Messi", "Ronaldo", "Pelé", "Maradona", "Neymar", "Mbappé", "Bola de Ouro",
                "FIFA The Best", "Chuteira de Ouro", "Messi", "Ronaldo", "Pelé", "Maradona", "Neymar", "Mbappé", "Bola de Ouro", "FIFA The Best",
                "Chuteira de Ouro"]

    normalized = user_query.lower()
    # Verifica se a pergunta do usuário contém alguma palavra-chave de futebol
    if not any(kw in normalized for kw in keywords):
        return "Desculpe, só respondo perguntas sobre futebol."

    # Se a pergunta está relacionada a futebol, chama o modelo
    answer = llm.generate_answer(user_query)
    return answer

if __name__ == "__main__":
    llm = LocalLLM(model_name='gpt-3.5-turbo')
    root = tk.Tk()
    app = ChatGUI(root, handle_user_query)
    root.mainloop()
