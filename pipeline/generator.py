
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from config import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_PROMPT_VERSION,
    PROMPT_REGISTRY_NAME,
)
from models import get_llm
from pipeline.retriever import get_retriever
from prompts import PromptRegistry


def load_prompt(version: str | None = None) -> ChatPromptTemplate:
    """Load a prompt template from the prompts directory."""
    registry = PromptRegistry()
    return registry.get_prompt(
        name=PROMPT_REGISTRY_NAME,
        version=version if version else DEFAULT_PROMPT_VERSION,
    )


def create_rag_chain(
    provider: str = DEFAULT_GENERATION_MODEL, prompt_version: str | None = None
):
    """Build and return the full RAG chain using LCEL."""
    retriever = get_retriever()
    runnable = {"context": retriever | format_docs, "question": RunnablePassthrough()}
    prompt = load_prompt(prompt_version)
    llm = get_llm(provider=provider)
    chain = runnable | prompt | llm | StrOutputParser()
    return chain


def format_docs(docs: list[Document]) -> str:
    """Formats the PageContent attribute of list of Document object into a plain string."""
    return "\n\n".join(doc.page_content for doc in docs)
