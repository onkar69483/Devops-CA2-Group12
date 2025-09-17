from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from retrieval_layer.sparse_retriever import SparseRetriever
from retrieval_layer.dense_retriever import DenseRetriever
from app.configs.logging_config import setup_logger
from config.config_manager import ConfigurationManager
from storage_layer.vector_store import VectorStore

# Configure logger
logger = setup_logger()


# Initialize Configuration Manager
config_manager = ConfigurationManager()
config_manager.load_config()

# Load Sentence Transformer Model
try:
    embedding_model_name = config_manager.get("main", "model_embedding", "sentence-transformers/all-MiniLM-L6-v2")
    logger.info(f"Loading embedding model: {embedding_model_name}")
    embedding_model = SentenceTransformer(embedding_model_name)
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    exit(1)

class HybridRetriever:
    def __init__(self):
        self.sparse_retriever = SparseRetriever()
        self.vector_store = VectorStore()
        self.vector_store.initialize_opensearch_database()
        self.dense_retriever = DenseRetriever(self.vector_store)
        logger.info("Hybrid Retriever initialized")

    def retrieve_documents(self, query: str, top_k: int = 3) -> List[Document]:
        logger.info(f"Running hybrid search for: '{query}'")

        # Encode the query once
        query_embedding = embedding_model.encode(query).tolist()

        retrieval_tasks = {
            "sparse": lambda: self.sparse_retriever.retrieve_sparse_documents(query, top_k * 2),
            "dense": lambda: self.dense_retriever.retrieve_dense_documents(query_embedding, top_k * 2)
        }

        results = []
        with ThreadPoolExecutor() as executor:
            future_to_type = {executor.submit(task): task_type for task_type, task in retrieval_tasks.items()}

            for future in as_completed(future_to_type):
                try:
                    result = future.result()
                    if result:
                        results.extend(result)
                except Exception as e:
                    logger.error(f"Error in {future_to_type[future]} retrieval: {e}")

        if not results:
            return []

        # Deduplication and score tracking
        unique_results = {}
        logger.info(f"Combining {len(results)} results from sparse and dense retrieval.")
        for doc in results:
            text = doc.page_content  # Extract content from Document object
            score = doc.metadata.get("score", 0.0)  # Extract score from metadata
            if text not in unique_results or score > unique_results[text]["score"]:
                unique_results[text] = {"document": doc, "score": score}

        # Convert to list and normalize scores
        results = list(unique_results.values())
        scores = [doc["score"] for doc in results]
        min_score, max_score = min(scores), max(scores)
        score_range = max_score - min_score if max_score != min_score else 1.0

        for doc in results:
            doc["normalized_score"] = (doc["score"] - min_score) / score_range + 1e-6  # Small offset

        # Convert to list of `Document` objects and sort by normalized score
        retrieved_documents = [
            Document(
                page_content=doc["document"].page_content,
                metadata={"score": doc["normalized_score"]}
            )
            for doc in sorted(results, key=lambda x: x["normalized_score"], reverse=True)[:top_k]
        ]
        logger.info("Hybrid retrieval complete.")
        return retrieved_documents
