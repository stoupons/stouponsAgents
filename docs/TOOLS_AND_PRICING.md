# Tools, Alternatives & Prices

> These are approximate list prices as of October 2026. Vendors change pricing often, so check each pricing page when you sign up. Claude prices come from Anthropic's published price table.

## 1. LLMs (the "brain")

| Model | Input / output per 1M tokens | Best use in Stoupons |
|---|---|---|
| **Claude Haiku 5.5** (`claude-haiku-5-5`) | $0.10 / $0.50 (prompts ≤100K tokens) | Intent routing, guardrail classifiers, data extraction |
| **Claude Sonnet 5.5** (`claude-sonnet-5-5`) | $2 / $10 | Most worker agents |
| **Claude Opus 5.5** (`claude-opus-5-5`) | $4 / $20 | Manager Agent, Risk Review, complex reasoning |

**What one customer conversation costs** (about 20K tokens in and 2K out):

| Model | Cost per conversation | 1,000 conversations |
|---|---|---|
| Haiku 5.5 | ~$0.003 | ~$3 |
| Sonnet 5.5 | ~$0.06 | ~$60 |
| Opus 5.5 | ~$0.12 | ~$120 |

**Ways to spend less**
- **Prompt caching:** a stable system prompt and tool list are re-read at a large discount.
- **Batch API:** about 50% off for work that doesn't need an instant answer, like nightly marketing drafts or analytics.
- **The right model per job:** Haiku for routing and classification, bigger models only where quality matters. Measure with your evals before you downgrade.
- **Set a monthly spend limit** in the Anthropic Console on day one.

**Alternatives:** OpenAI (GPT models), Google Gemini (has a free tier), Mistral. You can also run free local models (Llama, Qwen) on your own computer with **Ollama**. They cost $0, but quality and tool use are weaker.

## 2. Core stack

| Need | Recommended (free) | Paid / alternatives |
|---|---|---|
| Language | **Python 3.12** | — |
| Editor | **VS Code** + Claude Code | Cursor (~$20/mo) |
| Code hosting | **GitHub** (free) | GitLab, Bitbucket |
| Agent loop | **Anthropic Python SDK** (Tool Runner) | LangGraph, OpenAI Agents SDK, CrewAI, PydanticAI (all free OSS) |
| Data models / validation | **Pydantic** | — |
| Database | **SQLite** (built into Python) → **Supabase Postgres** (free tier ~500MB) | Supabase Pro ~$25/mo, Neon (free tier), AWS RDS |
| Vector DB for RAG | **Chroma** (local, free) → **pgvector** inside Supabase | Pinecone (free starter; paid from ~$50/mo), Qdrant Cloud (free ~1GB), Weaviate |
| Embeddings | **sentence-transformers** (local, free) or **Voyage AI** (free starter tokens) | OpenAI `text-embedding-3-small` (~$0.02 / 1M tokens), Cohere |
| API server | **FastAPI** | Flask |
| Chat UI + Admin Dashboard | **Streamlit** (free; Community Cloud hosting free) | Next.js on Vercel (free hobby), Retool (free ≤5 users), Gradio |
| Tracing / observability | **Langfuse** (free hobby cloud or self-host) or **Arize Phoenix** (free OSS) | LangSmith (free dev tier; ~$39/seat/mo), Helicone, Datadog |
| Evals | **pytest** + **promptfoo** (free OSS) | Braintrust (free tier), LangSmith evals |
| Guardrails | **Your own Python rules + Haiku classifier** | Guardrails AI, NVIDIA NeMo Guardrails, Llama Guard (free OSS); Lakera (paid) |
| Scheduling / calendar | **Google Calendar API** (free) or **Cal.com** (free plan / self-host) | Calendly (~$10–16/seat/mo), Acuity |
| Payments | **Stripe test mode** (free) | Live: ~2.9% + 30¢ per card charge in the US; **Stripe Connect** for dealer payouts (extra fees) |
| SMS / WhatsApp | **Twilio** (trial credit) | SMS ~$0.008/msg in the US, plus number rental (~$1–2/mo); WhatsApp is priced per conversation by Meta |
| Email | **Resend** (free ~3,000/mo) | Postmark, SendGrid (~$15–20/mo) |
| Background jobs / cron | **APScheduler** or **GitHub Actions cron** (free) | n8n (self-host free; cloud ~€20/mo), Temporal, Celery |
| No-code glue (optional) | **n8n** self-hosted | Zapier (~$20+/mo), Make (~$9+/mo) |
| Hosting | **Render** / **Railway** (free or ~$5/mo hobby) | Fly.io, AWS, GCP, Azure |
| Secrets | **`.env` + python-dotenv** locally; host's env vars in prod | Doppler, AWS Secrets Manager |

## 3. Fine-tuning (much later, optional)

| Option | Cost | Notes |
|---|---|---|
| **Unsloth on Google Colab** (small open model such as Llama or Qwen) | Free (Colab free GPU) / Colab Pro ~$10/mo | Good for an intent classifier trained on your own logged data |
| OpenAI fine-tuning | Pay per training token + higher inference price | Easy managed option |
| Claude fine-tuning | Check current availability on Amazon Bedrock | Availability varies by model and region |

Use fine-tuning **only** after your traces show the same error repeating. Prompts, tools, RAG and evals come first. See [MANAGER_DESIGN.md](MANAGER_DESIGN.md#fine-tuning-policy).

## 4. Free learning resources

| Topic | Resource |
|---|---|
| Python from zero | **CS50P** (Harvard, free on edX/YouTube) |
| Git | GitHub Skills (free interactive courses) |
| Claude API, tool use, RAG | Anthropic docs + Anthropic courses on GitHub (free) |
| Agents, RAG, evals | DeepLearning.AI short courses (free) |
| SQL | SQLBolt, Mode SQL tutorial (free) |
| FastAPI | Official FastAPI tutorial (free) |

## 5. Budget summary

| Stage | Monthly cost |
|---|---|
| Learning (Phases 0–3) | **$0–25**, almost all of it Claude API usage |
| Pilot with real customers | **~$50–150**: Claude + Supabase + hosting + Twilio |
| Growing | Scales with conversations; at ~$0.06 per Sonnet conversation, 5,000 chats ≈ $300 |
| Per-transaction costs | Stripe ~2.9% + 30¢; SMS ~$0.008/msg |
