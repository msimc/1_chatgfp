"""
File: verify_structure.py
Location: ./scripts/verify_structure.py
Created: 2024-11-03
Purpose: Clean verification of core project structure only
"""

import os
from pathlib import Path

def verify_structure(base_path="src/chatgfp"):
    # Directories and files to exclude
    exclude_dirs = {
        '__pycache__',
        'venv',
        '.git',
        '.vscode',
        '.idea',
        'node_modules',
        '.pytest_cache',
        'build',
        'dist',
        'backups',
        'migrations',
        'fca_categorization.egg-info'
    }
    
    exclude_files = {
        '.gitignore',
        '.env',
        '.DS_Store',
        'Thumbs.db',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.python-version'
    }

    base = Path(base_path)
    
    print(f"\nVerifying core project structure in {base}...")
    print("=" * 50)
    
    def should_include(path: Path) -> bool:
        """Determine if path should be included in verification"""
        # Check if any parent directory should be excluded
        for parent in path.parents:
            if parent.name in exclude_dirs:
                return False
        
        # Check the path itself
        if path.is_dir():
            return path.name not in exclude_dirs
        else:
            return not any(path.name.endswith(pat.replace('*', '')) 
                         for pat in exclude_files)

    def print_tree(directory: Path, prefix: str = ""):
        """Print directory tree structure"""
        try:
            # Get all valid paths
            paths = sorted(
                [p for p in directory.iterdir() if should_include(p)],
                key=lambda x: (x.is_file(), x.name.lower())
            )

            # Print each path
            for i, path in enumerate(paths):
                is_last = i == len(paths) - 1
                connector = '└──' if is_last else '├──'
                print(f"{prefix}{connector} {path.name}")
                
                if path.is_dir():
                    extension = '    ' if is_last else '│   '
                    print_tree(path, prefix=prefix + extension)

        except PermissionError:
            print(f"{prefix}!── Permission denied: {directory}")
        except Exception as e:
            print(f"{prefix}!── Error reading {directory}: {str(e)}")

    # Verify main project components
    if base.exists():
        print("\nCore Project Structure:")
        print_tree(base)
        
        # Verify essential directories exist
        essential_dirs = [
            "steps/step_1_data_ingestion",
            "steps/step_2_preprocessing",
            "steps/step_3_embedding",
            "steps/step_4_retrieval",
            "steps/step_5_categorization",
            "core",
            "api/v1/endpoints",
            "models",
            "tests",
            "utils"
        ]
        
        print("\nVerifying essential directories:")
        print("-" * 30)
        for dir_path in essential_dirs:
            full_path = base / dir_path
            status = "✓ Present" if full_path.exists() else "✗ Missing"
            print(f"{dir_path}: {status}")
            
    else:
        print(f"\nError: Base directory {base} does not exist!")

if __name__ == "__main__":
    verify_structure()

"""
Save this file as: verify_structure.py
Location: ./scripts/verify_structure.py
"""