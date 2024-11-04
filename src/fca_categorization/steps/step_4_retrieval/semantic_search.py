"""
File: semantic_search.py
Location: src/fca_categorization/steps/step_4_retrieval/semantic_search.py
Migrated: 2024-11-03
Original Location: app/services/retriever.py
"""

from typing import List, Dict, Any
from src.fca_categorization.models.document import Document
from src.fca_categorization.services.vector_store import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    async def retrieve(
        self, 
        query: str, 
        k: int = 5,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            score_threshold: Minimum similarity score threshold
        """
        results = await self.vector_store.search(query, k=k)
        
        # Filter by score threshold
        filtered_results = [
            result for result in results 
            if result["score"] > score_threshold
        ]
        
        return filtered_results

    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the retrieval system"""
        await self.vector_store.add_documents(documents)
