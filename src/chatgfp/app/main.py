# app/main.py

from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.retriever import Retriever
from app.models.document import Document
from pydantic import BaseModel

app = FastAPI(title="ChatGFP RAG API")

# Initialize services
embedding_service = EmbeddingService()
vector_store = VectorStore(embedding_service)
retriever = Retriever(vector_store)

# Pydantic models for API
class DocumentCreate(BaseModel):
    title: str
    content: str
    source: Optional[str] = None
    metadata: dict = {}

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5
    threshold: Optional[float] = 0.0

@app.post("/documents/", response_model=Document)
async def create_document(document: DocumentCreate):
    """Add a new document to the system"""
    doc = Document(**document.dict())
    # Here we would typically also save to database
    await retriever.add_documents([doc])
    return doc

@app.post("/search/")
async def search_documents(query: SearchQuery):
    """Search through documents"""
    results = await retriever.retrieve(
        query.query,
        k=query.limit,
        score_threshold=query.threshold
    )
    return results

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}