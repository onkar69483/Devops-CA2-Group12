from typing import List, Optional, Type
from fastapi import HTTPException
from langchain.schema import Document
from storage_layer.vector_store import VectorStore
from config.config_manager import ConfigurationManager
from app.configs.logging_config import setup_logger


# Configure logger
logger = setup_logger()

# Initialize Configuration Manager
config_manager = ConfigurationManager()  # Create instance
config_manager.load_config()  # Load the config file

INDEX_NAME = config_manager.get("opensearch", "index", "test_index")


class SparseRetriever:
    def __init__(self, model_class: Optional[Type] = None):
        self.vector_store = VectorStore()  # Connects to database
        self.client = self.vector_store.OS_CLIENT  # Access client from VectorStore
        self.documents = []

        logger.info("Sparse Retriever initialized.")

    def retrieve_sparse_documents(self, query: str, top_k: int = 3, min_score: float = 0.5) -> List[Document]:
        try:
            response = self.client.search(
                index=INDEX_NAME,
                body={
                    "query": {
                        "bool": {
                            "should": [
                                {"match_phrase": {"text": query}},  # Exact match boost
                                {"match": {
                                    "text": {
                                        "query": query,
                                        "minimum_should_match": "20%",  
                                        "boost": 0.7
                                    }
                                }}
                            ]
                        }
                    },
                    "size": top_k * 2  # Fetch more chunks to improve result merging
                }
            )

            results = []
            seen_chunks = set()  # Track retrieved chunks

            for hit in response["hits"]["hits"]:
                text = hit["_source"]["text"]
                score = hit["_score"]

                if score >= min_score and text not in seen_chunks:
                    results.append(Document(page_content=text))
                    seen_chunks.add(text)

            logger.info(f"Retrieved {len(results)} relevant sparse document chunks.")
            return results[:top_k]  # Return top K chunks

        except Exception as e:
            logger.error(f"Sparse retrieval error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Sparse retrieval failed: {str(e)}"
            )
