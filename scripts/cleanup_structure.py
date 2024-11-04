"""
File: cleanup_structure.py
Location: ./scripts/cleanup_structure.py
Created: 2024-11-03
Purpose: Clean up and consolidate project structure
"""

import shutil
from pathlib import Path
import os

class StructureCleanup:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.src_dir = self.root_dir / "src" / "chatgfp"
        
    def cleanup_duplicates(self):
        """Consolidate duplicate directories and files"""
        print("Cleaning up duplicate structures...")
        
        # Move app/models content to /models if not already there
        if (self.root_dir / "app" / "models").exists():
            for file in (self.root_dir / "app" / "models").glob("*"):
                if file.is_file() and not (self.src_dir / "models" / file.name).exists():
                    shutil.copy2(file, self.src_dir / "models" / file.name)
            shutil.rmtree(self.root_dir / "app" / "models", ignore_errors=True)

        # Move app/services content to appropriate steps
        if (self.root_dir / "app" / "services").exists():
            service_mappings = {
                "embeddings.py": "steps/step_3_embedding/embeddings_generator.py",
                "retriever.py": "steps/step_4_retrieval/semantic_search.py",
                "vector_store.py": "steps/step_3_embedding/vector_store.py"
            }
            
            for source, dest in service_mappings.items():
                source_path = self.root_dir / "app" / "services" / source
                dest_path = self.src_dir / dest
                if source_path.exists() and not dest_path.exists():
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, dest_path)
            
            shutil.rmtree(self.root_dir / "app" / "services", ignore_errors=True)

        # Remove empty app directory if it exists
        if (self.root_dir / "app").exists():
            shutil.rmtree(self.root_dir / "app", ignore_errors=True)

    def organize_config_files(self):
        """Move configuration files to appropriate locations"""
        print("Organizing configuration files...")
        
        # Move root level configs to appropriate locations
        configs = {
            ".env": ".",  # Keep at root
            ".env.example": ".",  # Keep at root
            "alembic.ini": "core/database/",  # Move to database config
        }
        
        for file, dest in configs.items():
            source = self.root_dir / file
            if source.exists():
                if dest == ".":
                    continue  # Skip files that should stay at root
                destination = self.src_dir / dest / file
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                if dest != ".":  # Don't delete root level essential files
                    source.unlink()

    def organize_github_files(self):
        """Move GitHub related files to root"""
        print("Organizing GitHub files...")
        
        if (self.src_dir / ".github").exists():
            if not (self.root_dir / ".github").exists():
                shutil.move(self.src_dir / ".github", self.root_dir / ".github")
            else:
                shutil.rmtree(self.src_dir / ".github")

    def run(self):
        """Execute the cleanup process"""
        try:
            print("Starting structure cleanup...")
            self.cleanup_duplicates()
            self.organize_config_files()
            self.organize_github_files()
            print("Cleanup completed successfully!")
            
            print("\nNext steps:")
            print("1. Verify all files were moved correctly")
            print("2. Update any import statements that might have broken")
            print("3. Run your tests to ensure everything still works")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
            raise

if __name__ == "__main__":
    cleanup = StructureCleanup()
    cleanup.run()

"""
Save this file as: cleanup_structure.py
Location: ./scripts/cleanup_structure.py
"""