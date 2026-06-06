from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.embeddings import get_embedding_model
import os

# ChromaDB will save data in this folder
CHROMA_DB_PATH = "./chroma_db"


def ingest_pdf(file_path: str) -> int:
    """
    Reads a PDF, splits it into chunks, embeds them,
    and stores everything in ChromaDB.
    Returns the number of chunks created.
    """

    # Step 1: Load the PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Step 2: Split into small chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # Step 3: Get embedding model
    embeddings = get_embedding_model()

    # Step 4: Store chunks in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )

    print(f"✅ Ingested {len(chunks)} chunks into ChromaDB")
    return len(chunks)


def ask_question(question: str) -> dict:
    """
    Takes a user question, retrieves relevant chunks from ChromaDB,
    and asks Llama 3 to answer using only those chunks.
    Returns the answer and source pages.
    """

    # Step 1: Load embedding model + connect to ChromaDB
    embeddings = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    # Step 2: Create retriever — fetches top 3 relevant chunks
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    # Step 3: Load Llama 3 via Ollama
    llm = OllamaLLM(model="llama3.2", temperature=0.1)

    # Step 4: Custom prompt
    prompt_template = PromptTemplate.from_template("""
You are a helpful assistant. Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't have enough information in the document to answer this."

Context:
{context}

Question: {question}

Answer:
""")

    # Step 5: Build the chain using modern LCEL syntax
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )

    # Step 6: Run the chain
    answer = chain.invoke(question)

    # Step 7: Get source pages separately
    source_docs = retriever.invoke(question)
    sources = []
    for doc in source_docs:
        page = doc.metadata.get("page", "unknown")
        if page not in sources:
            sources.append(page)

    return {
        "answer": answer,
        "source_pages": sources
    }