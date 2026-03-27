# Recipe Finder — LLMOps Upgrade Targets & Fixes

This document provides a **direct action plan** to upgrade the Recipe Finder project with targets and concrete fixes.

---

## 1. Target: Scale from 10 to 10,000 concurrent users
**Proposed Fix:**  
- Move from local ChromaDB → distributed vector DB (Qdrant, Milvus).  
- Containerize API + inference with Docker + Kubernetes.  
- Add autoscaling for FastAPI + LLM inference nodes.  
- Implement request batching for LLM calls to reduce GPU overhead.  

---

## 2. Target: Reduce inference latency to <500ms per request
**Proposed Fix:**  
- Use vLLM or Triton Inference Server for GPU inference.  
- Stream output token-by-token instead of waiting for full response.  
- Cache embeddings for repeated ingredient queries.  
- Optimize prompt length and retrieval window size.  

---

## 3. Target: Reduce hallucinations / improve recipe relevance
**Proposed Fix:**  
- Enhance RAG retriever with hybrid search (semantic + BM25).  
- Add LLM evaluation loop (retry max 2 times if score < threshold).  
- Versioned prompts with A/B testing to select highest-quality prompt.  

---

## 4. Target: Handle large knowledge base (100k+ recipes)
**Proposed Fix:**  
- Chunk recipes semantically (max 200 tokens per chunk).  
- Precompute embeddings and store in distributed DB.  
- Implement vector DB indexing with efficient nearest-neighbor search.  
- Implement lazy loading / memory-mapped vectors to reduce memory footprint.  

---

## 5. Target: Track token usage and cost per request
**Proposed Fix:**  
- Extend Langfuse tracing to log:  
  - Tokens consumed per request  
  - Model used  
  - Approximate cost  
- Add Grafana dashboards + Prometheus metrics.  
- Log failed requests separately for debugging and monitoring.  

---

## 6. Target: Guardrails fail-proof for 11 languages
**Proposed Fix:**  
- Expand input normalization to all supported languages.  
- Add multilingual allergen detection (use synonym dictionaries).  
- Include edge-case tests (emoji, slang, non-standard spellings).  
- Add unit tests for guardrails in pipeline.  

---

## 7. Target: Multi-model orchestration with fallback
**Proposed Fix:**  
- Extend LLM factory to select primary → fallback model.  
- Log latency and cost per model per request.  
- Hot-swappable models via factory pattern, no downtime.  
- Add metrics to choose the cheapest / fastest model dynamically.  

---

## 8. Target: Versioned prompt management with measurable impact
**Proposed Fix:**  
- Implement prompt registry with active version + rollback.  
- Track evaluation metrics per prompt (faithfulness, hallucination, completeness).  
- Side-by-side comparison for A/B testing.  
- Include automated prompt updates in CI/CD pipeline.  

---

## 9. Target: Streaming support for all outputs
**Proposed Fix:**  
- Implement SSE streaming for all 11 languages.  
- Frontend: update JS to render partial responses incrementally.  
- Backend: yield LLM outputs token-by-token for low-latency streaming.  

---

## 10. Target: Evaluate pipeline at scale
**Proposed Fix:**  
- Add large dataset (Kaggle recipes or synthetic).  
- Run RAG evaluation with automated judge.  
- Track: recall, precision, completeness, hallucination, latency.  
- Log evaluation results and make dashboards to visualize metrics.  

---

## 11. Target: Monitoring and alerting
**Proposed Fix:**  
- Add Prometheus + Grafana for metrics.  
- Alerts for:
  - Failed requests  
  - Hallucination rate > threshold  
  - Latency spikes  
  - High token usage / cost  
- Set thresholds per model and per language.  

---

## 12. Target: Enable real-world feedback loop
**Proposed Fix:**  
- Add user rating for recipe suggestions.  
- Store ratings → adjust embedding ranking / prompt selection.  
- Optionally retrain embeddings periodically with feedback.  

---
