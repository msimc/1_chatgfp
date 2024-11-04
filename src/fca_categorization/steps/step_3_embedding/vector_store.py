"""
File: vector_store.py
Location: src/fca_categorization/steps/step_3_embedding/vector_store.py
Migrated: 2024-11-03
Original Location: app/services/vector_store.py
"""

from typing import List, Optional, Dict, Any
import numpy as np
import faiss
from src.fca_categorization.models.document import Document
from src.fca_categorization.services.embeddings import EmbeddingService

class VectorStore:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.index: Optional[faiss.Index] = None
        self.documents: List[Document] = []
        self.dimension: Optional[int] = None

    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store"""
        if not documents:
            return

        # Get embeddings for all documents
        texts = [doc.content for doc in documents]
        embeddings = await self.embedding_service.get_embeddings(texts)
        
        # Initialize FAISS index if needed
        if self.index is None:
            self.dimension = len(embeddings[0])
            self.index = faiss.IndexFlatL2(self.dimension)

        # Add to FAISS index
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        self.documents.extend(documents)

    async def search(
        self, 
        query: str, 
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if not self.index or not self.documents:
            return []

        # Get query embedding
        query_embedding = await self.embedding_service.get_single_embedding(query)
        query_array = np.array([query_embedding]).astype('float32')

        # Search in FAISS
        distances, indices = self.index.search(query_array, k)
        
        # Format results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):  # Ensure valid index
                doc = self.documents[idx]
                results.append({
                    "document": doc,
                    "score": float(1 / (1 + dist))  # Convert distance to similarity score
                })
        
        return results
