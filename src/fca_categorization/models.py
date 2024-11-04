# Name: models.py
# Location: src/fca_categorization
# Purpose: Define the database models for FCA categorization sections
# Inputs: None directly, used by other scripts for database interactions
# Outputs: Database model definitions
# Date: 28-10-2024 23:55 (European Time)
# Changes: Corrected imports, added appropriate table definition.

from sqlalchemy import Column, Integer, String
from .database import Base

class FCASection(Base):
    __tablename__ = 'fca_sections'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String)

# Name: models.py
# Location: src/fca_categorization
# Purpose: Define the database models for FCA categorization sections
# Inputs: None directly, used by other scripts for database interactions
# Outputs: Database model definitions
# Date: 28-10-2024 23:55 (European Time)
# Changes: Corrected imports, added appropriate table definition.
