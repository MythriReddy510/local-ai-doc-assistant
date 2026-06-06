from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import (
    QuestionRequest,
    UploadResponse,
    AnswerResponse,
    HealthResponse
)
from app.core.rag_pipeline import ingest_pdf, ask_question
import os
import shutil

# Create a router — think of it as a mini app
# that holds all our routes
router = APIRouter()

# Folder where uploaded PDFs will be saved
UPLOAD_DIR = "./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Simple health check endpoint.
    Tells us the server is alive and running.
    """
    return HealthResponse(
        status="ok",
        message="Local AI Document Assistant is running!"
    )


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, saves it to disk,
    then runs it through the RAG ingestion pipeline.
    """

    # Step 1: Make sure it is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Step 2: Save the file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 3: Run the RAG ingestion pipeline
    try:
        chunks_created = ingest_pdf(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )

    return UploadResponse(
        message="PDF uploaded and indexed successfully!",
        filename=file.filename,
        chunks_created=chunks_created
    )


@router.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    """
    Accepts a question, searches ChromaDB for
    relevant chunks, and returns Llama 3's answer.
    """

    # Make sure question is not empty
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Run the RAG question answering pipeline
    try:
        result = ask_question(request.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {str(e)}"
        )

    return AnswerResponse(
        question=request.question,
        answer=result["answer"],
        source_pages=result["source_pages"]
    )