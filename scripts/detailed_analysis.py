"""
File: detailed_analysis.py
Location: ./scripts/detailed_analysis.py
Created: 2024-11-03
Purpose: Provide detailed analysis of current project structure
"""

import os
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

class DetailedProjectAnalyzer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir).resolve()
        self.ignore_patterns = {
            # Directories to ignore
            'dirs': {
                'venv', '__pycache__', '.git', '.pytest_cache', 
                'build', 'dist', 'migrations', '.idea'
            },
            # Files to ignore
            'files': {
                '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
                '.git', '.ds_store', '.env'
            }
        }
        
    def should_include(self, path: Path) -> bool:
        """Determine if path should be included in analysis"""
        if path.is_dir():
            return path.name not in self.ignore_patterns['dirs']
        return not any(path.name.lower().endswith(ext) for ext in self.ignore_patterns['files'])

    def analyze_directory(self, directory: Path, indent: str = "") -> List[str]:
        """Analyze directory contents with metadata"""
        results = []
        
        try:
            # Get all items in directory
            items = sorted(directory.iterdir(), 
                         key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                if not self.should_include(item):
                    continue
                    
                # Get relative path
                rel_path = item.relative_to(self.root_dir)
                
                if item.is_file():
                    # Get file metadata
                    size = item.stat().st_size
                    mod_time = datetime.fromtimestamp(item.stat().st_mtime)
                    
                    # Format size
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024*1024:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/(1024*1024):.1f} MB"
                    
                    results.append(f"{indent}├── {item.name} ({size_str}, modified: {mod_time:%Y-%m-%d %H:%M})")
                else:
                    results.append(f"{indent}├── {item.name}/")
                    # Recursively analyze subdirectories
                    sub_results = self.analyze_directory(item, indent + "│   ")
                    results.extend(sub_results)
                    
        except PermissionError:
            results.append(f"{indent}!── Permission denied: {directory.name}")
        except Exception as e:
            results.append(f"{indent}!── Error: {str(e)}")
            
        return results

    def analyze_python_files(self) -> Dict[str, List[str]]:
        """Analyze Python files for imports and dependencies"""
        python_files = {}
        
        for root, _, files in os.walk(self.root_dir):
            root_path = Path(root)
            if not self.should_include(root_path):
                continue
                
            for file in files:
                if file.endswith('.py'):
                    file_path = root_path / file
                    rel_path = file_path.relative_to(self.root_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Extract imports
                        imports = []
                        for line in content.split('\n'):
                            if line.strip().startswith(('import ', 'from ')):
                                imports.append(line.strip())
                                
                        python_files[str(rel_path)] = imports
                    except Exception as e:
                        python_files[str(rel_path)] = [f"Error reading file: {str(e)}"]
                        
        return python_files

    def run_analysis(self):
        """Run complete analysis"""
        print("\nDetailed Project Structure Analysis")
        print("=" * 50)
        
        # Directory structure analysis
        print("\nDirectory Structure:")
        print("-" * 30)
        structure = self.analyze_directory(self.root_dir)
        for line in structure:
            print(line)
            
        # Python file analysis
        print("\nPython Files Analysis:")
        print("-" * 30)
        python_files = self.analyze_python_files()
        
        for file_path, imports in python_files.items():
            print(f"\n{file_path}:")
            if imports:
                for imp in imports:
                    print(f"  {imp}")
            else:
                print("  No imports found")
                
        print("\nSummary:")
        print("-" * 30)
        print(f"Total Python files: {len(python_files)}")
        print(f"Total directories analyzed: {len([x for x in structure if x.endswith('/')])}")

if __name__ == "__main__":
    analyzer = DetailedProjectAnalyzer()
    analyzer.run_analysis()