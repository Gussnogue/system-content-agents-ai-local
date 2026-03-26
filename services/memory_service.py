import chromadb
import uuid
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class MemoryService:
    def __init__(self):
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)

        # URLs do LM Studio
        self.embed_url = os.getenv("LM_STUDIO_EMBEDDING_URL", "http://localhost:1234/v1/embeddings")
        self.model_name = os.getenv("LLM_MODEL_NAME", "nomic-embed-text-v1.5")  # ou o nome exato no LM Studio

        # Cria coleções por agente
        self.collections = {}
        for agent_type in ['blogger', 'social', 'designer']:
            self.collections[agent_type] = self.client.get_or_create_collection(name=agent_type)

    def _get_embedding(self, text):
        """Obtém embedding do LM Studio."""
        payload = {
            "input": text,
            "model": self.model_name
        }
        try:
            response = requests.post(self.embed_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            # O retorno esperado: {"data":[{"embedding":[...]}]}
            return data["data"][0]["embedding"]
        except Exception as e:
            print(f"Erro ao obter embedding: {e}")
            # Retorna um embedding vazio para não quebrar o fluxo
            return [0.0] * 768  # dimensão padrão do Nomic

    def add_memory(self, agent_type, text, metadata=None):
        collection = self.collections[agent_type]
        embedding = self._get_embedding(text)
        doc_id = str(uuid.uuid4())
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            documents=[text]
        )
        return doc_id

    def search(self, agent_type, query, top_k=5):
        collection = self.collections[agent_type]
        query_embedding = self._get_embedding(query)
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results['documents'][0] if results['documents'] else []

    def delete_memory(self, agent_type, doc_id):
        collection = self.collections[agent_type]
        collection.delete(ids=[doc_id])