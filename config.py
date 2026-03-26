import os

from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_BASE_URL = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_BASE_URL = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai")

# Model configuration
MODELS = {
    "openai": {"model_name": "gpt-4o-mini", "provider": "openai"},
    "claude": {"model_name": "claude-3-5-sonnet-latest", "provider": "anthropic"},
    "gemini": {"model_name": "gemini-2.5-flash-lite", "provider": "google"},
    "grok": {"model_name": "grok-4", "provider": "xai"},
    "sarvam-audio": {"model_name": "saarika:v2.5", "provider": "sarvam"},
    "sarvam-translate": {"model_name": "mayura:v1", "provider": "sarvam"},
}

DEFAULT_GENERATION_MODEL = "gemini"
DEFAULT_EMBEDDING_MODEL = "gemini"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"
DEFAULT_AUDIO_MODEL = "sarvam-audio"
DEFAULT_TRANSLATION_MODEL = "sarvam-translate"

# ChromaDB
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval
TOP_K = 3

# Prompts
DEFAULT_PROMPT_VERSION = "v1"
PROMPTS_DIR = "./prompts"
PROMPT_REGISTRY_NAME = "recipe-generator"

# Langfuse
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

# Language Codes
LANGUAGE_MAP = {
    "bengali": "bn-IN",
    "english": "en-IN",
    "gujarati": "gu-IN",
    "hindi": "hi-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
    "marathi": "mr-IN",
    "odia": "od-IN",
    "punjabi": "pa-IN",
    "tamil": "ta-IN",
    "telugu": "te-IN",
}

# Sarvam
SARVAM_CHUNK_SIZE = 900

# QDRANT
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "recipes")
VECTOR_STORE = os.getenv("VECTOR_STORE", "Qdrant")
