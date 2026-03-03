from langfuse.langchain import CallbackHandler

# from config import LANGFUSE_BASE_URL, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY


def get_langfuse_handler():
    """Return a configured Langfuse callback handler for LangChain tracing."""
    return CallbackHandler()
