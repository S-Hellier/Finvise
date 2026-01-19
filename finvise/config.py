"""
Configuration management for Finvise.
Handles environment variables and application settings.
"""

import os
from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class Config:
    """
    Application configuration loaded from environment variables.
    
    Currently only supports local (Ollama) provider.
    """
    
    ollama_base_url: str = "http://localhost:11434"  # Local for Ollama
    
    # Vector Database Configuration
    vector_db_path: str = "./data/vector_db"
    
    # Embedding Configuration
    embedding_model: str = "nomic-embed-text"  # Test a few embedding versions once functionality is working
    
    # LLM Configuration
    llm_model: str = "llama3.2" 
    
    # Chunking Configuration
    # Using characters right, may want to consider semantic, token
    chunk_size: int = 1000  # Characters per chunk
    chunk_overlap: int = 200  # Overlap between chunks for context preservation
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            vector_db_path=os.getenv("VECTOR_DB_PATH", "./data/vector_db"),
            embedding_model=os.getenv(
                "EMBEDDING_MODEL",
                "nomic-embed-text"
            ),
            llm_model=os.getenv(
                "LLM_MODEL",
                "llama3.2"
            ),
            chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200")),
        )
