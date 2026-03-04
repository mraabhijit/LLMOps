# Recipe Finder -- LLMOps Pipeline

A production-grade RAG (Retrieval-Augmented Generation) application that takes a user's available ingredients and generates curated recipe suggestions. Built with a full LLMOps stack: orchestration, observability, evaluation, prompt management, and guardrails.

## How It Works

```
User Input (ingredients)
    |
    v
Input Guardrail ---- jailbreak detection, ingredient validation, allergen flagging
    |
    v
ChromaDB Retriever -- vector search over recipe knowledge base
    |
    v
Retrieval Evaluator - quality check, retry loop (max 2 retries)
    |
    v
LLM Generator ------- prompt from versioned registry, structured recipe output
    |
    v
Output Guardrail ---- allergen cross-check, unsafe food detection
    |
    v
Response (CLI or JSON API)
```

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Framework | LangChain | Unified LLM interface, LCEL chains |
| Orchestration | LangGraph | StateGraph with conditional edges and retry logic |
| Vector Store | ChromaDB | Local vector search over recipe embeddings |
| Embeddings | Gemini (gemini-embedding-001) | Text embedding for semantic search |
| LLM Providers | Gemini, OpenAI, Claude, Grok | Multi-model support via factory pattern |
| Observability | Langfuse | Distributed tracing across the pipeline |
| Evaluation | Ragas + LLM-as-a-Judge | Automated quality scoring on 5 criteria |
| Guardrails | Custom input/output rails | Allergen safety, jailbreak prevention |
| Prompt Management | Custom registry | Versioned prompts with A/B testing support |
| API | FastAPI | REST endpoint for the recipe finder |

## Project Structure

```
llmops/
├── app.py                       # FastAPI server (POST /recipe)
├── main.py                      # CLI entry point
├── recipe_finder.py             # CLI logic (collect, run, display)
├── config.py                    # Central configuration
├── models/
│   ├── factory.py               # get_llm() factory function
│   ├── openai_model.py
│   ├── claude_model.py
│   ├── gemini_model.py
│   └── grok_model.py
├── pipeline/
│   ├── ingest.py                # Recipe JSON loading and chunking
│   ├── embeddings.py            # Gemini embedding model
│   ├── retriever.py             # ChromaDB vector search
│   └── generator.py             # RAG chain (LCEL), prompt loading
├── orchestration/
│   └── graph.py                 # LangGraph StateGraph (5 nodes, 2 routing functions)
├── guardrails/
│   ├── input_rails.py           # Jailbreak detection, normalization, allergen flagging
│   └── output_rails.py          # Allergen cross-check, unsafe food scan, refusal detection
├── prompts/
│   ├── registry.py              # PromptRegistry class (version, rollback, compare)
│   ├── register_prompts.py      # Seed script for manifest
│   ├── manifest.json            # Prompt version metadata
│   ├── rag_prompt_v1.txt
│   └── rag_prompt_v2.txt
├── evaluation/
│   ├── test_quality.py          # Offline eval with 5 test cases
│   └── judge.py                 # LLM-as-a-Judge scoring
├── tracing/
│   └── setup.py                 # Langfuse callback handler
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

```
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key
XAI_API_KEY=your-key

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

### API

```bash
uv run uvicorn app:app --reload --port 8000
```

```bash
curl -X POST http://localhost:8000/recipe \
  -H "Content-Type: application/json" \
  -d '{"ingredients": "chicken, garlic, lemon", "allergies": ["dairy"]}'
```

Interactive docs available at `http://localhost:8000/docs`.

### Run Evaluation

```bash
uv run python -m evaluation.test_quality
```

## LLMOps Layers

| Layer | What It Does |
|-------|-------------|
| **Orchestration** | LangGraph StateGraph with 5 nodes. Conditional routing retries poor retrievals up to 2 times before generating. |
| **Observability** | Langfuse tracing captures the full request lifecycle -- latency, token usage, and intermediate outputs per step. |
| **Evaluation** | LLM-as-a-Judge scores responses on ingredient coverage, faithfulness, completeness, relevance, and safety. Offline test suite with edge cases. |
| **Prompt Management** | File-based registry with JSON manifest. Supports version listing, active version switching (rollback), and side-by-side comparison for A/B testing. |
| **Guardrails** | Input rails: jailbreak detection, gibberish filtering, ingredient normalization, allergen declaration parsing. Output rails: allergen cross-check with synonym expansion, known allergen scan, unsafe food pattern detection, refusal detection. |

## License

MIT
