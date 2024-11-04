"""
File: migrate_code_to_steps.py
Location: ./scripts/migrate_code_to_steps.py
Created: 2024-11-03
Purpose: Migrate existing code to new step-based structure
Dependencies: None (standard library only)
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

class CodeMigrator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.src_dir = self.root_dir / "src" / "fca_categorization"
        self.backup_dir = self.root_dir / f"backups/pre_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Define code mappings: source_file -> destination in step structure
        self.code_mappings = {
            # Step 1: Data Ingestion
            "app/services/document_loader.py": "steps/step_1_data_ingestion/document_loader.py",
            "pdf_processing/pdf_extractor.py": "steps/step_1_data_ingestion/text_extractor.py",
            
            # Step 2: Preprocessing
            "app/services/text_processor.py": "steps/step_2_preprocessing/text_cleaner.py",
            
            # Step 3: Embedding
            "app/services/embeddings.py": "steps/step_3_embedding/embeddings_generator.py",
            "app/services/vector_store.py": "steps/step_3_embedding/vector_store.py",
            
            # Step 4: Retrieval
            "app/services/retriever.py": "steps/step_4_retrieval/semantic_search.py",
            
            # Step 5: Categorization
            "src/fca_categorization/models.py": "steps/step_5_categorization/fca_analyzer.py",
            
            # Models
            "app/models/document.py": "models/document.py",
            "app/models/embedding.py": "models/embedding.py",
            
            # API
            "src/fca_categorization/main.py": "api/v1/endpoints/categorization.py",
            
            # Core
            "auth/auth.py": "core/security.py",
            "database/database.py": "core/config.py"
        }

    def backup_current_state(self):
        """Create backup of current state"""
        print(f"Creating backup in {self.backup_dir}")
        if not self.backup_dir.parent.exists():
            self.backup_dir.parent.mkdir(parents=True)
        
        # Backup existing code
        for source in self.code_mappings.keys():
            source_path = self.root_dir / source
            if source_path.exists():
                backup_path = self.backup_dir / source
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, backup_path)

    def update_imports(self, content: str, file_path: str) -> str:
        """Update import statements in file content"""
        # Map old imports to new structure
        import_mappings = {
            "from app.": "from src.fca_categorization.",
            "from pdf_processing.": "from src.fca_categorization.steps.step_1_data_ingestion.",
            "from auth.": "from src.fca_categorization.core.",
            "from database.": "from src.fca_categorization.core."
        }
        
        for old, new in import_mappings.items():
            content = content.replace(old, new)
            
        return content

    def migrate_file(self, source: str, destination: str):
        """Migrate a single file to new location"""
        source_path = self.root_dir / source
        dest_path = self.src_dir / destination
        
        if source_path.exists():
            print(f"Migrating {source} to {destination}")
            
            # Read and update content
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update imports
            updated_content = self.update_imports(content, dest_path)
            
            # Add step documentation
            step_doc = f'''"""
File: {dest_path.name}
Location: src/fca_categorization/{destination}
Migrated: {datetime.now().strftime('%Y-%m-%d')}
Original Location: {source}
"""

'''
            updated_content = step_doc + updated_content
            
            # Write to new location
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

    def migrate_code(self):
        """Execute the code migration"""
        try:
            print("Starting code migration...")
            self.backup_current_state()
            
            # Migrate each file
            for source, destination in self.code_mappings.items():
                self.migrate_file(source, destination)
            
            print("Migration completed successfully!")
            print(f"Backup created at: {self.backup_dir}")
            
            # Create new main.py
            self.create_main_file()
            
            print("\nNext steps:")
            print("1. Review migrated code in src/fca_categorization/")
            print("2. Run tests to verify functionality")
            print("3. Update any remaining imports or references")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            print("Rolling back changes...")
            if self.backup_dir.exists():
                shutil.copytree(self.backup_dir, self.src_dir, dirs_exist_ok=True)
            raise

    def create_main_file(self):
        """Create new main.py with step-based structure"""
        main_content = '''"""
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
'''
        
        with open(self.src_dir / "main.py", 'w', encoding='utf-8') as f:
            f.write(main_content)

if __name__ == "__main__":
    migrator = CodeMigrator()
    migrator.migrate_code()

"""
Save this file as: migrate_code_to_steps.py
Location: ./scripts/migrate_code_to_steps.py
Usage: python scripts/migrate_code_to_steps.py
"""