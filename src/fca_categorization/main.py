"""
File: main.py
Location: src/fca_categorization/main.py
Created: 2024-11-03
Purpose: Main application entry point with step-based processing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .steps.step_1_data_ingestion import document_loader
from .steps.step_2_preprocessing import text_cleaner
from .steps.step_3_embedding import embeddings_generator
from .steps.step_4_retrieval import semantic_search
from .steps.step_5_categorization import fca_analyzer

app = FastAPI(title="ChatGFP", description="FCA Categorization with RAG capabilities")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from each step
from .api.v1.endpoints import (
    ingestion,
    processing,
    embedding,
    retrieval,
    categorization
)

app.include_router(ingestion.router, prefix="/api/v1/ingestion", tags=["ingestion"])
app.include_router(processing.router, prefix="/api/v1/processing", tags=["processing"])
app.include_router(embedding.router, prefix="/api/v1/embedding", tags=["embedding"])
app.include_router(retrieval.router, prefix="/api/v1/retrieval", tags=["retrieval"])
app.include_router(categorization.router, prefix="/api/v1/categorization", tags=["categorization"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
