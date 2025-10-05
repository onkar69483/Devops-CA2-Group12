import requests
import psycopg2
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form,Query, HTTPException

from psycopg2 import OperationalError, DatabaseError
from requests.exceptions import RequestException, ConnectionError as ReqConnectionError
from typing import List


from app.models.models import (
    RetrievalResponse,
    RetrievalRequest,
    GenerateResponseRequest,
    GenerateResponseResponse
)

from app.services.retrieve_docs_service import DocumentRetriever
from app.services.response_service import FinalResponse

from input_layer.query_processor import QueryProcessor

from config.config_manager import ConfigurationManager
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

# Initialize Configuration Manager
config_manager = ConfigurationManager()  # Create instance
config_manager.load_config()  # Load the config file

# Initialize Routers
query_router = APIRouter()
delete_db_router = APIRouter()
file_router = APIRouter()
scraper_router = APIRouter()
retrieval_router = APIRouter()
response_router = APIRouter()
dbstore_or_not_router = APIRouter()

@query_router.post(
    "/upload-query",
    summary="Upload query and return response.",
)
async def upload_query(query: str = Form(...)):
    try:
        logger.info("Received a query.")
        logger.debug(f"Query received: {query}")

        # Processing Query
        logger.info("Initialize QueryProcessor with the loaded config_manager")
        processor = QueryProcessor(query=query, config_manager=config_manager)

        logger.info("Process query")
        processed_query = processor.process_query()
        logger.info(f"Process Query: {processed_query}")

        # Retrieve Documents
        retrieval_request = RetrievalRequest(query=processed_query)
        retrieval_response = retrieve_documents_endpoint(retrieval_request)

        logger.info(f"Retrieved Documents: {retrieval_response}")
        logger.info(f"Retrieved Documents type: {type(retrieval_response)}")

        # Final Response
        retriever = FinalResponse()
        final_response = retriever.answer_query(processed_query, retrieval_response)  

        # Return the response with extracted keywords
        return {
            "response": final_response,
            "documents": retrieval_response.documents,
            "processed_query": processed_query,
        }

    except HTTPException as http_exc:
        # FastAPI's HTTPException will be returned directly with status codes
        return {"error": http_exc.detail}

    except Exception as e:
        # Catch any unexpected errors
        logger.critical(f"Unexpected error in Query processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during image processing.")


@delete_db_router.delete("/delete-database", summary="Delete all documents from OpenSearch and PostgreSQL.")
async def delete_all_documents():
    try:
        # ---------------- OpenSearch Deletion ----------------
        try:
            os_host = config_manager.get("opensearch", "host")
            os_port = config_manager.get("opensearch", "port")
            os_scheme = config_manager.get("opensearch", "scheme")
            os_index = config_manager.get("opensearch", "index")

            delete_url = f"{os_scheme}://{os_host}:{os_port}/{os_index}/_delete_by_query"
            logger.info(f"Sending DELETE request to OpenSearch: {delete_url}")

            os_response = requests.post(
                delete_url,
                headers={"Content-Type": "application/json"},
                json={"query": {"match_all": {}}}
            )

            if os_response.status_code != 200:
                logger.error(f"OpenSearch deletion failed: {os_response.text}")
                raise HTTPException(status_code=500, detail="Failed to delete documents from OpenSearch.")

            logger.info("Successfully deleted from OpenSearch.")
        except ReqConnectionError as conn_err:
            logger.critical(f"OpenSearch connection error: {str(conn_err)}", exc_info=True)
            raise HTTPException(status_code=502, detail="Failed to connect to OpenSearch.")
        except RequestException as req_err:
            logger.critical(f"OpenSearch request error: {str(req_err)}", exc_info=True)
            raise HTTPException(status_code=500, detail="OpenSearch request failed.")

        # ---------------- PostgreSQL Deletion ----------------
        try:
            pg_host = config_manager.get("pgvector", "host")
            pg_port = config_manager.get("pgvector", "port")
            pg_user = config_manager.get("pgvector", "user")
            pg_password = config_manager.get("pgvector", "password")
            pg_db = config_manager.get("pgvector", "database")

            conn = psycopg2.connect(
                host=pg_host,
                port=pg_port,
                user=pg_user,
                password=pg_password,
                dbname=pg_db,
            )
            cursor = conn.cursor()

            delete_query = "DELETE FROM documents WHERE id < 10000;"
            cursor.execute(delete_query)
            conn.commit()

            cursor.close()
            conn.close()

            logger.info("Successfully deleted from PostgreSQL.")
        except OperationalError as op_err:
            logger.critical(f"PostgreSQL connection error: {str(op_err)}", exc_info=True)
            raise HTTPException(status_code=502, detail="Failed to connect to PostgreSQL.")
        except DatabaseError as db_err:
            logger.critical(f"PostgreSQL query error: {str(db_err)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error executing PostgreSQL query.")
        except Exception as e:
            logger.critical(f"Unexpected PostgreSQL error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Unexpected error during PostgreSQL deletion.")

        return {"message": "All documents deleted from OpenSearch and PostgreSQL."}

    except HTTPException as http_exc:
        raise http_exc  # re-raise to keep status codes
    except Exception as e:
        logger.critical(f"Unhandled error in delete_all_documents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during deletion.")
    

@retrieval_router.post(
    "/retrieve-documents",
    response_model=RetrievalResponse,
    summary="Retrieve relevant documents based on query or list of queries. (Helper for Query Router)"
)
def retrieve_documents_endpoint(request: RetrievalRequest):
    try:
        # Log the incoming request
        logger.info(f"Received query: {request.query}")

        document_retriever = DocumentRetriever()
        retrieved_documents = set()

        # Retrieve documents for query
        if request.query:
            logger.debug(f"Retrieving documents for query: {request.query}")
            top_documents = document_retriever.retrieve_documents(query=request.query, top_n=3)
            logger.info(f"Retrieved {len(top_documents)} documents for query: {request.query}")
            retrieved_documents.update(doc.page_content for doc in top_documents)

        # Convert back to list for the response
        logger.info(f"Total unique documents retrieved: {len(retrieved_documents)}")
        return RetrievalResponse(documents=list(retrieved_documents))

    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error during document retrieval in router: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during document retrieval in router.")


@response_router.post("/generate-response", summary="Generate a response using retrieved documents and a query. (Helper for Query Router)")
async def generate_response_endpoint(request: GenerateResponseRequest):
    try:
        logger.info("Generating response for query and documents.")

        # Initialize the FinalResponse instance
        retriever = FinalResponse()

        # Generate the response
        response = retriever.answer_query(request.query, request.documents)

        logger.info("Generated response successfully.")
        return GenerateResponseResponse(response=response)

    except Exception as e:
        logger.error(f"Error in generating response: {str(e)}")
        return GenerateResponseResponse(response=f"Error generating response: {str(e)}")





# FOR PDF AND TXT
DOCUMENTS_DIR = "storage_layer"

# Ensure the directory exists
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

@file_router.get("/documents", response_model=List[str], summary="List all stored document filenames")
def list_documents():
    try:
        files = os.listdir(DOCUMENTS_DIR)
        return [f for f in files if f.lower().endswith(('.pdf', '.txt'))]
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list documents")


@file_router.post("/documents", summary="Upload a document (PDF or TXT)")
async def upload_document(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith((".pdf", ".txt")):
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are allowed")

        file_path = os.path.join(DOCUMENTS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Uploaded document: {file.filename}")
        return {"message": f"{file.filename} uploaded successfully"}
    except Exception as e:
        logger.error(f"Failed to upload document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error uploading document")


@file_router.delete("/documents/{filename}", summary="Delete a document by filename")
def delete_document(filename: str):
    try:
        file_path = os.path.join(DOCUMENTS_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document not found")

        os.remove(file_path)
        logger.info(f"Deleted document: {filename}")
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting document")
    


# FOR SCRAPER URLS
@scraper_router.get("/scraper-urls", response_model=List[str], summary="Get all scraper URLs")
def get_scraper_urls():
    try:
        config_manager.load_config()
        urls_str = config_manager.get("SCRAPER", "urls", "")
        urls = [url.strip() for url in urls_str.split(",") if url.strip()]
        return urls
    except Exception as e:
        logger.error(f"Failed to fetch URLs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error reading URLs from config")


@scraper_router.post("/scraper-urls", summary="Add a new URL to the config")
def add_scraper_url(url: str = Query(..., description="URL to add")):
    try:
        config_manager.load_config()
        urls_str = config_manager.get("SCRAPER", "urls", "")
        existing_urls = {u.strip() for u in urls_str.split(",") if u.strip()}

        if url in existing_urls:
            raise HTTPException(status_code=400, detail="URL already exists")

        existing_urls.add(url.strip())
        new_urls = ", ".join(sorted(existing_urls))
        config_manager.update_config_value("SCRAPER", "urls", new_urls)
        config_manager.save_config()
        return {"message": "URL added successfully", "urls": list(existing_urls)}

    except HTTPException as http_ex:
        # Re-raise HTTP errors as-is
        raise http_ex

    except Exception as e:
        logger.error(f"Failed to add URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Error adding URL to config")


@scraper_router.delete("/scraper-urls", summary="Remove a URL from the config")
def delete_scraper_url(url: str = Query(..., description="URL to remove")):
    try:
        config_manager.load_config()
        urls_str = config_manager.get("SCRAPER", "urls", "")
        logger.info(f"Loaded URLs from config: '{urls_str}'")

        # Normalize
        normalized_url = url.strip().rstrip("/")
        existing_urls = {u.strip().rstrip("/") for u in urls_str.split(",") if u.strip()}

        logger.info(f"Trying to delete: {normalized_url}")
        logger.info(f"Current URLs: {existing_urls}")

        if normalized_url not in existing_urls:
            raise HTTPException(status_code=404, detail="URL not found")

        existing_urls.remove(normalized_url)
        new_urls = ", ".join(sorted(existing_urls))

        config_manager.update_config_value("SCRAPER", "urls", new_urls)
        config_manager.save_config()

        return {"message": "URL removed successfully", "urls": sorted(list(existing_urls))}

    except Exception as e:
        logger.error(f"Failed to remove URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@dbstore_or_not_router.get("/config/database_opensearch_store")
def get_database_opensearch_store():
    try:
        value = config_manager.get("main", "database_opensearch_store", default="true")
        return {"database_opensearch_store": value.lower() == "true"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@dbstore_or_not_router.post("/config/database_opensearch_store/{value}")
def set_database_opensearch_store(value: bool):
    try:
        config_manager.update_config_value("main", "database_opensearch_store", str(value).lower())
        return {"message": f"database_opensearch_store set to {value}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))