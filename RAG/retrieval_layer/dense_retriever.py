from typing import List
from fastapi import HTTPException
from langchain.schema import Document
from storage_layer.vector_store import VectorStore
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

class DenseRetriever:
    def __init__(self, vector_store: VectorStore):
        try:
            self.vector_store = vector_store
            self.cur = vector_store.cur
            if not self.cur:
                raise ValueError("Database cursor not available.")

            logger.info("Dense Retriever initialized")
        except Exception as e:
            logger.error(f"Dense Retriever initialization failed: {e}")
            raise HTTPException(status_code=500, detail="Service configuration error in dense retrieval.")

    def retrieve_dense_documents(self, query_embedding: List[float], top_k: int = 3, min_similarity: float = 0.6) -> List[Document]:
        try:
            self.cur.execute(
                """
                SELECT text, (1 - (embedding <=> %s::vector)) AS similarity
                FROM documents
                WHERE (1 - (embedding <=> %s::vector)) > %s
                ORDER BY similarity DESC
                LIMIT %s;
                """,
                (query_embedding, query_embedding, min_similarity, top_k * 2)  # Fetch extra results
            )

            results = []
            seen_chunks = set()

            for row in self.cur.fetchall():
                text, score = row
                if text not in seen_chunks:
                    results.append(Document(page_content=text))
                    seen_chunks.add(text)

            logger.info(f"Retrieved {len(results)} dense document chunks.")
            return results[:top_k]  # Return only top-K chunks after filtering

        except Exception as e:
            logger.error(f"Dense retrieval error: {e}")
            return []
