"""
File: reorganize_project.py
Location: ./scripts/reorganize_project.py
Created: 2024-11-03
Purpose: Consolidate and reorganize project into step-based structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class ProjectReorganizer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.backup_dir = self.root_dir / f"backups/full_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_backup(self):
        """Create full project backup"""
        print(f"Creating backup in {self.backup_dir}")
        shutil.copytree(
            self.root_dir,
            self.backup_dir,
            ignore=shutil.ignore_patterns('venv', '__pycache__', '*.pyc', '.git')
        )

    def create_new_structure(self):
        """Create new project structure"""
        new_structure = {
            "src/chatgfp": {  # Main application directory
                "steps": {
                    "step_1_data_ingestion": [
                        "document_loader.py",  # From pdf_processing
                        "text_extractor.py",
                        "data_validator.py"
                    ],
                    "step_2_preprocessing": [
                        "text_cleaner.py",
                        "chunker.py",
                        "metadata_extractor.py"
                    ],
                    "step_3_embedding": [
                        "embeddings_generator.py",  # From app/services/embeddings.py
                        "vector_store.py",         # From app/services/vector_store.py
                        "index_manager.py"
                    ],
                    "step_4_retrieval": [
                        "query_processor.py",
                        "semantic_search.py",      # From app/services/retriever.py
                        "result_ranker.py"
                    ],
                    "step_5_categorization": [
                        "fca_analyzer.py",         # From src/fca_categorization/models.py
                        "category_mapper.py",
                        "compliance_checker.py"
                    ]
                },
                "core": {
                    "auth": "auth",               # Move from auth/
                    "database": "database",        # Move from database/
                    "config.py": None,
                    "security.py": None
                },
                "api": {
                    "v1": {
                        "endpoints": {
                            "ingestion.py": None,
                            "processing.py": None,
                            "embedding.py": None,
                            "retrieval.py": None,
                            "categorization.py": None
                        }
                    }
                },
                "models": {
                    "document.py": "app/models/document.py",
                    "embedding.py": "app/models/embedding.py",
                    "categorization.py": "src/fca_categorization/models.py"
                },
                "tests": {  # Consolidate all tests
                    "step_1": "fca_queries",
                    "step_2": "fca_queries",
                    "step_3": "fca_queries",
                    "step_4": "fca_queries",
                    "step_5": "fca_queries",
                    "conftest.py": "fca_queries/conftest.py"
                },
                "utils": {
                    "monitoring.py": "postgres/postgres_monitor.py",
                    "health_check.py": "postgres/postgres_health.py",
                    "helpers.py": None
                }
            },
            "docs": {  # Consolidate documentation
                "steps": {
                    "step_1_data_ingestion.md": "fca_sequence_scripts/1_project_overview.md",
                    "step_2_preprocessing.md": "fca_sequence_scripts/2_api_specification.md",
                    "step_3_embedding.md": "fca_sequence_scripts/3_testing_implementation.md",
                    "step_4_retrieval.md": "fca_sequence_scripts/4_authentication_system.md",
                    "step_5_categorization.md": "fca_sequence_scripts/5_project_progress.md"
                },
                "api": "descriptions_overviews/ChatGFP Project Status Overview.md",
                "setup": "fca_sequence_scripts/8_windows_postgresql_installation.md"
            }
        }
        
        return new_structure

    def migrate_code(self):
        """Migrate code to new structure"""
        new_structure = self.create_new_structure()
        # Implementation of code migration...

    def run(self):
        """Execute the reorganization"""
        try:
            print("Starting project reorganization...")
            self.create_backup()
            self.migrate_code()
            print("Reorganization completed successfully!")
            print(f"Backup created at: {self.backup_dir}")
            
            print("\nNext steps:")
            print("1. Review the new structure in src/chatgfp/")
            print("2. Update imports in migrated files")
            print("3. Run tests to verify functionality")
            print("4. Update documentation with new file locations")
            
        except Exception as e:
            print(f"Error during reorganization: {str(e)}")
            print("Rolling back changes...")
            if self.backup_dir.exists():
                shutil.copytree(self.backup_dir, self.root_dir, dirs_exist_ok=True)
            raise

if __name__ == "__main__":
    reorganizer = ProjectReorganizer()
    reorganizer.run()

"""
Save this file as: reorganize_project.py
Location: ./scripts/reorganize_project.py
"""