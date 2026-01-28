from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    grade_level: str
    subject: str
    session_id: str
