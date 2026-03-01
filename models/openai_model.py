from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, MODELS


def get_openai_llm(temperature: float = 0.5) -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for gpt models."""
    return ChatOpenAI(
        model=MODELS.get("openai", {}).get("model_name"),
        api_key=OPENAI_API_KEY,
        temperature=temperature,
    )
