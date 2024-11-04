# Name: database.py
# Location: src/fca_categorization
# Purpose: Set up the SQLAlchemy engine and session for database interactions
# Inputs: None directly
# Outputs: SQLAlchemy engine and session configuration
# Date: 28-10-2024 23:55 (European Time)
# Changes: Added SessionLocal and engine definitions.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Name: database.py
# Location: src/fca_categorization
# Purpose: Set up the SQLAlchemy engine and session for database interactions
# Inputs: None directly
# Outputs: SQLAlchemy engine and session configuration
# Date: 28-10-2024 23:55 (European Time)
# Changes: Added SessionLocal and engine definitions.
