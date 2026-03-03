import os

from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_BASE_URL = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")

# Model configuration
MODELS = {
    "openai": {"model_name": "gpt-4o-mini", "provider": "openai"},
    "claude": {"model_name": "claude-3-haiku-20240307", "provider": "anthropic"},
    "gemini": {"model_name": "gemini-2.0-flash", "provider": "google"},
    "grok": {"model_name": "grok-2", "provider": "xai"},
}

DEFAULT_GENERATION_MODEL = "openai"
DEFAULT_EMBEDDING_MODEL = "gemini"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"

# ChromaDB
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval
TOP_K = 3

# Prompts
DEFAULT_PROMPT_VERSION = "v1"
PROMPTS_DIR = "./prompts"
