import os
import fitz 
from typing import List
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from config.config_manager import ConfigurationManager
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

# Initialize Configuration Manager
config_manager = ConfigurationManager()
config_manager.load_config()

class DocumentDatabase:
    def __init__(self):
        self.documents: List[Document] = []
        self.directory_path = os.path.dirname(os.path.abspath(__file__)) 

        logger.info(f"Searching for files in: {self.directory_path}")

        # Load URLs and HTML tags from config.ini
        self.urls = config_manager.get("SCRAPER", "urls", "").split(",")  # Get URLs as a list
        self.html_tags = config_manager.get("SCRAPER", "html_tags", "p,div,span,li,h1,h2,h3,h4,h5,h6").split(",")

        if not self.urls or self.urls == [""]:
            logger.error("No URLs and HTML tags found in configuration.")
        else:
            logger.info(f"Initializing document database with URLs: {self.urls} and HTML tags: {self.html_tags}")
     
        logger.info("Document database initialized.")

    # FOR PDF AND TXT FILES
    def extract_text_from_file(self, file_path: str) -> str:
        try:
            if file_path.lower().endswith(".pdf"):
                doc = fitz.open(file_path)
                text = "\n".join(page.get_text("text") for page in doc)
            elif file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                return ""

            logger.info(f"Extracted text from {file_path}: {text[:200]}...")  # Log first 200 chars
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return ""
        
    # FOR URLS
    def scrape_text_from_url(self, url: str) -> str:
        """Scrape text content from a given webpage, capturing more elements and removing duplicates."""
        try:
            logger.info(f"Fetching URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            elements = soup.find_all(self.html_tags)
            unique_texts = set(element.get_text(strip=True) for element in elements if element.get_text(strip=True))
            text = "\n".join(unique_texts)
            
            logger.info(f"Successfully scraped {len(text)} characters from {url}")
            return text
        except requests.RequestException as e:
            logger.error(f"Failed to scrape text from {url}: {e}")
            return ""
            
    def save_scraped_data(self, filename="scraped_data.txt"):
        """Save scraped data to a text file with clear separation between links."""
        if not self.documents:
            logger.warning("No documents to save.")
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                for idx, doc in enumerate(self.documents):
                    file.write(f"URL: {self.urls[idx]}\n")
                    file.write("=" * 80 + "\n")
                    file.write(doc.page_content + "\n\n")
                    file.write("-" * 80 + "\n\n")
            logger.info(f"Scraped data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data to file: {e}")

    def load_documents_from_links(self):
        """Scrape text from URLs and store them as whole documents."""
        if not self.urls:
            logger.error("No URLs provided.")
            return

        for url in self.urls:
            text = self.scrape_text_from_url(url)
            if text:
                self.documents.append(Document(page_content=text))

        logger.info(f"Loaded {len(self.documents)} documents.")
        self.save_scraped_data()

    def load_documents_from_files(self):
        if not os.path.exists(self.directory_path):
            logger.error(f"Directory does not exist: {self.directory_path}")
            return

        files = [f for f in os.listdir(self.directory_path) if f.lower().endswith((".pdf", ".txt"))]
        logger.info(f"Found {len(files)} files: {files}")

        for filename in files:
            file_path = os.path.join(self.directory_path, filename)
            text = self.extract_text_from_file(file_path)

            if text:
                self.documents.append(Document(page_content=text))

        logger.info(f"Loaded {len(self.documents)} documents.")
        logger.info(f"Loaded document {self.documents}")

    def get_all_documents(self) -> List[Document]:
        if not self.documents:  # If documents haven't been loaded yet, load them
            self.load_documents_from_files()
            self.load_documents_from_links()

        logger.info(f"Retrieved {len(self.documents)} documents.")
        logger.info(f"Retrieved document {self.documents}")
        return self.documents