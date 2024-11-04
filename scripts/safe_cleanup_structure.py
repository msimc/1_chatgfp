"""
File: safe_cleanup_structure.py
Location: ./scripts/safe_cleanup_structure.py
Created: 2024-11-03
Purpose: Safely clean up project structure with detailed reporting
"""

import shutil
from pathlib import Path
import os
import sys
from typing import Dict, List

class SafeStructureCleanup:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir).resolve()
        self.src_dir = self.root_dir / "src" / "chatgfp"
        self.venv_dir = self.root_dir / "venv"
        self.changes_made: Dict[str, List[str]] = {
            "moved": [],
            "skipped": [],
            "cleaned": []
        }
        
        self.protected_dirs = {
            "venv",
            ".git",
            ".vscode",
            "__pycache__",
            ".pytest_cache"
        }

    def log_change(self, change_type: str, item: str):
        """Log changes for reporting"""
        self.changes_made[change_type].append(item)

    def print_changes(self):
        """Print detailed change report"""
        print("\nChanges Report:")
        print("=" * 50)
        
        if self.changes_made["moved"]:
            print("\nFiles Moved:")
            for item in self.changes_made["moved"]:
                print(f"  ✓ {item}")
        
        if self.changes_made["cleaned"]:
            print("\nCleaned Up:")
            for item in self.changes_made["cleaned"]:
                print(f"  ✓ {item}")
        
        if self.changes_made["skipped"]:
            print("\nSkipped (Protected):")
            for item in self.changes_made["skipped"]:
                print(f"  • {item}")

    def safe_move(self, source: Path, dest: Path):
        """Safely move files with logging"""
        if not source.exists():
            return
            
        if self.is_protected(source) or self.is_protected(dest):
            self.log_change("skipped", f"{source} (protected)")
            return
            
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(source, dest)
                self.log_change("moved", f"{source} → {dest}")
                if source.is_file():
                    source.unlink()
                    self.log_change("cleaned", str(source))
                elif not any(self.is_protected(p) for p in source.rglob("*")):
                    shutil.rmtree(source)
                    self.log_change("cleaned", str(source))
        except Exception as e:
            print(f"Error moving {source} to {dest}: {e}")

    def is_protected(self, path: Path) -> bool:
        return any(parent.name in self.protected_dirs 
                  for parent in path.parents) or path.name in self.protected_dirs

    def cleanup_duplicates(self):
        """Consolidate duplicate directories and files"""
        print("\nCleaning up duplicate structures...")
        
        # Define mappings for files to move
        mappings = {
            "app/models": {
                "document.py": "models/document.py",
                "embedding.py": "models/embedding.py"
            },
            "app/services": {
                "embeddings.py": "steps/step_3_embedding/embeddings_generator.py",
                "retriever.py": "steps/step_4_retrieval/semantic_search.py",
                "vector_store.py": "steps/step_3_embedding/vector_store.py"
            }
        }

        for source_dir, files in mappings.items():
            source_path = self.root_dir / source_dir
            if source_path.exists():
                for file, dest in files.items():
                    self.safe_move(source_path / file, self.src_dir / dest)

    def verify_venv(self) -> bool:
        """Verify virtual environment is intact"""
        if not self.venv_dir.exists():
            print("⚠️ Warning: Virtual environment not found!")
            return False
            
        activate_script = self.venv_dir / "Scripts" / "activate"
        if not activate_script.exists():
            print("⚠️ Warning: Virtual environment activation script not found!")
            return False
            
        print("✓ Virtual environment verified successfully!")
        return True

    def run(self):
        """Execute the cleanup process"""
        try:
            print("\nStarting safe structure cleanup...")
            print(f"Project root: {self.root_dir}")
            print(f"Virtual environment: {self.venv_dir}")
            
            if not self.verify_venv():
                raise Exception("Virtual environment verification failed!")
            
            self.cleanup_duplicates()
            
            if not self.verify_venv():
                raise Exception("Virtual environment was affected by cleanup!")
                
            self.print_changes()
            
            print("\n✓ Cleanup completed successfully!")
            print("\nNext steps:")
            print("1. Review the changes report above")
            print("2. Update any import statements in moved files")
            print("3. Run your tests to verify functionality")
            
            if self.changes_made["moved"]:
                print("\nIf your virtual environment deactivates, run:")
                print("    deactivate")
                print("    .\\venv\\Scripts\\activate")
            
        except Exception as e:
            print(f"\n❌ Error during cleanup: {str(e)}")
            return False
            
        return True

if __name__ == "__main__":
    cleanup = SafeStructureCleanup()
    success = cleanup.run()
    sys.exit(0 if success else 1)