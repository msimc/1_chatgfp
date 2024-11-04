"""
File: setup_project.ps1
Location: ./scripts/setup_project.ps1
Created: 2024-11-03
Purpose: Set up the ChatGFP project environment and dependencies
Changes: Initial version
Dependencies: Requires PowerShell and Python installed
"""

# Create necessary directories
New-Item -ItemType Directory -Force -Path "app"
New-Item -ItemType Directory -Force -Path "app/services"
New-Item -ItemType Directory -Force -Path "app/models"
New-Item -ItemType Directory -Force -Path "alembic"
New-Item -ItemType Directory -Force -Path "scripts"

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install required packages
pip install alembic sqlalchemy psycopg2-binary fastapi uvicorn sqlmodel python-dotenv

# Verify installations
pip list

Write-Host "Project setup complete! Next steps:"
Write-Host "1. Configure .env file with your database settings"
Write-Host "2. Run 'alembic init alembic' to initialize migrations"
Write-Host "3. Run 'alembic revision --autogenerate -m "Initial migration"'"

"""
Save this file as: setup_project.ps1
Location: ./scripts/setup_project.ps1
"""