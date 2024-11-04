"""
File: analyze_core_structure.py
Location: ./scripts/analyze_core_structure.py
Created: 2024-11-03
Purpose: Analyze only core project structure relevant to RAG implementation
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class CoreStructureAnalyzer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir).resolve()
        self.src_dir = self.root_dir / "src" / "chatgfp"
        
        # Define core project directories to analyze
        self.core_directories = {
            "steps": [
                "step_1_data_ingestion",
                "step_2_preprocessing",
                "step_3_embedding",
                "step_4_retrieval",
                "step_5_categorization"
            ],
            "core": [
                "auth",
                "database"
            ],
            "api/v1/endpoints": [],
            "models": [],
            "utils": []
        }

    def analyze_structure(self) -> Dict:
        """Analyze core structure implementation"""
        analysis = {
            "implemented": [],
            "missing": [],
            "extra": [],
            "files": {}
        }
        
        # Check core directories
        for main_dir, subdirs in self.core_directories.items():
            main_path = self.src_dir / main_dir
            
            if main_path.exists():
                analysis["implemented"].append(main_dir)
                analysis["files"][main_dir] = []
                
                # Check Python files in this directory
                for item in main_path.glob("*.py"):
                    if item.name != "__init__.py":
                        analysis["files"][main_dir].append(item.name)
                
                # Check subdirectories if specified
                for subdir in subdirs:
                    subdir_path = main_path / subdir
                    if subdir_path.exists():
                        analysis["implemented"].append(f"{main_dir}/{subdir}")
                        analysis["files"][f"{main_dir}/{subdir}"] = [
                            f.name for f in subdir_path.glob("*.py")
                            if f.name != "__init__.py"
                        ]
                    else:
                        analysis["missing"].append(f"{main_dir}/{subdir}")
            else:
                analysis["missing"].append(main_dir)

        return analysis

    def print_analysis(self):
        """Print formatted analysis results"""
        analysis = self.analyze_structure()
        
        print("\nCore Project Structure Analysis")
        print("=" * 50)
        
        print("\n📁 Implemented Structure:")
        print("-" * 30)
        for item in sorted(analysis["implemented"]):
            print(f"✓ {item}")
            if item in analysis["files"]:
                for file in sorted(analysis["files"][item]):
                    print(f"  └── {file}")
        
        if analysis["missing"]:
            print("\n❌ Missing Components:")
            print("-" * 30)
            for item in sorted(analysis["missing"]):
                print(f"• {item}")

        print("\n📊 Summary:")
        print("-" * 30)
        print(f"Implemented components: {len(analysis['implemented'])}")
        print(f"Missing components: {len(analysis['missing'])}")
        
        print("\n📝 Next Steps:")
        print("-" * 30)
        if analysis["missing"]:
            print("1. Implement missing components:")
            for item in sorted(analysis["missing"]):
                print(f"   - Create {item}")
        else:
            print("✓ All core components are implemented!")

if __name__ == "__main__":
    analyzer = CoreStructureAnalyzer()
    analyzer.print_analysis()

"""
Save this file as: analyze_core_structure.py
Location: ./scripts/analyze_core_structure.py
"""