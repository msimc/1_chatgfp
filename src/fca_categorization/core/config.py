"""
File: config.py
Location: src/fca_categorization/core/config.py
Migrated: 2024-11-03
Original Location: database/database.py
"""

# Location: /mnt/data/database/database.py
# Summary: Configures connection to PostgreSQL and tests the database connection.
# Inputs: Uses .env file for database URL.
# Outputs: Initializes and checks database connection.
# Date: 28-10-2024 19:30 (European Time)
# Changes: Corrected the SQL execution method for testing the connection.

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up the database engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to test database connection
def test_database_connection():
    try:
        with engine.connect() as connection:
            # Corrected the execution method for raw SQL
            connection.execute(text("SELECT 1"))
        print("Database connection successful.")
    except OperationalError as e:
        print(f"Database connection failed: {e}")

# Run connection test
if __name__ == "__main__":
    test_database_connection()

# End of File: /mnt/data/database/database.py
