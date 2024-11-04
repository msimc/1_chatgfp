# Location: database/models.py
# Purpose: Define SQLAlchemy models for the FCA categorization database.
# Inputs: None (defines database schema)
# Outputs: SQLAlchemy ORM models for database interaction
# Date: 28-10-2024 21:00 (European Time)
# Changes: Added metadata for Alembic migration.

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FCASection(Base):
    __tablename__ = 'fca_sections'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String, index=True)
    
    def __repr__(self):
        return f"<FCASection(title={self.title}, category={self.category})>"

# End of File: database/models.py