"""
File: create_safe_structure.py
Location: ./scripts/create_safe_structure.py
Created: 2024-11-03
Purpose: Safely create the step-based project structure
Changes: Added recursion safety and better error handling
"""

import os
from pathlib import Path
import shutil
from datetime import datetime
import sys

# Increase recursion limit for deep directories
sys.setrecursionlimit(10000)

class SafeProjectCreator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir).resolve()  # Get absolute path
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = self.root_dir / f"backup_{self.timestamp}"
        self.src_dir = self.root_dir / "src" / "chatgfp"

    def safe_create_dir(self, path: Path):
        """Safely create directory"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {path}: {str(e)}")
            return False

    def safe_create_file(self, path: Path, content: str = ""):
        """Safely create file with content"""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file {path}: {str(e)}")
            return False

    def create_structure(self):
        """Create the project structure"""
        print("Creating project structure...")
        
        # Create main source directory
        if not self.safe_create_dir(self.src_dir):
            return False

        # Create step directories
        steps = ['step_1_data_ingestion', 'step_2_preprocessing', 
                'step_3_embedding', 'step_4_retrieval', 'step_5_categorization']
        
        for step in steps:
            step_dir = self.src_dir / 'steps' / step
            if not self.safe_create_dir(step_dir):
                return False
            
            # Create __init__.py
            self.safe_create_file(step_dir / '__init__.py')
            
            # Create step-specific files
            if step == 'step_1_data_ingestion':
                files = ['document_loader.py', 'text_extractor.py', 'data_validator.py']
            elif step == 'step_2_preprocessing':
                files = ['text_cleaner.py', 'chunker.py', 'metadata_extractor.py']
            elif step == 'step_3_embedding':
                files = ['embeddings_generator.py', 'vector_store.py', 'index_manager.py']
            elif step == 'step_4_retrieval':
                files = ['query_processor.py', 'semantic_search.py', 'result_ranker.py']
            elif step == 'step_5_categorization':
                files = ['fca_analyzer.py', 'category_mapper.py', 'compliance_checker.py']
            
            for file in files:
                self.safe_create_file(step_dir / file)

        # Create core directory
        core_dir = self.src_dir / 'core'
        self.safe_create_dir(core_dir)
        self.safe_create_file(core_dir / '__init__.py')
        self.safe_create_file(core_dir / 'config.py')
        self.safe_create_file(core_dir / 'security.py')
        
        # Create core subdirectories
        for subdir in ['auth', 'database']:
            subdir_path = core_dir / subdir
            self.safe_create_dir(subdir_path)
            self.safe_create_file(subdir_path / '__init__.py')

        # Create API directory structure
        api_dir = self.src_dir / 'api' / 'v1' / 'endpoints'
        self.safe_create_dir(api_dir)
        self.safe_create_file(api_dir / '__init__.py')
        
        for endpoint in ['ingestion.py', 'processing.py', 'embedding.py', 
                        'retrieval.py', 'categorization.py']:
            self.safe_create_file(api_dir / endpoint)

        # Create models directory
        models_dir = self.src_dir / 'models'
        self.safe_create_dir(models_dir)
        self.safe_create_file(models_dir / '__init__.py')
        
        for model in ['document.py', 'embedding.py', 'categorization.py']:
            self.safe_create_file(models_dir / model)

        # Create tests directory
        tests_dir = self.src_dir / 'tests'
        self.safe_create_dir(tests_dir)
        self.safe_create_file(tests_dir / '__init__.py')
        self.safe_create_file(tests_dir / 'conftest.py')
        
        for step in range(1, 6):
            step_test_dir = tests_dir / f'step_{step}'
            self.safe_create_dir(step_test_dir)
            self.safe_create_file(step_test_dir / '__init__.py')

        # Create utils directory
        utils_dir = self.src_dir / 'utils'
        self.safe_create_dir(utils_dir)
        self.safe_create_file(utils_dir / '__init__.py')
        
        for util in ['monitoring.py', 'health_check.py', 'helpers.py']:
            self.safe_create_file(utils_dir / util)

        return True

    def run(self):
        """Execute the structure creation"""
        try:
            print(f"Starting safe project creation in {self.src_dir}")
            if self.create_structure():
                print("\nProject structure created successfully!")
                print("\nNext steps:")
                print("1. Review the created structure")
                print("2. Move your existing code into appropriate directories")
                print("3. Update import statements")
                return True
            return False
        except Exception as e:
            print(f"Error during creation: {str(e)}")
            return False

if __name__ == "__main__":
    creator = SafeProjectCreator()
    success = creator.run()
    sys.exit(0 if success else 1)

"""
Save this file as: create_safe_structure.py
Location: ./scripts/create_safe_structure.py
"""