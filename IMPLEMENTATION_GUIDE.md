# LLMOps Project — Recipe Finder

## 🎯 Project Overview

Build a **RAG-powered Recipe Finder** that takes a user's available ingredients and generates curated dish recipes. Built with **LangChain** and **4 free-tier LLM providers**.

### How It Works

```
User Input:  "I have chicken, garlic, lemon, olive oil, and spinach"
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Embed query │────▶│  Retrieve    │────▶│  Generate recipe │
│  (Gemini)    │     │  matching    │     │  (OpenAI)        │
│              │     │  recipes     │     │                  │
└─────────────┘     │  (ChromaDB)  │     │  With steps,     │
                    └──────────────┘     │  tips, and       │
                                        │  substitutions   │
                                        └─────────────────┘
```

### LLM Providers

| Provider | Model (Free Tier) | LangChain Package | Role |
|----------|-------------------|-------------------|------|
| **OpenAI** | `gpt-4o-mini` | `langchain-openai` | Primary recipe generation |
| **Claude** | `claude-3-haiku` | `langchain-anthropic` | Evaluator / LLM-as-a-Judge |
| **Gemini** | `gemini-2.0-flash` | `langchain-google-genai` | Embeddings + fallback generation |
| **Grok** | `grok-2` | `langchain-openai` (OpenAI-compatible) | Guardrails / alternative generation |

> **Note:** Grok uses the OpenAI-compatible API — we reuse `langchain-openai` with `base_url=https://api.x.ai/v1`.

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| **Framework** | LangChain | Industry standard, unified `.invoke()` interface |
| **Orchestration** | LangGraph | Agentic workflows — retry bad retrievals, tool calling |
| **Vector Store** | ChromaDB | Local, zero-config |
| **Observability** | Langfuse | Open-source tracing |
| **Evaluation** | Ragas | Automated quality scoring |
| **Guardrails** | NeMo Guardrails | Allergen warnings, dietary safety |
| **API Server** | FastAPI + Uvicorn | REST API for the recipe finder |
| **Secrets** | `.env` + python-dotenv | Local development |

---

## 📁 Project Structure

```
llmops/
├── IMPLEMENTATION_GUIDE.md      # This file
├── pyproject.toml               # Dependencies (uv)
├── .env                         # API keys (never commit!)
├── .gitignore
├── config.py                    # Central configuration
├── models/
│   ├── __init__.py
│   ├── factory.py               # Model factory — get_llm("openai")
│   ├── openai_model.py          # ChatOpenAI wrapper
│   ├── claude_model.py          # ChatAnthropic wrapper
│   ├── gemini_model.py          # ChatGoogleGenerativeAI wrapper
│   └── grok_model.py            # ChatOpenAI wrapper (xAI base_url)
├── pipeline/
│   ├── __init__.py
│   ├── ingest.py                # Load & chunk recipes from JSON
│   ├── embeddings.py            # Embed recipes using Gemini
│   ├── retriever.py             # ChromaDB vector search by ingredients
│   └── generator.py             # RAG chain — generate recipes via LCEL
├── orchestration/
│   ├── __init__.py
│   └── graph.py                 # LangGraph workflow with decision loops
├── evaluation/
│   ├── __init__.py
│   ├── test_quality.py          # Offline eval — score recipe quality
│   └── judge.py                 # LLM-as-a-Judge using Claude
├── guardrails/
│   ├── __init__.py
│   ├── input_rail.py            # Validate ingredients, block jailbreaks
│   └── output_rail.py           # Allergen warnings, dietary checks
├── tracing/
│   ├── __init__.py
│   └── setup.py                 # Langfuse tracing setup
├── prompts/
│   ├── rag_prompt_v1.txt        # Recipe generation prompt v1
│   └── rag_prompt_v2.txt        # Iterated prompt v2
├── data/
│   └── recipes.json             # Recipe knowledge base
├── recipe_finder.py             # CLI entry point (Phase 1)
└── app.py                       # FastAPI server (Phase 2)
```

---

## 🗄️ Data Format: `data/recipes.json`

Each recipe is a structured object. During ingestion, we convert each recipe to a text chunk for embedding.

```json
[
  {
    "id": "001",
    "name": "Lemon Garlic Chicken with Sautéed Spinach",
    "cuisine": "Mediterranean",
    "dietary": ["gluten-free", "high-protein"],
    "allergens": [],
    "prep_time_mins": 10,
    "cook_time_mins": 20,
    "servings": 2,
    "difficulty": "easy",
    "ingredients": [
      {"item": "chicken breast", "quantity": "2", "unit": "pieces"},
      {"item": "garlic", "quantity": "4", "unit": "cloves"},
      {"item": "olive oil", "quantity": "2", "unit": "tbsp"},
      {"item": "lemon", "quantity": "1", "unit": "whole"},
      {"item": "spinach", "quantity": "2", "unit": "cups"}
    ],
    "instructions": [
      "Season chicken with salt, pepper, and lemon zest.",
      "Heat olive oil in a skillet over medium-high heat.",
      "Sear chicken 6 mins per side until golden and cooked through.",
      "Add minced garlic, cook 1 min until fragrant.",
      "Squeeze lemon juice over chicken, add spinach, wilt for 2 mins."
    ],
    "tips": "Add red pepper flakes for a spicy kick."
  },
  {
    "id": "002",
    "name": "Classic Tomato Basil Pasta",
    "cuisine": "Italian",
    "dietary": ["vegetarian"],
    "allergens": ["gluten"],
    "prep_time_mins": 5,
    "cook_time_mins": 15,
    "servings": 2,
    "difficulty": "easy",
    "ingredients": [
      {"item": "pasta", "quantity": "200", "unit": "grams"},
      {"item": "tomato", "quantity": "4", "unit": "whole"},
      {"item": "garlic", "quantity": "3", "unit": "cloves"},
      {"item": "basil", "quantity": "10", "unit": "leaves"},
      {"item": "olive oil", "quantity": "2", "unit": "tbsp"},
      {"item": "parmesan", "quantity": "50", "unit": "grams"}
    ],
    "instructions": [
      "Cook pasta according to package instructions.",
      "Dice tomatoes. Heat olive oil, sauté garlic for 1 min.",
      "Add tomatoes, cook 8 mins until softened into a sauce.",
      "Toss drained pasta with sauce, top with torn basil and parmesan."
    ],
    "tips": "Use San Marzano tomatoes for the best flavor."
  }
]
```

> Start with 15–20 recipes covering diverse cuisines and dietary categories for a solid demo.

---

## 🚀 Implementation Steps

### Phase 1: Mini RAG Pipeline (Steps 1–5)

| Step | What to Build | Key Files | Key Concepts |
|------|---------------|-----------|--------------|
| **1** | Project setup, deps, `.env`, config | `pyproject.toml`, `.env`, `config.py` | Environment management |
| **2** | LangChain model wrappers + factory | `models/factory.py`, `models/*_model.py` | `BaseChatModel`, `.invoke()`, `.stream()` |
| **3** | Recipe ingestion & chunking | `pipeline/ingest.py` | JSON parsing, `RecursiveCharacterTextSplitter`, recipe-to-text |
| **4** | Embeddings + ChromaDB vector store | `pipeline/embeddings.py`, `pipeline/retriever.py` | `GoogleGenerativeAIEmbeddings`, `Chroma`, ingredient-based search |
| **5** | RAG recipe chain + CLI | `pipeline/generator.py`, `recipe_finder.py` | LCEL chains, `RunnablePassthrough`, recipe prompts |

### Phase 2: LLMOps Layers (Steps 6–10)

| Step | What to Build | Key Files | Key Concepts |
|------|---------------|-----------|--------------|
| **6** | Observability — Langfuse tracing | `tracing/setup.py` | Traces, spans, LangChain callbacks |
| **7** | Evaluation — Ragas + LLM-as-a-Judge | `evaluation/test_quality.py`, `evaluation/judge.py` | Recipe quality scoring (see below) |
| **8** | Prompt management — versioned registry | `prompts/`, `config.py` | Prompt versioning, A/B testing |
| **9** | Guardrails — input/output rails | `guardrails/input_rail.py`, `guardrails/output_rail.py` | Allergen detection, dietary checks |
| **10** | Advanced orchestration — LangGraph | `orchestration/graph.py`, `app.py` | StateGraph, conditional edges, retry logic |

---

## 📝 Recipe-Specific Prompt (v1)

```
prompts/rag_prompt_v1.txt
```

```text
You are a professional chef assistant. The user will provide a list of ingredients
they have available. Based on the recipe context provided below, suggest the best
matching recipe and present it in a clear, appetizing format.

Rules:
- ONLY suggest recipes that can be made with the user's available ingredients
- Clearly mark if any additional ingredients are needed (distinguish "nice to have"
  from "essential")
- Include preparation steps, cooking time, and serving size
- Suggest ingredient substitutions when possible
- Add a chef's tip at the end
- If no recipe matches well, say so honestly — do not invent recipes

Context (retrieved recipes):
{context}

User's available ingredients:
{question}

Your recipe suggestion:
```

---

## 📊 Recipe-Specific Evaluation Criteria (Step 7)

| Metric | What It Measures | Example |
|--------|-----------------|---------|
| **Ingredient Coverage** | Does the recipe use the user's listed ingredients? | User has 5 items → recipe uses 4 ✅ |
| **Faithfulness** | Is the recipe grounded in the knowledge base? | Recipe exists in `recipes.json`? ✅ |
| **Completeness** | Does the output include steps, time, servings? | Missing cook time ❌ |
| **Relevance** | Does the recipe match the ingredient list? | User has fish → suggests beef ❌ |
| **Safety** | Are allergen warnings included when needed? | Recipe has nuts → warns nut allergy ✅ |

---

## 🛡️ Recipe-Specific Guardrails (Step 9)

### Input Rails
- Validate that input looks like an ingredient list (not a jailbreak attempt)
- Normalize ingredient names ("chicken breast" = "chicken breasts")
- Flag potential allergens in the input for user awareness

### Output Rails
- Scan generated recipe for common allergens (nuts, gluten, dairy, shellfish)
- Add allergen warning banner if detected
- Ensure recipe doesn't include unsafe food combinations
- Verify cooking temperatures/times are reasonable

---

## 🔁 LangGraph Workflow (Step 10)

```
                    ┌─────────────┐
                    │  User Input │
                    │ (ingredients)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Retrieve  │
                    │   recipes   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Good match?│
                    └──┬───────┬──┘
                   Yes │       │ No
                       │  ┌────▼─────────┐
                       │  │ Rewrite query│
                       │  │ (broaden     │
                       │  │  ingredient  │
                       │  │  matching)   │
                       │  └────┬─────────┘
                       │       │ retry (max 2)
                       │  ┌────▼─────┐
                       │  │ Retrieve │
                       │  │ again    │
                       │  └────┬─────┘
                       │       │
                    ┌──▼───────▼──┐
                    │  Generate   │
                    │  recipe     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Guardrails │
                    │  (allergens)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Output    │
                    └─────────────┘
```

---

## ✅ Step 1 Checklist

- [x] Folder structure created
- [x] `pyproject.toml` with all dependencies
- [x] `.venv` created and deps installed (via `uv`)
- [x] `.git` initialized
- [x] `.gitignore` — add `.env` and `chroma_db/`
- [x] `.env` — add API key placeholders
- [x] `config.py` — add configuration code
- [ ] `data/recipes.json` — add 15-20 sample recipes
- [ ] `prompts/rag_prompt_v1.txt` — add recipe generation prompt

Once Step 1 is complete → **Step 2: Build the LangChain model wrappers**.

---

## 📚 Resume-Ready Skills

> **LangChain** · **LangGraph** · **RAG Pipelines** · **ChromaDB** · **Prompt Engineering** · **LLM Evaluation (Ragas)** · **Observability (Langfuse)** · **Guardrails** · **LLMOps** · **Multi-Model Orchestration**
