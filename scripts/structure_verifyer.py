"""
File: structure_verifier.py
Location: ./scripts/migration/structure_verifier.py
Created: 2024-11-03
Purpose: Verify the correctness of the migrated project structure
"""

import os
from pathlib import Path
from typing import List, Dict
import importlib
import sys

class StructureVerifier:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.src_dir = self.root_dir / "src" / "chatgfp"
        self.required_structure = {
            "steps": {
                "step_1_data_ingestion": ["document_loader.py", "text_extractor.py", "data_validator.py"],
                "step_2_preprocessing": ["text_cleaner.py", "chunker.py", "metadata_extractor.py"],
                "step_3_embedding": ["embeddings_generator.py", "vector_store.py", "index_manager.py"],
                "step_4_retrieval": ["query_processor.py", "semantic_search.py", "result_ranker.py"],
                "step_5_categorization": ["fca_analyzer.py", "category_mapper.py", "compliance_checker.py"]
            },
            "core": ["auth", "database", "config.py", "security.py"],
            "api/v1/endpoints": [
                "ingestion.py", "processing.py", "embedding.py", 
                "retrieval.py", "categorization.py"
            ],
            "models": ["document.py", "embedding.py", "categorization.py"],
            "tests": ["step_1", "step_2", "step_3", "step_4", "step_5", "conftest.py"],
            "utils": ["monitoring.py", "health_check.py", "helpers.py"]
        }

    def verify_structure(self) -> List[str]:
        """Verify the project structure"""
        issues = []
        
        for dir_path, required_items in self.required_structure.items():
            full_path = self.src_dir / dir_path
            
            if not full_path.exists():
                issues.append(f"Missing directory: {dir_path}")
                continue
                
            for item in required_items:
                item_path = full_path / item
                if not item_path.exists():
                    issues.append(f"Missing file/directory: {dir_path}/{item}")

        return issues

    def verify_imports(self) -> List[str]:
        """Verify Python imports work correctly"""
        issues = []
        original_path = sys.path.copy()
        
        try:
            sys.path.insert(0, str(self.root_dir))
            
            # Test core imports
            test_imports = [
                "src.chatgfp.steps.step_1_data_ingestion.document_loader",
                "src.chatgfp.steps.step_3_embedding.embeddings_generator",
                "src.chatgfp.models.document",
                "src.chatgfp.core.config"
            ]
            
            for import_path in test_imports:
                try:
                    importlib.import_module(import_path)
                except ImportError as e:
                    issues.append(f"Import failed for {import_path}: {str(e)}")
                
        finally:
            sys.path = original_path
            
        return issues

    def verify_file_contents(self) -> List[str]:
        """Verify file contents meet basic requirements"""
        issues = []
        
        for py_file in self.src_dir.rglob("*.py"):
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for docstring
            if not content.strip().startswith('"""'):
                issues.append(f"Missing docstring in {py_file.relative_to(self.src_dir)}")
                
            # Check for old import patterns
            if "from app." in content:
                issues.append(f"Found old import 'from app.' in {py_file.relative_to(self.src_dir)}")
                
        return issues

    def run_verification(self) -> bool:
        """Run all verifications"""
        print("Starting structure verification...")
        
        structure_issues = self.verify_structure()
        import_issues = self.verify_imports()
        content_issues