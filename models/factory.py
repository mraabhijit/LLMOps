from langchain_core.language_models.chat_models import BaseChatModel
from models.openai_model import get_openai_llm
from models.claude_model import get_claude_llm
from models.gemini_model import get_gemini_llm
from models.grok_model import get_grok_llm


_MODEL_REGISTRY = {
    "openai": get_openai_llm,
    "claude": get_claude_llm,
    "gemini": get_gemini_llm,
    "grok": get_grok_llm,
}


def get_llm(provider: str = "openai", temperature: float = 0.7) -> BaseChatModel:
    """
    Factory function to get a configured LLM by provider name.

    Usage:
        llm = get_llm("openai")
        llm = get_llm("gemini", temperature=0.3)
    """
    if provider not in _MODEL_REGISTRY:
        raise ValueError(
            f"Unknown provider '{provider}'. "
            f"Available: {list(_MODEL_REGISTRY.keys())}"
        )
    
    return _MODEL_REGISTRY[provider](temperature=temperature)
