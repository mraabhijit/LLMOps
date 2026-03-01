from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, MODELS


def get_gemini_llm(temperature: float = 0.5) -> ChatGoogleGenerativeAI:
    """Return a ChatGoogleGenerativeAI instance configured for gemini models."""
    return ChatGoogleGenerativeAI(
        model=MODELS.get("gemini", {}).get("model_name"),
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
    )