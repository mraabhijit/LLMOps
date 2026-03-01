from langchain_anthropic import ChatAnthropic
from config import ANTHROPIC_API_KEY, MODELS


def get_claude_llm(temperature: float = 0.5) -> ChatAnthropic:
    """Return a ChatAnthropic instance configured to Claude models."""
    return ChatAnthropic(
        model=MODELS.get("claude", {}).get("model_name"),
        api_key=ANTHROPIC_API_KEY,
        temperature=temperature,
    )
