from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from config import DEFAULT_GENERATION_MODEL, DEFAULT_PROMPT_VERSION, PROMPTS_DIR
from models import get_llm
from pipeline.retriever import get_retriever


def load_prompt(version: str = DEFAULT_PROMPT_VERSION) -> ChatPromptTemplate:
    """Load a prompt template from the prompts directory."""
    prompt_path = Path(PROMPTS_DIR) / f"rag_prompt_{version}.txt"
    try:
        with open(prompt_path, "r") as f:
            template = f.read()

        return ChatPromptTemplate.from_template(
            template=template,
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(e)


def create_rag_chain(provider: str = DEFAULT_GENERATION_MODEL):
    """Build and return the full RAG chain using LCEL."""
    retriever = get_retriever()
    runnable = {"context": retriever | format_docs, "question": RunnablePassthrough()}
    prompt = load_prompt()
    llm = get_llm(provider=provider)
    chain = runnable | prompt | llm | StrOutputParser()
    return chain


def format_docs(docs: list[Document]) -> str:
    """Formats the PageContent attribute of list of Document object into a plain string."""
    return "\n\n".join(doc.page_content for doc in docs)
