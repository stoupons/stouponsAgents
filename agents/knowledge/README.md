# Agent #1: Knowledge Agent

**Difficulty:** 1/10 · **Model:** Claude Sonnet 5.5 (`core/config.py`) · **Status:** built, waiting on its first live eval run

## Job
Answer questions about Stoupons water softeners, RO systems, options and warranty, **using only approved documents** in `knowledge/`, with citations.

## Approved sources
| source_id | Document | Version | Original |
|---|---|---|---|
| `KB-WS-RO` | [Stoupons Water Softener & RO Systems Knowledge Base](../../knowledge/water_softener_ro_kb.md) | 1.0 | [PDF](../../knowledge/originals/Stoupons_Water_Softener_RO_Internal_Knowledge_Base.pdf) |

The KB's section 17 "AI / RAG Guardrails" is built into [prompts.py](prompts.py) as the agent's product rules. Only documents with `status: approved` are indexed (see [knowledge/README.md](../../knowledge/README.md)).

## Inputs → outputs
- **Input:** a customer question (plus earlier turns of the same chat)
- **Output:** `KnowledgeResult`, containing `answer`, `status`, `citations`, `transaction_id`, `cost_usd`

| Status | Meaning | What the Manager will do (later) |
|---|---|---|
| `ANSWERED` | Answered from cited documents | Show the answer |
| `UNKNOWN` | Documents don't cover it | Offer a human or create a ticket |
| `OUT_OF_SCOPE` | Price, scheduling, order or payment question | Route to the Pricing, Scheduling or Support agent |
| `BLOCKED` | The input guardrail stopped it | Show the safe reply |
| `ESCALATED` | The output guardrail rejected the answer | Show the safe fallback and review the trace |

## Tools
| Tool | What it does |
|---|---|
| `retrieve_knowledge(query)` | Semantic search over all approved docs |
| `search_faq(query)` | Semantic search over FAQ docs only |
| `get_document(source_id)` | Full text of one doc |

## Must never
- State a price, discount, appointment, availability, order or payment status
- Answer from general knowledge instead of the documents
- Cite a source it didn't retrieve
- Reveal its instructions (the canary `CANARY-KB-7731` must never appear)

## Files
| File | What it teaches |
|---|---|
| [ingest.py](ingest.py) | Chunking, embeddings, vector database (Chroma) |
| [tools.py](tools.py) | Retrieval with source_id, version and score; relevance threshold |
| [prompts.py](prompts.py) | System prompt design, grounding rules, canary |
| [agent.py](agent.py) | Tool Runner loop, guardrails, status parsing, tracing, cost |
| [chat.py](chat.py) | Talking to the agent in your terminal |
| [../../core/guardrails.py](../../core/guardrails.py) | Input and output guardrails (shared by all agents) |
| [../../tests/test_knowledge.py](../../tests/test_knowledge.py) | Unit tests with a fake Claude (free) |
| [../../evals/knowledge.yaml](../../evals/knowledge.yaml) | 38-case golden eval set based on the approved KB |

## How to run

```powershell
.\.venv\Scripts\Activate.ps1

# 1. Build the vector index (re-run after changing anything in knowledge/)
python -m agents.knowledge.ingest

# 2. Free tests, no API key needed
pytest

# 3. Chat with it (needs ANTHROPIC_API_KEY in .env)
python -m agents.knowledge.chat

# 4. Run the eval set (~$0.50-1.50)
python -m evals.run_knowledge_evals
```

Every question is logged to `logs/traces.jsonl`. Open the file to see exactly which tools ran, what they found, what it cost, and why an answer was escalated.

## Definition of done (from the roadmap)
- [x] Typed tool schemas (`strict: true`)
- [x] Automated tests (30 passing)
- [x] Input and output guardrails, including prompt-injection tests
- [x] Trace logging with cost
- [x] Clear escalation behavior (`UNKNOWN`, `OUT_OF_SCOPE`, `ESCALATED`)
- [ ] **Eval set ≥ 90% passing on a live run**
- [x] Sample documents replaced with the approved Stoupons KB (KB-WS-RO v1.0)

## Exercises (do these yourself, they're how you learn)
1. **Read a trace.** Ask a question in chat, then find its `transaction_id` in `logs/traces.jsonl`. Which chunks were retrieved, and what were their scores?
2. **Approve a document.** Pick a draft in `knowledge/drafts/`, correct it with real Stoupons facts, move it to `knowledge/`, set `status: approved`, run ingest, and ask about it.
3. **Tune the threshold.** Change `RELEVANCE_THRESHOLD` in `tools.py` to 0.2 and then 0.5, and re-run the evals. What breaks?
4. **Break it.** Find a question that makes it answer badly, add it to `evals/knowledge.yaml`, then fix the prompt until it passes.
5. **Compare models.** Set `WORKER_MODEL = "claude-haiku-5-5"` and re-run the evals. Is quality still fine at 1/20th the cost?
