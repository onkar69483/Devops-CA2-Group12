from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.configs.logging_config import setup_logger
from app.routers.routers import query_router,delete_db_router, file_router, scraper_router, retrieval_router, response_router, dbstore_or_not_router

# Configure logger
logger = setup_logger()

class RAGFrameworkChatbot:

    def __init__(self):
        logger.info("Initializing the RAG Framework Chatbot application.")
        self.app = FastAPI(title="RAG Framework Chatbot", version="1.0.0")
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://52.206.61.91"],  # your frontend dev origin
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add health check route
        @self.app.get("/", summary="Health check")
        def health_check():
            logger.debug("Health check requested.")
            return {"status": "ok", "message": "RAG Framework Chatbot is running"}

        self._include_routers()
        logger.info("RAG Framework Chatbot application initialization complete.")

    def _include_routers(self):
        logger.info("Including routers into the FastAPI application.")
        try:
            self.app.include_router(query_router, prefix="/query", tags=["Query Route"])
            logger.info("Query router included successfully.")
            self.app.include_router(delete_db_router, prefix="/delete_db", tags=["Delete DB, Opensearch Route"])
            logger.info("Delete DB router included successfully.")
            self.app.include_router(file_router, prefix="/pdf_txt", tags=["PDF,TXT Docs Route"])
            logger.info("PDF and txt router included successfully.")
            self.app.include_router(scraper_router, prefix="/scraper", tags=["Scraper Route"])
            logger.info("Scarper router included successfully.")
            self.app.include_router(dbstore_or_not_router, prefix="/dbstore_or_no", tags=["DBStore or Not Route"])
            logger.info("DBStore or not router included successfully.")
            self.app.include_router(retrieval_router, prefix="/retrieval", tags=["Retrieval Route (Helper)"])
            logger.info("Retrieval router included successfully.")
            self.app.include_router(response_router, prefix="/response", tags=["Response Route (Helper)"])
            logger.info("Response router included successfully.")
 
        except Exception as e:
            logger.error(f"Error including routers: {str(e)}", exc_info=True)
            raise

    def get_app(self):
        logger.info("Retrieving the FastAPI application instance.")
        return self.app

# Initialize the RAG Framework Chatbot
try:
    logger.info("Starting RAG Framework Chatbot initialization.")
    rag_framework = RAGFrameworkChatbot()
    app = rag_framework.get_app()
    logger.info("RAG Framework Chatbot initialized and app instance retrieved.")
except Exception as e:
    logger.critical(f"Critical failure during chatbot initialization: {str(e)}", exc_info=True)
    raise
