from groq import Groq
from app.prompts.prompt import get_document_retrieval_prompt
from config.config_manager import ConfigurationManager
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()


class FinalResponse:
    def __init__(self):
        try:
            # Initialize Config Manager
            self.config_manager = ConfigurationManager()

            # Load Configs
            self.config_manager.load_config()
            self.api_key = self.config_manager.get("main", "key")
            self.model_response = self.config_manager.get("main", "model_response")
            if not self.api_key or not self.model_response:
                raise ValueError("API key or model_response is missing in configuration.")

            self.client = Groq(api_key=self.api_key)
            logger.info("Response service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise

    def answer_query(self, query, retrieved_documents):
        logger.info("Generating response...")
        try:
            # Handle different formats of retrieved_documents
            if hasattr(retrieved_documents, "documents") and isinstance(retrieved_documents.documents, list):
                document_text = "\n".join(retrieved_documents.documents)
            elif isinstance(retrieved_documents, list):
                document_text = "\n".join(retrieved_documents)
            else:
                logger.error("Unexpected retrieved_documents format.")
                raise TypeError("Invalid document format received")

            # Extract tuning parameters
            tuning_params = {}
            for key in self.config_manager.loaded_config.get("tuning", {}):
                value = self.config_manager.get("tuning", key).strip()  # Remove extra spaces

                if value.lower() in ["true", "false"]:  # Handle boolean values
                    tuning_params[key] = value.lower() == "true"
                else:
                    try:
                        if "." in value:  # Check if it's a float
                            tuning_params[key] = float(value)
                        else:  # Otherwise, assume it's an integer
                            tuning_params[key] = int(value)
                    except ValueError:
                        tuning_params[key] = value  # Keep as string if not a number


            if(not tuning_params):
                logger.error("No tuning parameters found in configuration.")
            
            logger.info(f"Using tuning parameters: {tuning_params}")

            chat_completion = self.client.chat.completions.create(
                messages=get_document_retrieval_prompt(document_text, query),
                model=self.model_response,
                **tuning_params  # Pass the extracted tuning parameters
            )
            logger.info(f"Prompt passed successfully in response service: {get_document_retrieval_prompt(document_text, query)}")

            # Extract response text
            response_text = chat_completion.choices[0].message.content.strip() if chat_completion.choices[0].message.content else "No valid response generated."

            # Prepare JSON response
            response_json = {
                "response": response_text
            }

            return response_json # Return JSON response containing HTML

        except Exception as e:
            logger.error(f"Error answering query: {e}")
            raise