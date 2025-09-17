from typing import List
from fastapi import HTTPException
from langchain.schema import Document
from retrieval_layer.hybrid_retriever import HybridRetriever

from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

class DocumentRetriever:
    def __init__(self):
        self.hybrid_retriever = HybridRetriever()

    def retrieve_documents(
        self, query: str, top_n: int = 3
    ) -> List[Document]:
        try:
            logger.info("Using Hybrid Retrieval method.")
            return self.hybrid_retriever.retrieve_documents(query, top_n)
        except Exception as e:
            logger.error(f"Error during document retrieval: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error during document retrieval: {str(e)}")
