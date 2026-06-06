import sys
import os

# This makes sure Python can find the app/ folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.rag_pipeline import ingest_pdf, ask_question

print("=" * 50)
print("STEP 1: Testing PDF ingestion...")
print("=" * 50)

# 👇 Change this to your actual PDF path
PDF_PATH = "C:/Users/DELL/OneDrive/Documents/document.pdf"

chunks = ingest_pdf(PDF_PATH)
print(f"✅ Success! Created {chunks} chunks\n")

print("=" * 50)
print("STEP 2: Testing question answering...")
print("=" * 50)

result = ask_question("What is this document about?")

print(f"✅ Answer: {result['answer']}")
print(f"✅ Found on pages: {result['source_pages']}")