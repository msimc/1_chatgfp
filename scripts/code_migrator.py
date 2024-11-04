"""
File: code_migrator.py
Location: ./scripts/migration/code_migrator.py
Created: 2024-11-03
Purpose: Migrate existing code to new step-based structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

class CompleteMigrator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.backup_dir = self.root_dir / f"backups/full_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.new_src_dir = self.root_dir / "src" / "chatgfp"

    def backup_project(self):
        """Create complete project backup"""
        print(f"Creating backup in {self.backup_dir}")
        shutil.copytree(
            self.root_dir,
            self.backup_dir,
            ignore=shutil.ignore_patterns('venv', '__pycache__', '*.pyc', '.git')
        )

    def setup_new_structure(self):
        """Create new directory structure"""
        # Create main directories
        directories = [
            "steps/step_1_data_ingestion",
            "steps/step_2_preprocessing",
            "steps/step_3_embedding",
            "steps/step_4_retrieval",
            "steps/step_5_categorization",
            "core/auth",
            "core/database",
            "api/v1/endpoints",
            "models",
            "tests/step_1",
            "tests/step_2",
            "tests/step_3",
            "tests/step_4",
            "tests/step_5",
            "utils"
        ]

        for dir_path in directories:
            full_path = self.new_src_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            (full_path / "__init__.py").touch()

    def migrate_files(self):
        """Migrate files to new structure"""
        migrations = {
            # Step 1: Data Ingestion
            "pdf_processing": "steps/step_1_data_ingestion",
            
            # Step 2: Preprocessing
            "app/services/text_processor.py": "steps/step_2_preprocessing/text_cleaner.py",
            
            # Step 3: Embedding
            "app/services/embeddings.py": "steps/step_3_embedding/embeddings_generator.py",
            "app/services/vector_store.py": "steps/step_3_embedding/vector_store.py",
            
            # Step 4: Retrieval
            "app/services/retriever.py": "steps/step_4_retrieval/semantic_search.py",
            
            # Step 5: Categorization
            "src/fca_categorization/models.py": "steps/step_5_categorization/fca_analyzer.py",
            
            # Core components
            "auth": "core/auth",
            "database": "core/database",
            
            # Models
            "app/models/document.py": "models/document.py",
            "app/models/embedding.py": "models/embedding.py",
            
            # Tests
            "fca_queries": "tests",
            
            # Utils
            "postgres/postgres_monitor.py": "utils/monitoring.py",
            "postgres/postgres_health.py": "utils/health_check.py"
        }

        for source, dest in migrations.items():
            self._migrate_single_file_or_dir(source, dest)

    def _migrate_single_file_or_dir(self, source: str, destination: str):
        """Migrate a single file or directory"""
        source_path = self.root_dir / source
        dest_path = self.new_src_dir / destination

        if source_path.exists():
            if source_path.is_file():
                self._migrate_file(source_path, dest_path)
            else:
                self._migrate_directory(source_path, dest_path)

    def _migrate_file(self, source_path: Path, dest_path: Path):
        """Migrate a single file with import updates"""
        print(f"Migrating {source_path.relative_to(self.root_dir)} to {dest_path.relative_to(self.new_src_dir)}")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update imports
        content = self._update_imports(content)

        # Add file header
        header = f'''"""
File: {dest_path.name}
Location: src/chatgfp/{dest_path.relative_to(self.new_src_dir)}
Migrated: {datetime.now().strftime('%Y-%m-%d')}
Original: {source_path.relative_to(self.root_dir)}
"""

'''
        content = header + content

        # Write to new location
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _migrate_directory(self, source_path: Path, dest_path: Path):
        """Migrate an entire directory"""
        for item in source_path.rglob('*'):
            if item.is_file() and not item.name.startswith('.'):
                rel_path = item.relative_to(source_path)
                new_dest = dest_path / rel_path
                self._migrate_file(item, new_dest)

    def _update_imports(self, content: str) -> str:
        """Update import statements to match new structure"""
        import_maps = {
            r'from app\.': 'from src.chatgfp.',
            r'from pdf_processing\.': 'from src.chatgfp.steps.step_1_data_ingestion.',
            r'from auth\.': 'from src.chatgfp.core.auth.',
            r'from database\.': 'from src.chatgfp.core.database.'
        }

        for old, new in import_maps.items():
            content = re.sub(old, new, content)

        return content

    def run(self):
        """Execute the complete migration"""
        try:
            print("Starting complete project migration...")
            self.backup_project()
            self.setup_new_structure()
            self.migrate_files()
            print("Migration completed successfully!")
            print(f"Backup created at: {self.backup_dir}")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            print("Rolling back changes...")
            if self.new_src_dir.exists():
                shutil.rmtree(self.new_src_dir)
            raise

if __name__ == "__main__":
    migrator = CompleteMigrator()
    migrator.run()

"""
Save this file as: code_migrator.py
Location: ./scripts/migration/code_migrator.py
"""