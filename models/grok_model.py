from langchain_openai import ChatOpenAI
from config import XAI_API_KEY, XAI_BASE_URL, MODELS


def get_grok_llm(temperature: float = 0.5) -> ChatOpenAI:
    """Return a ChatOpenAI instance pointing to xAI's Grok API."""
    return ChatOpenAI(
        model=MODELS.get("grok", {}).get("model_name"),
        api_key=XAI_API_KEY,
        base_url=XAI_BASE_URL,
        temperature=temperature,
    )
