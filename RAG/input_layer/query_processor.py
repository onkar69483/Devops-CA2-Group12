import re
import groq
from app.prompts.prompt import get_spelling_correction_prompt
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

class QueryProcessor:
    def __init__(self, query, config_manager):
        self.query = query
        self.config_manager = config_manager

        # Retrieve the API key from the configuration manager
        self.api_key = self.config_manager.get("main", "key")
        if not self.api_key:
            logger.error("API Key is missing in the configuration. Cannot initialize Groq client.")
            raise ValueError("API Key is required for initializing Groq client.")

        # Retrieve the model from the configuration manager
        self.model = self.config_manager.get("main", "model_query", "deepseek-r1-distill-llama-70b")
        if not self.model:
            logger.warning("Model is missing in the configuration. Using a default model.")

        # Initialize Groq client using the API key from the configuration
        self.client = groq.Client(api_key=self.api_key)  # Initialize Groq client

        logger.info(f"QueryProcessor initialized with model: {self.model} and API key.")

    def _clean_query(self):
        try:
            logger.info("Cleaning the query.")
            query = self.query.lower().strip()

            # Remove special characters
            query = self._remove_special_characters(query)

            # Correct spelling
            query = self._correct_spelling_with_groq(query)

            # Remove extra spaces
            query = " ".join(query.split())

            logger.debug(f"Cleaned query: {query}")
            return query
        except Exception as e:
            logger.error(f"Error cleaning query: {str(e)}")
            return self.query  # Return original query on failure

    def _remove_special_characters(self, query):
        try:
            logger.info("Removing special characters from the query.")
            cleaned_query = re.sub(r"[^a-zA-Z0-9\s]", "", query)  # Keep only alphanumeric and spaces
            return cleaned_query
        except Exception as e:
            logger.error(f"Error removing special characters: {str(e)}")
            return query

    def _correct_spelling_with_groq(self, query):
        try:
            logger.info("Correcting spelling with Groq.")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=get_spelling_correction_prompt(query),
                temperature=0.2
            )
            # Extract the corrected query from the response
            corrected_query = response.choices[0].message.content.strip()

            # Remove unwanted `<think>` section if present
            corrected_query = re.sub(r"<think>.*?</think>", "", corrected_query, flags=re.DOTALL).strip()

            # Ensure output starts with "Processed Query: "
            return f"{corrected_query}"

        except Exception as e:
            logger.error(f"Error correcting spelling with Groq: {str(e)}")
            return f"{query}"  # Return original query if an error occurs

    def process_query(self):
        return self._clean_query()
