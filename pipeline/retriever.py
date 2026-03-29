from pathlib import Path
from typing import Literal

from langchain_chroma.vectorstores import Chroma
from langchain_qdrant import QdrantVectorStore

from config import TOP_K, QDRANT_COLLECTION, QDRANT_URL, VECTOR_STORE
from pipeline.embeddings import get_embedding_model
from pipeline.ingest import get_recipe_chunks


def create_vector_store(persist_directory: Path | str = Path("chroma_db"), name: Literal["Chroma", "Qdrant"] = VECTOR_STORE) -> Chroma | QdrantVectorStore:
    """Ingest recipe chunks into a vector store and persist it."""
    recipe_chunks = get_recipe_chunks()
    embedding_model = get_embedding_model()
    if name == "Chroma":
        return Chroma.from_documents(
            documents=recipe_chunks,
            embedding=embedding_model,
            persist_directory=str(persist_directory),
        )
    return QdrantVectorStore.from_documents(
        documents=recipe_chunks,
        embedding=embedding_model,
        url=QDRANT_URL,
        collection_name=QDRANT_COLLECTION,
    )


def get_retriever(persist_directory: Path | str = Path("chroma_db"), name: Literal["Chroma", "Qdrant"] = VECTOR_STORE):
    """Load an existing vector store and return a retriever."""
    if name == "Chroma":
        vector_store = Chroma(
            persist_directory=str(persist_directory),
            embedding_function=get_embedding_model(),
        )
    else:
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=get_embedding_model(),
            url=QDRANT_URL,
            collection_name=QDRANT_COLLECTION,
        )
    return vector_store.as_retriever(
        search_kwargs={
            "k": TOP_K,
        }
    )


if __name__ == "__main__":
    _ = create_vector_store()
