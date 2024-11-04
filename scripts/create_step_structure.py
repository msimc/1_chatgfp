"""
File: create_step_structure.py
Location: ./scripts/create_step_structure.py
Created: 2024-11-03
Purpose: Set up new step-based project structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class StepBasedStructureCreator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.src_dir = self.root_dir / "src" / "fca_categorization"
        self.backup_dir = self.root_dir / f"backups/pre_step_structure_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_backup(self):
        """Create backup of current state"""
        print(f"Creating backup in {self.backup_dir}")
        if not self.backup_dir.parent.exists():
            self.backup_dir.parent.mkdir(parents=True)
        shutil.copytree(self.src_dir, self.backup_dir, dirs_exist_ok=True)

    def create_directory_structure(self):
        """Create the step-based directory structure"""
        # Define the structure
        structure = {
            "steps": {
                "step_1_data_ingestion": [
                    "document_loader.py",
                    "text_extractor.py",
                    "data_validator.py"
                ],
                "step_2_preprocessing": [
                    "text_cleaner.py",
                    "chunker.py",
                    "metadata_extractor.py"
                ],
                "step_3_embedding": [
                    "embeddings_generator.py",
                    "vector_store.py",
                    "index_manager.py"
                ],
                "step_4_retrieval": [
                    "query_processor.py",
                    "semantic_search.py",
                    "result_ranker.py"
                ],
                "step_5_categorization": [
                    "fca_analyzer.py",
                    "category_mapper.py",
                    "compliance_checker.py"
                ]
            },
            "models": [
                "document.py",
                "embedding.py",
                "categorization.py"
            ],
            "api/v1/endpoints": [
                "ingestion.py",
                "processing.py",
                "embedding.py",
                "retrieval.py",
                "categorization.py"
            ],
            "core": [
                "config.py",
                "security.py"
            ],
            "utils": [
                "helpers.py"
            ]
        }

        print("Creating new directory structure...")
        for dir_path, items in structure.items():
            # Create directory
            full_dir = self.src_dir / dir_path
            full_dir.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py
            (full_dir / "__init__.py").touch()

            # Create files or subdirectories
            if isinstance(items, list):
                for file in items:
                    (full_dir / file).touch()
            else:
                for subdir, files in items.items():
                    subdir_path = full_dir / subdir
                    subdir_path.mkdir(parents=True, exist_ok=True)
                    (subdir_path / "__init__.py").touch()
                    for file in files:
                        (subdir_path / file).touch()

    def run(self):
        """Execute the structure creation"""
        try:
            print("Starting step-based structure creation...")
            self.create_backup()
            self.create_directory_structure()
            print("Structure created successfully!")
            print(f"Backup created at: {self.backup_dir}")
            
            # Print next steps
            print("\nNext steps:")
            print("1. Review the new structure in src/fca_categorization/")
            print("2. Move existing code into appropriate step directories")
            print("3. Update imports in your files")
            print("4. Run your tests to ensure everything works")
            
        except Exception as e:
            print(f"Error during structure creation: {str(e)}")
            print("Rolling back changes...")
            if self.src_dir.exists():
                shutil.rmtree(self.src_dir)
            if self.backup_dir.exists():
                shutil.copytree(self.backup_dir, self.src_dir)
            raise

if __name__ == "__main__":
    creator = StepBasedStructureCreator()
    creator.run()

"""
Save this file as: create_step_structure.py
Location: ./scripts/create_step_structure.py
"""