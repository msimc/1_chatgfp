"""
File: analyze_structure.py
Location: ./scripts/analyze_structure.py
Created: 2024-11-03
Purpose: Analyze current project structure and identify needed changes
"""

import os
from pathlib import Path
from typing import Dict, List, Set
import json

class ProjectAnalyzer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir).resolve()
        self.src_dir = self.root_dir / "src" / "chatgfp"
        
        # Define expected structure
        self.expected_structure = {
            "steps": {
                "step_1_data_ingestion": {
                    "files": ["document_loader.py", "text_extractor.py", "data_validator.py"],
                    "sources": ["pdf_processing", "app/services"]
                },
                "step_2_preprocessing": {
                    "files": ["text_cleaner.py", "chunker.py", "metadata_extractor.py"],
                    "sources": ["app/services"]
                },
                "step_3_embedding": {
                    "files": ["embeddings_generator.py", "vector_store.py", "index_manager.py"],
                    "sources": ["app/services/embeddings.py", "app/services/vector_store.py"]
                },
                "step_4_retrieval": {
                    "files": ["query_processor.py", "semantic_search.py", "result_ranker.py"],
                    "sources": ["app/services/retriever.py"]
                },
                "step_5_categorization": {
                    "files": ["fca_analyzer.py", "category_mapper.py", "compliance_checker.py"],
                    "sources": ["src/fca_categorization/models.py"]
                }
            }
        }

    def find_duplicates(self) -> Dict[str, List[str]]:
        """Find duplicate files/functionality across the project"""
        duplicates = {}
        
        # Check for model duplicates
        if (self.root_dir / "app" / "models").exists() and (self.src_dir / "models").exists():
            duplicates["models"] = [
                str(self.root_dir / "app" / "models"),
                str(self.src_dir / "models")
            ]
        
        # Check for service duplicates
        if (self.root_dir / "app" / "services").exists() and (self.src_dir / "steps").exists():
            duplicates["services"] = [
                str(self.root_dir / "app" / "services"),
                str(self.src_dir / "steps")
            ]
            
        return duplicates

    def analyze_structure(self) -> Dict:
        """Analyze current structure against expected"""
        analysis = {
            "missing_directories": [],
            "missing_files": [],
            "duplicates": self.find_duplicates(),
            "misplaced_files": [],
            "suggestions": []
        }
        
        # Check expected structure
        for step, details in self.expected_structure["steps"].items():
            step_dir = self.src_dir / "steps" / step
            if not step_dir.exists():
                analysis["missing_directories"].append(f"steps/{step}")
            else:
                for file in details["files"]:
                    if not (step_dir / file).exists():
                        analysis["missing_files"].append(f"steps/{step}/{file}")
        
        # Look for misplaced files
        for root, _, files in os.walk(self.root_dir):
            root_path = Path(root)
            if any(p.name in {".git", "venv", "__pycache__"} for p in root_path.parents):
                continue
                
            for file in files:
                if file.endswith(".py"):
                    file_path = root_path / file
                    rel_path = file_path.relative_to(self.root_dir)
                    
                    # Check if file should be moved to steps
                    for step, details in self.expected_structure["steps"].items():
                        if str(rel_path) in details["sources"]:
                            analysis["misplaced_files"].append({
                                "current": str(rel_path),
                                "suggested": f"steps/{step}/{file}"
                            })
        
        return analysis

    def print_analysis(self):
        """Print detailed analysis"""
        analysis = self.analyze_structure()
        
        print("\nProject Structure Analysis")
        print("=" * 50)
        
        if analysis["duplicates"]:
            print("\n🔄 Duplicate Functionality Found:")
            for category, locations in analysis["duplicates"].items():
                print(f"\n  {category}:")
                for loc in locations:
                    print(f"    - {loc}")
        
        if analysis["missing_directories"]:
            print("\n📁 Missing Directories:")
            for dir_path in analysis["missing_directories"]:
                print(f"  - {dir_path}")
        
        if analysis["missing_files"]:
            print("\n📄 Missing Files:")
            for file_path in analysis["missing_files"]:
                print(f"  - {file_path}")
        
        if analysis["misplaced_files"]:
            print("\n🔄 Files to Move:")
            for file in analysis["misplaced_files"]:
                print(f"  Move: {file['current']}")
                print(f"    To: {file['suggested']}")
        
        if not any([analysis["duplicates"], analysis["missing_directories"], 
                   analysis["missing_files"], analysis["misplaced_files"]]):
            print("\n✅ Project structure looks good! No changes needed.")
        else:
            print("\nSuggested Actions:")
            print("1. First resolve duplicate functionality")
            print("2. Move misplaced files to their suggested locations")
            print("3. Create any missing directories and files")
            print("4. Update import statements after moving files")

if __name__ == "__main__":
    analyzer = ProjectAnalyzer()
    analyzer.print_analysis()

"""
Save this file as: analyze_structure.py
Location: ./scripts/analyze_structure.py
"""