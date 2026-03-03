from pathlib import Path

from langchain_chroma.vectorstores import Chroma

from config import TOP_K
from pipeline import get_embedding_model, get_recipe_chunks


def create_vector_store(persist_directory: Path | str = Path("chroma_db")) -> Chroma:
    """Ingest recipe chunks into a ChromaDB vector store and persist it."""
    recipe_chunks = get_recipe_chunks()
    embedding_model = get_embedding_model()
    return Chroma.from_documents(
        documents=recipe_chunks,
        embedding=embedding_model,
        persist_directory=str(persist_directory),
    )


def get_retriever(persist_directory: Path | str = Path("chroma_db")):
    """Load an existing ChromaDB vector store and return a retriever."""
    vector_store = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=get_embedding_model(),
    )
    return vector_store.as_retriever(
        search_kwargs={
            "k": TOP_K,
        }
    )


if __name__ == "__main__":
    _ = create_vector_store()
    retriever = get_retriever()
    print(retriever.invoke("chicken garlic lemon"))
