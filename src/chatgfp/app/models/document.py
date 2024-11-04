from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"Document(id={self.id}, title='{self.title}')"
