# Improved env.py file for Alembic
# Location: ./alembic/env.py
# Updated: 2024-11-04
# Purpose: Enhanced Alembic environment configuration for handling database migrations with improved import paths and error handling.

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os
from dotenv import load_dotenv
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Ensure the project root is in the Python path for proper module discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# This is the Alembic Config object
config = context.config

# Override sqlalchemy.url with environment variable
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all models here for 'autogenerate' support
try:
    from src.fca_categorization.models import Document, Embedding  # Adjust the import path to match your project structure
    logger.info("Models imported successfully.")
except ImportError as e:
    logger.error("Failed to import models. Ensure the path is correct. Details: %s", e)
    raise ImportError(f"Failed to import models. Details: {e}")

# Set the target metadata for migrations
# Ensure target_metadata reflects the base metadata from all models in the project
try:
    target_metadata = Document.metadata
    logger.info("Target metadata set successfully.")
except AttributeError as e:
    logger.error("Failed to access metadata. Ensure models are properly defined. Details: %s", e)
    raise AttributeError(f"Failed to access metadata. Details: {e}")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    logger.info("Running migrations in offline mode.")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    logger.info("Running migrations in online mode.")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

"""
Save this file as: env.py
Location: ./alembic/env.py
"""
