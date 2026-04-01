from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_classic.embeddings.cache import CacheBackedEmbeddings
from langchain_community.storage import RedisStore

from config import EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, REDIS_URL

store = RedisStore(redis_url=REDIS_URL)


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Return a configured Gemini embedding model."""
    underlying_embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
    )
    print(f"DEBUG: Using namespace: {underlying_embeddings.model}")
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=underlying_embeddings,
        document_embedding_cache=store,
        namespace=underlying_embeddings.model,
        query_embedding_cache=store,
    )
    return cached_embedder
