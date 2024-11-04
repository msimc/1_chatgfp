# Location: database/alembic/env.py
# Purpose: To set up Alembic to recognize SQLAlchemy models and manage database migrations.
# Inputs: Alembic configuration and model metadata.
# Outputs: Migration scripts for the database.
# Date: 28-10-2024 21:00 (European Time)
# Changes: Updated import paths and corrected configurations for metadata import.

import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Import the Base metadata from models.py (Absolute import to ensure it works)
from database.models import Base

# this is the Alembic Config object, which provides access to the .ini file values,
# for example, to use in a logging configuration.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate'
target_metadata = Base.metadata

# Set the SQLAlchemy connection string from environment variables
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Functions to run migrations in offline or online mode
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# End of File: database/alembic/env.py
