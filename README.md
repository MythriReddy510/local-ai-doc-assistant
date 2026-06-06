# 🤖 Local AI Document Assistant

A RAG-powered document Q&A system that lets you upload any PDF and ask questions about it using Llama 3 — running **100% locally** with no API keys or cloud costs.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.2 via Ollama (local) |
| RAG Pipeline | LangChain + ChromaDB |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| API | FastAPI + Pydantic |
| Containerization | Docker + Docker Compose |

---

## ✨ Features

- 📄 Upload any PDF and index it instantly
- 🧠 Ask natural language questions about the document
- 📍 Get answers with source page references
- 🔒 100% local — no data sent to any cloud
- 🐳 One command deployment with Docker

---

## 🏗️ Project Structure

```
local-ai-doc-assistant/
├── app/
│   ├── core/
│   │   ├── rag_pipeline.py   # RAG logic
│   │   └── embeddings.py     # HuggingFace embeddings
│   ├── api/
│   │   └── routes.py         # API endpoints
│   └── models/
│       └── schemas.py        # Pydantic models
├── data/uploads/             # Uploaded PDFs
├── main.py                   # FastAPI entry point
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ⚡ Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/download) with Llama 3.2 pulled

```bash
ollama pull llama3.2
```

### Run with Docker

```bash
git clone https://github.com/MythriReddy510/local-ai-doc-assistant.git
cd local-ai-doc-assistant
docker-compose up --build
```

Visit `http://localhost:8000/docs` to use the API.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check server status |
| POST | `/upload` | Upload a PDF file |
| POST | `/ask` | Ask a question |

### Example — Ask a question

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

### Response

```json
{
  "question": "What is this document about?",
  "answer": "The document is about...",
  "source_pages": [1, 3, 5]
}
```

---

## 🧠 How RAG Works

1. **Upload** — PDF is loaded and split into chunks
2. **Embed** — Each chunk is converted to vectors using HuggingFace
3. **Store** — Vectors saved in ChromaDB locally
4. **Retrieve** — Top 3 relevant chunks fetched for each question
5. **Answer** — Llama 3 answers using only those chunks

---

## 👨‍💻 Author

Built by **G R MYTHRI** as part of an AI Engineering portfolio project.