import os
from pathlib import Path
import ast
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import textwrap

@dataclass
class RAGPattern:
    """Definition of a RAG implementation pattern"""
    name: str
    required_methods: List[str]
    required_imports: List[str]
    example_implementation: str

class CompleteImplementationAnalyzer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir).resolve()
        self.src_dir = self.root_dir / "src" / "chatgfp"
        
        # Initialize expected implementations
        self.expected_implementations = {
            "steps/step_1_data_ingestion": {
                "document_loader.py": {
                    "classes": ["DocumentLoader"],
                    "methods": ["load_document", "validate_document"],
                    "required_imports": ["pathlib", "typing"]
                },
                "text_extractor.py": {
                    "classes": ["TextExtractor"],
                    "methods": ["extract_text"],
                    "required_imports": ["typing"]
                },
                "data_validator.py": {
                    "classes": ["DataValidator"],
                    "methods": ["validate"],
                    "required_imports": ["typing", "pydantic"]
                }
            },
            "steps/step_2_preprocessing": {
                "text_cleaner.py": {
                    "classes": ["TextCleaner"],
                    "methods": ["clean_text", "normalize"],
                    "required_imports": ["re", "typing"]
                },
                "chunker.py": {
                    "classes": ["TextChunker"],
                    "methods": ["create_chunks"],
                    "required_imports": ["typing"]
                },
                "metadata_extractor.py": {
                    "classes": ["MetadataExtractor"],
                    "methods": ["extract_metadata"],
                    "required_imports": ["typing", "json"]
                }
            },
            "steps/step_3_embedding": {
                "embeddings_generator.py": {
                    "classes": ["EmbeddingGenerator"],
                    "methods": ["generate_embeddings", "batch_generate", "cache_embeddings"],
                    "required_imports": ["sentence_transformers", "numpy", "typing"]
                },
                "vector_store.py": {
                    "classes": ["VectorStore"],
                    "methods": ["add_vectors", "search", "delete_vectors"],
                    "required_imports": ["faiss", "numpy", "typing"]
                },
                "index_manager.py": {
                    "classes": ["IndexManager"],
                    "methods": ["create_index", "load_index", "save_index"],
                    "required_imports": ["faiss", "typing"]
                }
            },
            "steps/step_4_retrieval": {
                "query_processor.py": {
                    "classes": ["QueryProcessor"],
                    "methods": ["process_query"],
                    "required_imports": ["typing"]
                },
                "semantic_search.py": {
                    "classes": ["SemanticSearch"],
                    "methods": ["search"],
                    "required_imports": ["numpy", "typing"]
                },
                "result_ranker.py": {
                    "classes": ["ResultRanker"],
                    "methods": ["rank_results"],
                    "required_imports": ["typing"]
                }
            },
            "steps/step_5_categorization": {
                "fca_analyzer.py": {
                    "classes": ["FCAAnalyzer"],
                    "methods": ["analyze"],
                    "required_imports": ["typing"]
                },
                "category_mapper.py": {
                    "classes": ["CategoryMapper"],
                    "methods": ["map_categories"],
                    "required_imports": ["typing"]
                },
                "compliance_checker.py": {
                    "classes": ["ComplianceChecker"],
                    "methods": ["check_compliance"],
                    "required_imports": ["typing"]
                }
            }
        }

        # Define RAG patterns
        self.rag_patterns = {
            "embeddings_generator.py": RAGPattern(
                name="Embedding Generation",
                required_methods=["generate_embeddings", "batch_generate", "cache_embeddings"],
                required_imports=["sentence_transformers", "numpy"],
                example_implementation=self._get_embedding_template()
            ),
            "vector_store.py": RAGPattern(
                name="Vector Storage",
                required_methods=["add_vectors", "search", "delete_vectors"],
                required_imports=["faiss", "numpy"],
                example_implementation=self._get_vectorstore_template()
            )
        }

    def _get_embedding_template(self) -> str:
        return textwrap.dedent('''
            """Embedding generator implementation"""
            from sentence_transformers import SentenceTransformer
            import numpy as np
            from typing import List, Optional
            
            class EmbeddingGenerator:
                def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
                    self.model = SentenceTransformer(model_name)
                    self.cache = {}
                
                async def generate_embeddings(self, text: str) -> np.ndarray:
                    if text in self.cache:
                        return self.cache[text]
                    embedding = self.model.encode(text)
                    self.cache[text] = embedding
                    return embedding
                
                async def batch_generate(self, texts: List[str]) -> np.ndarray:
                    return self.model.encode(texts)
                
                def cache_embeddings(self, texts: List[str]) -> None:
                    embeddings = self.model.encode(texts)
                    for text, emb in zip(texts, embeddings):
                        self.cache[text] = emb
        ''')

    def _get_vectorstore_template(self) -> str:
        return textwrap.dedent('''
            """Vector store implementation"""
            import faiss
            import numpy as np
            from typing import List, Dict, Optional
            
            class VectorStore:
                def __init__(self, dimension: int):
                    self.index = faiss.IndexFlatL2(dimension)
                    self.id_map = {}
                
                def add_vectors(self, vectors: np.ndarray, ids: List[int]) -> None:
                    self.index.add(vectors)
                    for i, id in enumerate(ids):
                        self.id_map[i] = id
                
                def search(self, query_vector: np.ndarray, k: int = 5) -> Dict[int, float]:
                    distances, indices = self.index.search(query_vector.reshape(1, -1), k)
                    return {self.id_map[i]: float(d) for i, d in zip(indices[0], distances[0])}
                
                def delete_vectors(self, ids: List[int]) -> None:
                    # Implementation for vector deletion
                    pass
        ''')

    def analyze_file_implementation(self, file_path: Path) -> Dict:
        default_analysis = {
            "classes": [],
            "functions": [],
            "imports": [],
            "has_docstrings": False,
            "has_type_hints": False,
            "error": None
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            analysis = default_analysis.copy()
            
            if (len(tree.body) > 0 and 
                isinstance(tree.body[0], ast.Expr) and 
                isinstance(tree.body[0].value, ast.Str)):
                analysis["has_docstrings"] = True
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(node.name)
                    if node.returns or any(arg.annotation for arg in node.args.args):
                        analysis["has_type_hints"] = True
                elif isinstance(node, ast.Import):
                    analysis["imports"].extend(n.name for n in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    analysis["imports"].append(node.module)
            
            file_name = file_path.name
            if file_name in self.rag_patterns:
                pattern = self.rag_patterns[file_name]
                analysis["rag_pattern"] = {
                    "name": pattern.name,
                    "missing_methods": set(pattern.required_methods) - set(analysis["functions"]),
                    "missing_imports": set(pattern.required_imports) - set(analysis["imports"])
                }
            
            return analysis
            
        except Exception as e:
            default_analysis["error"] = str(e)
            return default_analysis

    def save_analysis_report(self, issues: List[str]) -> None:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rag_analysis_report_{timestamp_str}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("RAG Implementation Analysis Report\n")
                f.write("=" * 50 + "\n\n")
                
                if issues:
                    f.write("🔍 Implementation Issues:\n")
                    f.write("-" * 20 + "\n")
                    for issue in issues:
                        f.write(f"• {issue}\n")
                else:
                    f.write("✓ No implementation issues found!\n")
                
                f.write("\n📝 Next Steps:\n")
                f.write("-" * 20 + "\n")
                f.write("1. Implement missing components\n")
                f.write("2. Add docstrings to all files\n")
                f.write("3. Add type hints for better code quality\n")
                f.write("4. Complete RAG pattern implementations\n")
                
                f.write(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            print(f"\nAnalysis report saved to: {filename}")
            
        except Exception as e:
            print(f"\n❌ Error saving report: {str(e)}")

    def run(self):
        print("\nRAG Implementation Analysis")
        print("=" * 50)
        
        all_issues = []
        
        for component_path, files in self.expected_implementations.items():
            print(f"\n📂 {component_path}")
            component_dir = self.src_dir / component_path
            
            if not component_dir.exists():
                all_issues.append(f"Missing directory: {component_path}")
                print(f"  ❌ Directory not found")
                continue
            
            for file_name, expected in files.items():
                file_path = component_dir / file_name
                if not file_path.exists():
                    all_issues.append(f"Missing file: {component_path}/{file_name}")
                    print(f"  ❌ {file_name} not found")
                    continue
                
                print(f"\n  📄 {file_name}:")
                analysis = self.analyze_file_implementation(file_path)
                
                if analysis.get("error"):
                    all_issues.append(f"Analysis error in {file_name}: {analysis['error']}")
                    print(f"    ❌ Error analyzing file: {analysis['error']}")
                    continue
                
                missing_classes = set(expected["classes"]) - set(analysis["classes"])
                missing_methods = set(expected["methods"]) - set(analysis["functions"])
                missing_imports = set(expected["required_imports"]) - set(analysis["imports"])
                
                if missing_classes or missing_methods or missing_imports:
                    if missing_classes:
                        all_issues.append(f"Missing classes in {file_name}: {missing_classes}")
                        print(f"    ❌ Missing classes: {', '.join(missing_classes)}")
                    if missing_methods:
                        all_issues.append(f"Missing methods in {file_name}: {missing_methods}")
                        print(f"    ❌ Missing methods: {', '.join(missing_methods)}")
                    if missing_imports:
                        all_issues.append(f"Missing imports in {file_name}: {missing_imports}")
                        print(f"    ❌ Missing imports: {', '.join(missing_imports)}")
                else:
                    print(f"    ✓ Core implementation complete")
                
                if "rag_pattern" in analysis:
                    pattern_info = analysis["rag_pattern"]
                    if pattern_info["missing_methods"] or pattern_info["missing_imports"]:
                        print(f"    ⚠️ RAG Pattern '{pattern_info['name']}' incomplete:")
                        if pattern_info["missing_methods"]:
                            all_issues.append(f"Missing RAG methods in {file_name}: {pattern_info['missing_methods']}")
                            print(f"      Missing methods: {', '.join(pattern_info['missing_methods'])}")
                        if pattern_info["missing_imports"]:
                            all_issues.append(f"Missing RAG imports in {file_name}: {pattern_info['missing_imports']}")
                            print(f"      Missing imports: {', '.join(pattern_info['missing_imports'])}")
                
                print(f"    Documentation: {'✓' if analysis['has_docstrings'] else '❌'}")
                print(f"    Type Hints: {'✓' if analysis['has_type_hints'] else '❌'}")
                
                if not analysis['has_docstrings']:
                    all_issues.append(f"Missing docstrings in {file_name}")
                if not analysis['has_type_hints']:
                    all_issues.append(f"Missing type hints in {file_name}")
        
        if all_issues:
            print("\n🔍 Summary of Issues:")
            print("-" * 20)
            for issue in all_issues:
                print(f"• {issue}")
            
            print("\n📝 Next Steps:")
            print("-" * 20)
            print("1. Implement missing components")
            print("2. Add docstrings to all files")
            print("3. Add type hints for better code quality")
            print("4. Complete RAG pattern implementations")
        else:
            print("\n✓ All implementations complete and following best practices!")
            
        # Save the analysis report
        self.save_analysis_report(all_issues)

if __name__ == "__main__":
    analyzer = CompleteImplementationAnalyzer()
    analyzer.run()