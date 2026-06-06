from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Loads a free HuggingFace embedding model.
    This converts text into numbers (vectors) for ChromaDB storage.
    Model: all-MiniLM-L6-v2 — small, fast, and very accurate.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},   # runs on CPU, no GPU needed
        encode_kwargs={"normalize_embeddings": True}
    )
    return embeddings