from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import EMBEDDING_MODEL_NAME, GOOGLE_API_KEY


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Return a configured Gemini embedding model."""
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
    )
