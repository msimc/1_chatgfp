"""
File: test_rag_system.py
Directory: scripts/test_rag_system.py
Created: 2024-11-03 16:45 UTC
Version: 1.0.0

Summary:
--------
Test script for verifying RAG system functionality and generating diagnostic reports.
Tests the complete pipeline from query processing to Pinecone retrieval and saves
detailed logs and diagnostics to files.

Purpose:
--------
- Test RAG system components independently and together
- Generate detailed diagnostic reports
- Verify Pinecone connection and retrieval
- Save test results and system status to files
- Create documentation of the current implementation state

Dependencies:
------------
- All RAG system components
- python-dotenv
- asyncio
- rich (for formatted console output)
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import json
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
import logging
from contextlib import contextmanager
import traceback

# Import RAG components
from chatgfp.steps.step_3_embedding.pinecone_client import PineconeClient
from chatgfp.steps.step_4_retrieval.query_processor import QueryProcessor
from chatgfp.core.services.rag_service import RAGService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

class RAGSystemTester:
    def __init__(self):
        """Initialize the RAG system tester"""
        load_dotenv()
        self.test_queries = [
            "What are the requirements for client money handling?",
            "Explain the SMCR requirements for core firms",
            "What are the key compliance requirements for financial advisers?",
            "How should firms handle customer complaints?",
            "What are the reporting requirements for regulated firms?"
        ]
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_diagnostic_file(self, filename: str, content: Any) -> Path:
        """Save diagnostic information to a file"""
        file_path = self.results_dir / f"{filename}_{self.timestamp}.txt"
        
        if isinstance(content, (dict, list)):
            content = json.dumps(content, indent=2)
        else:
            content = str(content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        console.print(f"[green]Saved diagnostic file:[/green] {file_path}")
        return file_path

    @contextmanager
    def test_section(self, name: str):
        """Context manager for test sections with timing"""
        console.print(f"\n[bold blue]Testing {name}...[/bold blue]")
        start_time = datetime.now()
        try:
            yield
            duration = (datetime.now() - start_time).total_seconds()
            console.print(f"[green]✓ {name} completed in {duration:.2f}s[/green]")
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            console.print(f"[red]✗ {name} failed in {duration:.2f}s[/red]")
            console.print(f"[red]Error: {str(e)}[/red]")
            traceback.print_exc()
            raise

    async def test_pinecone_connection(self) -> Dict:
        """Test Pinecone connection and basic functionality"""
        with self.test_section("Pinecone Connection"):
            client = PineconeClient()
            health_check = client.get_health_check()
            self.save_diagnostic_file("pinecone_health_check", health_check)
            return health_check

    async def test_query_processor(self) -> Dict:
        """Test query processing functionality"""
        with self.test_section("Query Processor"):
            processor = QueryProcessor()
            results = []
            
            for query in self.test_queries:
                try:
                    embedding = processor.generate_embedding(query)
                    results.append({
                        "query": query,
                        "embedding_shape": embedding.shape,
                        "embedding_norm": float(np.linalg.norm(embedding)),
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "query": query,
                        "error": str(e),
                        "status": "failed"
                    })
            
            self.save_diagnostic_file("query_processor_results", results)
            return {"total_queries": len(results), "results": results}

    async def test_rag_service(self) -> Dict:
        """Test complete RAG service functionality"""
        with self.test_section("RAG Service"):
            service = RAGService()
            results = []
            
            for query in self.test_queries:
                try:
                    response = await service.process_query(
                        query=query,
                        conversation_id=f"test_{self.timestamp}"
                    )
                    results.append({
                        "query": query,
                        "response_length": len(response.answer),
                        "num_references": len(response.references),
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "query": query,
                        "error": str(e),
                        "status": "failed"
                    })
            
            self.save_diagnostic_file("rag_service_results", results)
            return {"total_queries": len(results), "results": results}

    def generate_system_info(self) -> Dict:
        """Generate system information report"""
        info = {
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "python_version": sys.version,
                "platform": sys.platform,
                "env_vars_set": {
                    "PINECONE_API_KEY": bool(os.getenv("PINECONE_API_KEY")),
                    "PINECONE_ENVIRONMENT": bool(os.getenv("PINECONE_ENVIRONMENT")),
                    "PINECONE_INDEX_NAME": bool(os.getenv("PINECONE_INDEX_NAME")),
                    "PINECONE_REGION": bool(os.getenv("PINECONE_REGION"))
                }
            },
            "test_queries": self.test_queries
        }
        
        self.save_diagnostic_file("system_info", info)
        return info

    def generate_test_report(self, results: Dict) -> None:
        """Generate and save test report"""
        report = [
            "RAG System Test Report",
            "===================",
            f"\nTest Run: {self.timestamp}",
            "\nTest Results:",
            "-----------------"
        ]
        
        for component, result in results.items():
            report.append(f"\n{component}:")
            report.append("-" * (len(component) + 1))
            report.append(json.dumps(result, indent=2))
        
        self.save_diagnostic_file("test_report", "\n".join(report))

    async def run_all_tests(self):
        """Run all tests and generate reports"""
        console.print("[bold]Starting RAG System Tests[/bold]")
        
        try:
            # Generate system info
            system_info = self.generate_system_info()
            
            # Run all tests
            results = {
                "pinecone": await self.test_pinecone_connection(),
                "query_processor": await self.test_query_processor(),
                "rag_service": await self.test_rag_service()
            }
            
            # Generate final report
            self.generate_test_report(results)
            
            # Display summary table
            table = Table(title="Test Results Summary")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Details", style="yellow")
            
            for component, result in results.items():
                status = result.get("status", "Completed")
                details = str(result.get("total_queries", "Health check completed"))
                table.add_row(component, status, details)
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error during testing: {str(e)}[/red]")
            raise

"""
File Location and Purpose:
-------------------------
This file should be placed in:
scripts/test_rag_system.py

This script provides comprehensive testing and diagnostics for the RAG system,
saving detailed reports and logs for analysis.

Usage:
------
python -m scripts.test_rag_system

Test results and diagnostics will be saved in the test_results directory.

For questions or modifications, contact: [Your Contact Info]
"""

if __name__ == "__main__":
    tester = RAGSystemTester()
    asyncio.run(tester.run_all_tests())