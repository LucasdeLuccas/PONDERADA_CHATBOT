import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class ChatGUI:
    def __init__(self, master, model_handler):
        self.master = master
        self.model_handler = model_handler
        self.master.title("Chatbot de Futebol")

        self.text_area = ScrolledText(self.master, wrap='word', width=80, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.master, width=80)
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.master, text="Enviar", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.display_message("Chatbot: Olá! Pergunte-me sobre as regras do futebol, ou campeões da Champions League e da Libertadores.\n")

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if user_message:
            self.display_message(f"Você: {user_message}\n")
            self.entry.delete(0, 'end')
            resposta = self.model_handler(user_message)
            self.display_message(f"Chatbot: {resposta}\n")

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.see('end')
        self.text_area.config(state='disabled')
