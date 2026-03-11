# Recipe Finder — LLMOps Pipeline

A production-grade RAG (Retrieval-Augmented Generation) application that takes a user's available ingredients and generates curated recipe suggestions. Built with a full LLMOps stack: orchestration, observability, evaluation, prompt management, and guardrails. Supports voice input, multilingual responses (11 Indian languages), and a browser-based frontend with authentication.

## How It Works

```
User Input (text / voice / vernacular)
    |
    v
Sarvam STT -------- speech-to-text (WAV → transcript)  [voice path only]
    |
    v
Sarvam Translation - vernacular → English              [non-English path only]
    |
    v
Input Guardrail ---- jailbreak detection, normalization, allergen flagging
    |
    v
ChromaDB Retriever - vector search over recipe knowledge base
    |
    v
Retrieval Evaluator- quality check, retry loop (max 2 retries)
    |
    v
LLM Generator ------ prompt from versioned registry, structured recipe output
    |
    v
Output Guardrail --- allergen cross-check, unsafe food detection
    |
    v
Sarvam Translation - English → vernacular (streamed)   [non-English path only]
    |
    v
Response (CLI · REST API · Browser UI)
```

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Framework | LangChain | Unified LLM interface, LCEL chains |
| Orchestration | LangGraph | StateGraph with conditional edges and retry logic |
| Vector Store | ChromaDB | Local vector search over recipe embeddings |
| Embeddings | Gemini (`gemini-embedding-001`) | Text embedding for semantic search |
| LLM Providers | Gemini, OpenAI, Claude, Grok | Multi-model support via factory pattern |
| Observability | Langfuse | Distributed tracing across the pipeline |
| Evaluation | Ragas + LLM-as-a-Judge | Automated quality scoring on 5 criteria |
| Guardrails | NeMo Guardrails + custom rails | Allergen safety, jailbreak prevention |
| Prompt Management | Custom file-based registry | Versioned prompts with A/B testing support |
| Voice / STT | Sarvam AI (`saarika:v2.5`) | Speech-to-text for Indian languages |
| Translation | Sarvam AI (`mayura:v1`) | Bidirectional vernacular ↔ English translation |
| API | FastAPI | REST endpoints with JWT-style token auth |
| Auth | SQLite + Bearer tokens | User registration, login, token validation |
| Frontend | Vanilla HTML/CSS/JS | Browser UI with mic input, streaming, auth |

## Project Structure

```
llmops/
├── app.py                       # FastAPI server — mounts auth + recipe routers
├── main.py                      # CLI entry point
├── recipe_finder.py             # CLI logic (interactive, --text, --audio modes)
├── config.py                    # Central configuration (keys, models, language map)
├── database.py                  # SQLite init — users + tokens tables
│
├── routers/
│   ├── auth.py                  # POST /register, POST /login
│   └── recipe.py                # POST /recipe, /recipe/voice, /recipe/text
│
├── sarvam/
│   ├── __init__.py              # Re-exports stream helpers
│   ├── stt.py                   # Speech-to-text via Sarvam API
│   ├── translate.py             # Vernacular ↔ English translation (chunked + streamed)
│   └── interface.py             # High-level voice/text pipeline orchestration
│
├── frontend/
│   ├── index.html               # SPA shell — search bar, mic button, auth modal
│   ├── styles.css               # Dark-mode, glassmorphism UI
│   └── script.js                # API calls, SSE streaming, MediaRecorder mic capture
│
├── models/
│   ├── factory.py               # get_llm() factory function
│   ├── openai_model.py
│   ├── claude_model.py
│   ├── gemini_model.py
│   └── grok_model.py
│
├── pipeline/
│   ├── ingest.py                # Recipe JSON loading and chunking
│   ├── embeddings.py            # Gemini embedding model
│   ├── retriever.py             # ChromaDB vector search
│   └── generator.py             # RAG chain (LCEL), prompt loading
│
├── orchestration/
│   └── graph.py                 # LangGraph StateGraph (5 nodes, 2 routing functions)
│
├── guardrails/
│   ├── input_rails.py           # Jailbreak detection, normalization, allergen flagging
│   └── output_rails.py          # Allergen cross-check, unsafe food scan, refusal detection
│
├── prompts/
│   ├── registry.py              # PromptRegistry — version, rollback, compare
│   ├── register_prompts.py      # Seed script for manifest
│   ├── manifest.json            # Prompt version metadata
│   ├── rag_prompt_v1.txt
│   └── rag_prompt_v2.txt
│
├── evaluation/
│   ├── test_quality.py          # Offline eval with 5 test cases
│   └── judge.py                 # LLM-as-a-Judge scoring
│
├── tracing/
│   └── setup.py                 # Langfuse callback handler
│
├── audio/
│   └── test.wav                 # Sample audio for testing voice input
│
└── data/
    └── recipes.json             # 17 recipes across 6 cuisines
```

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Install

```bash
git clone <repo-url>
cd llmops
uv sync
```

### Environment Variables

Create a `.env` file in the project root:

```env
# LLM Providers
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key
XAI_API_KEY=your-key

# Sarvam AI (voice + translation)
SARVAM_API_KEY=your-key
SARVAM_BASE_URL=https://api.sarvam.ai

# Langfuse (observability)
LANGFUSE_SECRET_KEY=your-key
LANGFUSE_PUBLIC_KEY=your-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Initialize Vector Store

Run once to embed recipes into ChromaDB:

```bash
uv run python -m pipeline.retriever
```

### Register Prompts

Run once to seed the prompt manifest:

```bash
uv run python -m prompts.register_prompts
```

## Usage

### CLI

**Interactive mode** (English):

```bash
uv run python main.py
```

```
Welcome to Recipe Finder
=========================
Enter available ingredients, each ingredient in a new line.
You can also mention allergies (e.g., 'allergic to dairy').
Type 'quit' or 'exit' when done.

> chicken
> garlic
> lemon
> quit

Searching for recipes...

Recipe Name: Lemon Garlic Chicken with Sauteed Spinach
...
```

**Single-line text (with vernacular support)**:

```bash
uv run python main.py --text "আমার কাছে মাংস আছে, রসুন আছে" --language bengali
```

**Voice input (WAV file)**:

```bash
uv run python main.py --audio audio/test.wav --language hindi
```

### API

```bash
uv run uvicorn app:app --reload --port 8000
```

Interactive docs: `http://localhost:8000/docs`

**Register & Login:**

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'

curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'
# → {"access_token": "<token>", "token_type": "bearer"}
```

**Text recipe (English):**

```bash
curl -X POST http://localhost:8000/recipe \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"ingredients": "chicken, garlic, lemon", "allergies": ["dairy"]}'
```

**Vernacular text (streamed SSE):**

```bash
curl -X POST http://localhost:8000/recipe/text \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"ingredients": "मेरे पास चिकन और लहसुन है", "language": "hindi"}'
```

**Voice upload (streamed SSE):**

```bash
curl -X POST http://localhost:8000/recipe/voice \
  -H "Authorization: Bearer <token>" \
  -F "audio=@audio/test.wav" \
  -F "language=bengali"
```

### Frontend

Open `frontend/index.html` directly in a browser (make sure the API server is running on port 8000). Features:

- Register / Login with Bearer token auth
- Type ingredients or speak via microphone
- Select from 11 Indian languages
- Streamed recipe output rendered in real-time

### Run Evaluation

```bash
uv run python -m evaluation.test_quality
```

## LLMOps Layers

| Layer | What It Does |
|-------|-------------|
| **Orchestration** | LangGraph StateGraph with 5 nodes. Conditional routing retries poor retrievals up to 2 times before generating. |
| **Observability** | Langfuse tracing captures the full request lifecycle — latency, token usage, and intermediate outputs per step. |
| **Evaluation** | LLM-as-a-Judge scores responses on ingredient coverage, faithfulness, completeness, relevance, and safety. Offline test suite with edge cases. |
| **Prompt Management** | File-based registry with JSON manifest. Supports version listing, active version switching (rollback), and side-by-side comparison for A/B testing. |
| **Guardrails** | Input rails: jailbreak detection, gibberish filtering, ingredient normalization, allergen declaration parsing. Output rails: allergen cross-check with synonym expansion, known allergen scan, unsafe food pattern detection, refusal detection. |
| **Voice & Translation** | Sarvam AI integration: WAV audio → transcript (STT), plus bidirectional translation between English and 11 Indian languages. Responses are streamed paragraph-by-paragraph to reduce latency. |
| **Authentication** | SQLite-backed user store with hashed passwords (SHA-256) and random Bearer tokens. Soft-delete support for account deactivation without data loss. |

## Supported Languages

| Language | Code |
|----------|------|
| English | `english` |
| Bengali | `bengali` |
| Gujarati | `gujarati` |
| Hindi | `hindi` |
| Kannada | `kannada` |
| Malayalam | `malayalam` |
| Marathi | `marathi` |
| Odia | `odia` |
| Punjabi | `punjabi` |
| Tamil | `tamil` |
| Telugu | `telugu` |

## License

MIT
