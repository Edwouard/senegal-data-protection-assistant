from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union


class ChatRequest(BaseModel):
    """Requête de chat"""

    message: str = Field(..., description="Message de l'utilisateur")


class ChatResponse(BaseModel):
    """Réponse du chatbot"""

    response: str = Field(..., description="Réponse générée")
    sources: List[Dict[str, Union[str, float]]] = Field(
        default=[], description="Sources utilisées"
    )
