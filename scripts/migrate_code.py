"""
File: migrate_code.py
Location: ./scripts/migrate_code.py
Created: 2024-11-03
Purpose: Move existing code to new structure
"""

import shutil
from pathlib import Path
import re

def migrate_code():
    # Define source and destination mappings
    migrations = {
        # Step 1: Data Ingestion
        "pdf_processing/pdf_extractor.py": "src/chatgfp/steps/step_1_data_ingestion/text_extractor.py",
        
        # Step 2: Preprocessing
        "app/services/text_processor.py": "src/chatgfp/steps/step_2_preprocessing/text_cleaner.py",
        
        # Step 3: Embedding
        "app/services/embeddings.py": "src/chatgfp/steps/step_3_embedding/embeddings_generator.py",
        "app/services/vector_store.py": "src/chatgfp/steps/step_3_embedding/vector_store.py",
        
        # Step 4: Retrieval
        "app/services/retriever.py": "src/chatgfp/steps/step_4_retrieval/semantic_search.py",
        
        # Step 5: Categorization
        "src/fca_categorization/models.py": "src/chatgfp/steps/step_5_categorization/fca_analyzer.py",
        
        # Core components
        "auth/auth.py": "src/chatgfp/core/security.py",
        "database/database.py": "src/chatgfp/core/database/database.py",
        
        # Models
        "app/models/document.py": "src/chatgfp/models/document.py",
        "app/models/embedding.py": "src/chatgfp/models/embedding.py",
        
        # Tests
        "fca_queries/test_api.py": "src/chatgfp/tests/step_1/test_api.py",
        "fca_queries/test_business_logic.py": "src/chatgfp/tests/step_5/test_business_logic.py",
        
        # Utils
        "postgres/postgres_monitor.py": "src/chatgfp/utils/monitoring.py",
        "postgres/postgres_health.py": "src/chatgfp/utils/health_check.py"
    }

    print("Starting code migration...")
    
    for source, dest in migrations.items():
        source_path = Path(source)
        dest_path = Path(dest)
        
        if source_path.exists():
            print(f"Moving {source} to {dest}")
            
            # Create destination directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read and update imports in the file
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update imports
            content = re.sub(r'from app\.', 'from src.chatgfp.', content)
            content = re.sub(r'from auth\.', 'from src.chatgfp.core.', content)
            content = re.sub(r'from database\.', 'from src.chatgfp.core.database.', content)
            
            # Write to new location
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Successfully moved and updated {source}")
        else:
            print(f"Warning: Source file {source} not found")

if __name__ == "__main__":
    migrate_code()

"""
Save this file as: migrate_code.py
Location: ./scripts/migrate_code.py
"""