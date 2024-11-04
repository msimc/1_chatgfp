"""
File: create_project_structure.py
Location: ./scripts/create_project_structure.py
Created: 2024-11-03
Purpose: Create the complete step-based project structure
"""

import os
from pathlib import Path
import shutil
from datetime import datetime

class ProjectStructureCreator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.backup_dir = self.root_dir / f"backups/pre_restructure_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.src_dir = self.root_dir / "src" / "chatgfp"

    def backup_existing(self):
        """Create backup of existing project"""
        print(f"Creating backup in {self.backup_dir}")
        if not self.backup_dir.parent.exists():
            self.backup_dir.parent.mkdir(parents=True)
        shutil.copytree(self.root_dir, self.backup_dir, 
                       ignore=shutil.ignore_patterns('venv', '__pycache__', '*.pyc', '.git'))

    def create_directory_structure(self):
        """Create the complete directory structure"""
        # Define the structure with files
        structure = {
            "steps": {
                "step_1_data_ingestion": [
                    "__init__.py",
                    "document_loader.py",
                    "text_extractor.py",
                    "data_validator.py"
                ],
                "step_2_preprocessing": [
                    "__init__.py",
                    "text_cleaner.py",
                    "chunker.py",
                    "metadata_extractor.py"
                ],
                "step_3_embedding": [
                    "__init__.py",
                    "embeddings_generator.py",
                    "vector_store.py",
                    "index_manager.py"
                ],
                "step_4_retrieval": [
                    "__init__.py",
                    "query_processor.py",
                    "semantic_search.py",
                    "result_ranker.py"
                ],
                "step_5_categorization": [
                    "__init__.py",
                    "fca_analyzer.py",
                    "category_mapper.py",
                    "compliance_checker.py"
                ]
            },
            "core": {
                "__init__.py": None,
                "auth": {
                    "__init__.py": None,
                },
                "database": {
                    "__init__.py": None,
                },
                "config.py": None,
                "security.py": None
            },
            "api": {
                "__init__.py": None,
                "v1": {
                    "__init__.py": None,
                    "endpoints": {
                        "__init__.py": None,
                        "ingestion.py": None,
                        "processing.py": None,
                        "embedding.py": None,
                        "retrieval.py": None,
                        "categorization.py": None
                    }
                }
            },
            "models": {
                "__init__.py": None,
                "document.py": None,
                "embedding.py": None,
                "categorization.py": None
            },
            "tests": {
                "__init__.py": None,
                "conftest.py": None,
                "step_1": {"__init__.py": None},
                "step_2": {"__init__.py": None},
                "step_3": {"__init__.py": None},
                "step_4": {"__init__.py": None},
                "step_5": {"__init__.py": None}
            },
            "utils": {
                "__init__.py": None,
                "monitoring.py": None,
                "health_check.py": None,
                "helpers.py": None
            }
        }

        # Create base src directory
        print(f"Creating directory structure in {self.src_dir}")
        self.src_dir.mkdir(parents=True, exist_ok=True)

        def create_structure(current_path: Path, structure_dict: dict):
            for name, content in structure_dict.items():
                path = current_path / name
                if isinstance(content, dict):
                    path.mkdir(exist_ok=True)
                    create_structure(path, content)
                elif isinstance(content, list):
                    path.mkdir(exist_ok=True)
                    for file in content:
                        (path / file).touch()
                else:
                    path.touch()

        create_structure(self.src_dir, structure)

        # Create docs directory
        docs_dir = self.root_dir / "docs"
        docs_structure = {
            "steps": {
                "step_1_data_ingestion.md": None,
                "step_2_preprocessing.md": None,
                "step_3_embedding.md": None,
                "step_4_retrieval.md": None,
                "step_5_categorization.md": None
            },
            "api": {},
            "setup": {},
            "README.md": None
        }
        docs_dir.mkdir(exist_ok=True)
        create_structure(docs_dir, docs_structure)

        # Create scripts directory
        scripts_dir = self.root_dir / "scripts"
        scripts_structure = {
            "migration": {
                "code_migrator.py": None,
                "structure_verifier.py": None
            },
            "deployment": {
                "setup_environment.py": None
            }
        }
        scripts_dir.mkdir(exist_ok=True)
        create_structure(scripts_dir, scripts_structure)

    def create_base_files(self):
        """Create base project files"""
        base_files = {
            ".env.example": "# Environment variables\nDATABASE_URL=\nSECRET_KEY=\nDEBUG=True\n",
            "pyproject.toml": "[tool.poetry]\nname = \"chatgfp\"\nversion = \"0.1.0\"\n",
            "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npython-dotenv\n",
            "alembic.ini": "# Alembic configuration\n[alembic]\nscript_location = alembic\n"
        }

        for filename, content in base_files.items():
            filepath = self.root_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    def run(self):
        """Execute the structure creation"""
        try:
            print("Starting project structure creation...")
            self.backup_existing()
            self.create_directory_structure()
            self.create_base_files()
            print("\nProject structure created successfully!")
            print(f"Backup created at: {self.backup_dir}")
            
            print("\nNext steps:")
            print("1. Review the created structure")
            print("2. Move existing code to appropriate directories")
            print("3. Update imports in your files")
            print("4. Install required dependencies")
            
        except Exception as e:
            print(f"Error during structure creation: {str(e)}")
            if self.backup_dir.exists():
                print("Rolling back changes...")
                if self.src_dir.exists():
                    shutil.rmtree(self.src_dir)
                shutil.copytree(self.backup_dir, self.src_dir)
            raise

if __name__ == "__main__":
    creator = ProjectStructureCreator()
    creator.run()

"""
Save this file as: create_project_structure.py
Location: ./scripts/create_project_structure.py
"""