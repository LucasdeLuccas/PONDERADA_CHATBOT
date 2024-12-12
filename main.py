import streamlit as st
from openai import OpenAI
import nltk
from nltk.corpus import stopwords
import re
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

class FutebolCuriosidadesChatbot:
    def __init__(self):
        load_dotenv()

        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        try:
            with open("rules_of_soccer.txt", "r", encoding="utf-8") as file:
                self.document = file.read()
        except FileNotFoundError:
            self.document = "Regras não encontradas. Certifique-se de que o arquivo rules_of_soccer.txt está presente."

        nltk.download("stopwords", quiet=True)

        self.vector_store = self._load_document()
        self.conversation_context = ""

    def _load_document(self):
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(self.document)

        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(chunks, embeddings)
        return vector_store

    def extract_keywords(self, query):
        stop_words = set(stopwords.words("portuguese"))
        words = re.findall(r"\w+", query.lower())
        keywords = [word for word in words if word not in stop_words]
        return " ".join(keywords)

    def generate_response(self, query):
        self.conversation_context += f"Usuário: {query}\n"

        keywords = self.extract_keywords(query)

        if not any(kw in keywords for kw in ["futebol", "gol", "time", "jogador", "campeonato", "partida", "impedimento", "escanteio", "libertadores", "champions", "copa do mundo"]):
            return "Desculpe, só respondo perguntas de futebol."

        results = self.vector_store.similarity_search(query, k=2)
        context = "\n".join([result.page_content for result in results])

       
        combined_context = f"Histórico da conversa:\n{self.conversation_context}\n\n{context}"

        prompt = f"Com base no seguinte contexto:\n\n{combined_context}\n\nResponda à pergunta atual: {query}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em curiosidades sobre futebol. Certifique-se de responder com precisão ao contexto e lembrar do histórico da conversa."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.7,
            )

            answer = response.choices[0].message.content.strip()
            self.conversation_context += f"Assistente: {answer}\n"
            return answer
        except Exception as e:
            return f"Erro: {str(e)}"

def main():
    st.title("Chatbot de Curiosidades sobre Futebol")
    chatbot = FutebolCuriosidadesChatbot()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
  
    if prompt := st.chat_input("Qual é a sua dúvida sobre futebol?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = chatbot.generate_response(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()