from typing import List
from pydantic import BaseModel

# Model for individual document (for retrieval and response generation)
class DocumentModel(BaseModel):
    id: int
    text: str

# Model for the request to retrieve documents (for /retrieve-documents)
class RetrievalRequest(BaseModel):
    query: str

# Model for the response to retrieve documents (for /retrieve-documents response)
class RetrievalResponse(BaseModel):
    documents: List[str]

# Model for the request to generate a response (for /generate-response)
class GenerateResponseRequest(BaseModel):
    query: str
    documents: List[DocumentModel]

# Model for the response from generating a response (for /generate-response)
class GenerateResponseResponse(BaseModel):
    response: str
