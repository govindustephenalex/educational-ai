import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
import os

class VectorStoreService:
    def __init__(self):
        self.persist_directory = settings.VECTOR_DB_PATH
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
        
        # We need an embedding function. 
        # If no key, we can't really do embeddings easily with OpenAI. 
        # For this demo, assuming OpenAI key is present for embeddings too.
        if settings.OPENAI_API_KEY:
            self.embedding_function = OpenAIEmbeddings()
            self.vectordb = Chroma(
                persist_directory=self.persist_directory, 
                embedding_function=self.embedding_function
            )
        else:
            self.vectordb = None

    def add_texts(self, texts: list[str], metadatas: list[dict]):
        if self.vectordb:
            self.vectordb.add_texts(texts=texts, metadatas=metadatas)
            self.vectordb.persist()

    def similarity_search(self, query: str, k: int = 3):
        if self.vectordb:
            return self.vectordb.similarity_search(query, k=k)
        return []

vector_store_service = VectorStoreService()
