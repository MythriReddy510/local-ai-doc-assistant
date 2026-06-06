from pydantic import BaseModel
from typing import List

# ── Request Models ──────────────────────────────────────────

class QuestionRequest(BaseModel):
    """What the user sends when asking a question"""
    question: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "What is this document about?"
            }
        }
    }

# ── Response Models ─────────────────────────────────────────

class UploadResponse(BaseModel):
    """What the API returns after a PDF is uploaded"""
    message: str
    filename: str
    chunks_created: int

class AnswerResponse(BaseModel):
    """What the API returns after answering a question"""
    question: str
    answer: str
    source_pages: List

class HealthResponse(BaseModel):
    """What the API returns for health check"""
    status: str
    message: str