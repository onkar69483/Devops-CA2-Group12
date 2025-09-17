from typing import List
import psycopg2
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
from storage_layer.document_database import DocumentDatabase
from config.config_manager import ConfigurationManager
from app.configs.logging_config import setup_logger

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

# PostgreSQL Configuration
PG_CONFIG = {
    "dbname": config_manager.get("pgvector", "database", "testdb"),
    "user": config_manager.get("pgvector", "user", "postgres"),
    "password": config_manager.get("pgvector", "password", "admin"),
    "host": config_manager.get("pgvector", "host", "localhost"),
    "port": config_manager.get("pgvector", "port", 5432),
}

# OpenSearch Configuration
try:
    OS_CLIENT = OpenSearch(
        hosts=[{"host": config_manager.get("opensearch", "host", "localhost"), "port": config_manager.get("opensearch", "port", 9200)}],
        http_auth=(config_manager.get("opensearch", "user", "admin"))
    )
    OS_INDEX = config_manager.get("opensearch", "index", "test_index")

except Exception as e:
    logger.error(f"Error initializing OpenSearch: {e}")


# Create OpenSearch index with custom analyzer
def opensearch_index_create():
    try:
        # Delete old index and recreate with improved settings
        if OS_CLIENT.indices.exists(OS_INDEX):
            OS_CLIENT.indices.delete(index=OS_INDEX)
        OS_CLIENT.indices.create(
            index=OS_INDEX,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "analysis": {
                        "analyzer": {
                            "custom_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": ["lowercase", "english_stemmer"]
                            }
                        },
                        "filter": {
                            "english_stemmer": {
                                "type": "stemmer",
                                "language": "english"
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "text": {
                            "type": "text",
                            "analyzer": "custom_analyzer",
                            "fields": {
                                "keyword": {
                                    "type": "keyword"
                                }
                            }
                        }
                    }
                }
            }
        )
        logger.info(f"Created OpenSearch index: {OS_INDEX}")
    except Exception as e:
        logger.error(f"Error initializing OpenSearch: {e}")


class VectorStore:
    def __init__(self):
        self.conn = self._get_pg_connection()
        self.cur = self.conn.cursor() if self.conn else None
        self.OS_CLIENT = OS_CLIENT
        logger.info("VectorStore initialized.")

    def initialize_opensearch_database(self):
        try:
            database_opensearch_store = config_manager.get("main", "database_opensearch_store", "true")
            logger.info(f"Database and Opensearch Store: {database_opensearch_store}")
        except Exception as e:
            logger.error(f"Failed to load config in vectorDB: {e}")

        if(database_opensearch_store == "true"):
            if self.conn:
                logger.info("Storing in Database and OpenSearch store.")
                opensearch_index_create()
                self._initialize_database()
                self.store_documents_with_embeddings()

    def _get_pg_connection(self):
        try:
            conn = psycopg2.connect(**PG_CONFIG)
            logger.info("Connected to PostgreSQL.")
            return conn
        except psycopg2.Error as err:
            logger.error(f"Error connecting to PostgreSQL: {err}")
            return None

    def _initialize_database(self):
        if not self.conn:
            return
        try:
            with self.conn.cursor() as cur:
                logger.info("Initializing PostgreSQL database...")
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Drop the table if it exists before recreating it
                cur.execute("DROP TABLE IF EXISTS documents CASCADE;")
                
                # Create the table again
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id SERIAL PRIMARY KEY,
                        text TEXT,
                        embedding vector(384)
                    );
                """)
                
                # Recreate the index
                cur.execute("CREATE INDEX IF NOT EXISTS embedding_idx ON documents USING ivfflat (embedding vector_l2_ops);")
                
                self.conn.commit()
            logger.info("PostgreSQL database initialized and all previous data deleted.")
        except psycopg2.Error as err:
            logger.error(f"Error initializing database: {err}")
            self.conn.rollback()

    def _generate_embedding(self, text: str) -> List[float]:
        try:
            return embedding_model.encode(text).tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return []

    def _store_embedding_in_db(self, text: str, embedding: List[float]):
        if not self.conn:
            logger.error("Database connection unavailable.")
            return
        try:
            # Store in PostgreSQL
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM documents WHERE text = %s", (text,))
                if cur.fetchone():
                    logger.info(f"Document already exists: {text[:30]}...")
                    return
                
                # Fetch the last stored ID
                cur.execute("SELECT MAX(id) FROM documents")
                last_id = cur.fetchone()[0]
                next_id = (last_id + 1) if last_id is not None else 1  # Start from 1 if table is empty

                # Insert the new document
                cur.execute("INSERT INTO documents (id, text, embedding) VALUES (%s, %s, %s)", 
                        (next_id, text, embedding))
                self.conn.commit()
                logger.info(f"Stored document in PostgreSQL: {text[:30]}...")

            # Store in OpenSearch
            OS_CLIENT.index(index=OS_INDEX, body={"text": text})
            logger.info(f"Inserted into OpenSearch: {text[:30]}...")

        except psycopg2.Error as err:
            logger.error(f"Error storing document: {err}")
            self.conn.rollback()

    def _chunk_text(self, text: str, chunk_size, chunk_overlap) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            chunk = text[start : start + chunk_size]
            chunks.append(chunk)
            start += chunk_size - chunk_overlap  # Move with overlap
        return chunks

    def store_documents_with_embeddings(self):
        try:
            document_database = DocumentDatabase()
            documents = document_database.get_all_documents()
            
            for doc in documents:
                text = doc.page_content.strip()
                if not text:
                    logger.warning("Skipping empty document.")
                    continue
                
                chunk_size = int(config_manager.get("chunking", "chunk_size", "300"))
                chunk_overlap= int(config_manager.get("chunking", "chunk_overlap", "30"))
                chunks = self._chunk_text(text,chunk_size,chunk_overlap)
                for chunk in chunks:
                    logger.info(f"Processing chunk: {chunk[:30]}...")
                    embedding = self._generate_embedding(chunk)
                    if embedding:
                        self._store_embedding_in_db(chunk, embedding)
                    else:
                        logger.warning(f"Skipping chunk due to missing embedding: {chunk[:30]}...")
        
        except Exception as e:
            logger.error(f"Error in storing chunked documents with embeddings: {e}")

    def get_documents_and_embeddings(self):
        if not self.conn:
            return [], []
        documents, embeddings = [], []
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT text, embedding FROM documents")
                rows = cur.fetchall()
                for text, embedding_vec in rows:
                    documents.append(text)
                    embeddings.append(embedding_vec)
                logger.info("Retrieved documents and embeddings from DB.")
        except psycopg2.Error as err:
            logger.error(f"Error retrieving embeddings: {err}")
        return documents, embeddings

    def get_cursor(self):
        return self.cur

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed.")
