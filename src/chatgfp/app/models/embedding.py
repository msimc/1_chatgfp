from typing import List, Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

class Embedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="document.id")
    embedding_data: List[float]
    model_name: str
    dimension: int

    @validator('embedding_data')
    def check_dimension(cls, v, values):
        """Validate embedding dimension"""
        if 'dimension' in values and len(v) != values['dimension']:
            raise ValueError(f"Embedding dimension mismatch. Expected {values['dimension']}, got {len(v)}")
        return v

    class Config:
        arbitrary_types_allowed = True
