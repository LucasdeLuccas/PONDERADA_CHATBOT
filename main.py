import os
import tkinter as tk
from model import LocalLLM
from gui import ChatGUI

def handle_user_query(user_query):
    answer = llm.generate_answer(user_query)
    return answer

if __name__ == "__main__":
    llm = LocalLLM(model_name='gpt-3.5-turbo')  
    root = tk.Tk()
    app = ChatGUI(root, handle_user_query)
    root.mainloop()
