from fastapi import FastAPI
from app.api.routes import router

# Create the FastAPI app
app = FastAPI(
    title="Local AI Document Assistant",
    description="Upload a PDF and ask questions about it using Llama 3 — 100% local, no API keys needed.",
    version="1.0.0"
)

# Connect all routes from routes.py
app.include_router(router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Local AI Document Assistant!",
        "docs": "Visit /docs to see all API endpoints",
        "health": "Visit /health to check server status"
    }