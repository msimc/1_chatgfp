from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

    async def get_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embedding = self.model.encode([text], convert_to_tensor=False)[0]
        return embedding.tolist()
