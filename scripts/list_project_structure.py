"""
File: list_project_structure.py
Location: ./scripts/list_project_structure.py
Created: 2024-11-03
Updated: 2024-11-03
Purpose: Generate a clean project structure overview with proper encoding
Changes: Added UTF-8 encoding support and better error handling
"""

import os
from pathlib import Path
from typing import Set
import sys

def list_project_structure(
    start_path: str = ".",
    max_depth: int = 3,
    exclude_dirs: Set[str] = {
        "venv", "__pycache__", ".git", ".idea", ".pytest_cache", 
        "node_modules", ".next", "build", "dist"
    },
    exclude_files: Set[str] = {
        ".pyc", ".pyo", ".pyd", ".DS_Store"
    }
) -> str:
    output = []
    start_path = Path(start_path)

    def should_include(path: Path) -> bool:
        if any(parent.name in exclude_dirs for parent in path.parents):
            return False
        
        if path.is_file():
            if path.suffix in exclude_files or path.name in exclude_files:
                return False
        
        return path.name not in exclude_dirs

    def add_to_output(path: Path, depth: int) -> None:
        if depth > max_depth:
            return

        indent = "    " * (depth - 1)
        if depth > 0:
            prefix = "├── " if depth > 0 else ""
            output.append(f"{indent}{prefix}{path.name}")

        if path.is_dir():
            items = sorted(
                [p for p in path.iterdir() if should_include(p)],
                key=lambda p: (p.is_file(), p.name.lower())
            )
            
            for item in items:
                add_to_output(item, depth + 1)

    output.append(f"Project Structure for: {start_path.absolute().name}")
    output.append("=" * 50)
    add_to_output(start_path, 0)

    return "\n".join(output)

if __name__ == "__main__":
    try:
        # Get command line arguments
        path = sys.argv[1] if len(sys.argv) > 1 else "."
        
        # Generate structure
        structure = list_project_structure(path)
        
        # Print to console
        print(structure)
        
        # Save to file with UTF-8 encoding
        with open("project_structure.txt", "w", encoding='utf-8') as f:
            f.write(structure)
        
        print("\nStructure has been saved to 'project_structure.txt'")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

"""
Save this file as: list_project_structure.py
Location: ./scripts/list_project_structure.py
Usage: python scripts/list_project_structure.py [path]
"""