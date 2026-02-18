import os

from langdetect import detect
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

from utils import HireMeChatbotUtils

class QueryChatbot:
    def __init__(self):
        OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://hire_me_ollama:11434")
        self.embeddings = HireMeChatbotUtils().load_embeddings()
        self.vectordb = Chroma(
            persist_directory="./vector_db",  
            embedding_function=self.embeddings
        )
        self.llm = OllamaLLM(model="mistral:7b-instruct", base_url=OLLAMA_HOST)
    
    def detect_language(self, query):
        language = detect(query)
        return language

    def qa_chain(self):
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(search_kwargs={"k": 10})
        )
        return qa_chain
    
    def get_response(self, query):
        language = self.detect_language(query)
        print(f"✓ Detected language: {language}")
        qa_chain = self.qa_chain()
        response = qa_chain.invoke(query)
        return response

if __name__ == "__main__":
    chatbot = QueryChatbot()
    sample_query = "What programming languages is Nour proficient in?"
    response = chatbot.get_response(sample_query)
    print(f"✓ Response: {response}")

