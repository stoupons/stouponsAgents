# Roadmap: Beginner to FDE, while Automating Stoupons

**Assumptions:** no prior coding experience and about 10–15 hours per week. That puts the full system at **about 9–12 months**. Going faster is fine, but never skip an exit checklist.

> Rule from the Stoupons skill: *Do not move to the next phase just because the previous agent works in a demo.*

## Overview

| Phase | Weeks | Build | Learn |
|---|---|---|---|
| 0. Foundations | 1–6 | Python scripts, first Claude API call | Python, terminal, Git, JSON, HTTP APIs, secrets |
| 1. Talk & know | 7–14 | #1 Knowledge, #2 Lead Qualification, #3 Product Recommendation | RAG, embeddings, structured output, tool calling |
| 2. Transact safely | 15–22 | #4 Customer Support, #5 Pricing & Promotion, #6 Quote & Order | Multi-tool flows, deterministic pricing, confirmation, idempotency |
| ⭐ Milestone | ~20 | **Manager prototype** that routes between #1, #2, #3, #5 (and #7 when ready) | Routing, handoffs, shared context |
| 3. Time & people | 23–30 | #7 Scheduling, #8 Specialist Support, #9 Maintenance | Slot locking, RBAC, cron jobs, long-lived state |
| 4. Field ops & money | 31–38 | #10 Installation & QA, #11 Specialist Dispatch, #12 Payment & Payout | Vision, scoring, retries, webhooks, reconciliation |
| 5. Growth & insight | 39–44 | #13 Social & Referral, #14 Marketing, #15 Analytics | Consent, approvals, SQL metrics |
| 6. Control tower | 45–52 | #16 Risk Review, #17 Manager Agent, Admin Dashboard | Orchestration, tracing, recovery, production ops |

---

## Phase 0: Foundations (weeks 1–6)

**Goal:** be comfortable enough with Python to read and change agent code.

- [ ] Complete [docs/PHASE0_SETUP.md](PHASE0_SETUP.md) (Python, VS Code, Git, API key)
- [ ] Python basics: variables, lists, dicts, functions, loops, `if`, files, `import` (free: **CS50P** from Harvard, weeks 0–6)
- [ ] JSON: read and write a `.json` file from Python
- [ ] HTTP APIs: what a request and a response are, and status codes
- [ ] Git: `add`, `commit`, `push`, branches
- [ ] Virtual environments and `pip install`
- [ ] Write `hello_claude.py`, then extend it into a loop that holds a back-and-forth conversation

**Exit checklist**
- [ ] I can write a 50-line Python script without copying every line
- [ ] I can call the Claude API and print the answer
- [ ] My code is on GitHub and `.env` is **not** committed

---

## Phase 1: Talk & know (weeks 7–14)

| Agent | Weeks | New skills |
|---|---|---|
| #1 Knowledge | 7–9 | System prompts, chunking, embeddings, vector search, citations, "I don't know" |
| #2 Lead Qualification | 10–11 | Pydantic models, structured output, conversation state, validation |
| #3 Product Recommendation | 12–14 | Tool calling, deterministic rules in Python, explaining a decision |

**Exit checklist (per agent)**
- [ ] Typed tool schemas (Pydantic)
- [ ] 20+ eval cases passing, including at least 3 prompt-injection cases
- [ ] It escalates or says "I don't know" instead of guessing
- [ ] Every run is traced (Langfuse or a local log file)

---

## Phase 2: Transact safely (weeks 15–22)

| Agent | Weeks | New skills |
|---|---|---|
| #4 Customer Support | 15–16 | Intent detection, multi-tool flows, ticket creation |
| #5 Pricing & Promotion | 17–19 | Pricing engine in plain Python, margin protection, output guardrail on `$` amounts |
| #6 Quote & Order | 20–22 | State machine, explicit confirmation, idempotency keys |

⭐ **Milestone (week ~20): Manager prototype.** A small router that classifies the user's intent and hands off to #1, #2, #3 or #5 with a shared `transaction_id`. This is your first portfolio demo, so record a video of it.

**Exit checklist**
- [ ] 50 pricing evals with **zero** invented prices
- [ ] Dealer cost and floor price never appear in any output (tested)
- [ ] Running `create_order` twice with the same idempotency key creates only one order

---

## Phase 3: Time & people (weeks 23–30)

| Agent | Weeks | New skills |
|---|---|---|
| #7 Scheduling | 23–25 | Calendar API, slot generation, locking, race conditions |
| #8 Specialist Support | 26–27 | Roles and permissions (RBAC), a second persona (specialists) |
| #9 Maintenance | 28–30 | Cron jobs, installed assets, recurring service, proactive messages |

**Move from mock JSON to a real database here:** SQLite first, then Supabase Postgres.

**Exit checklist**
- [ ] Concurrent booking test: 2 simultaneous bookings for one slot, exactly 1 succeeds
- [ ] A specialist can never see another specialist's jobs (tested)
- [ ] Filter-due reminders are generated automatically from the database

---

## Phase 4: Field ops & money (weeks 31–38)

| Agent | Weeks | New skills |
|---|---|---|
| #10 Installation & QA | 31–33 | Images and vision, checklists, evidence gates |
| #11 Specialist Dispatch | 34–35 | Scoring, offer → timeout → re-offer, async jobs |
| #12 Payment & Payout | 36–38 | Stripe test mode, webhooks, reconciliation, audit log |

**Exit checklist**
- [ ] A job can't be completed without the required photos, checklist and signature
- [ ] Dispatch automatically re-offers a job when a specialist declines or times out
- [ ] Payment status in the database always matches Stripe; a payout requires a QA-complete job

---

## Phase 5: Growth & insight (weeks 39–44)

| Agent | Weeks | New skills |
|---|---|---|
| #13 Social & Referral | 39–40 | Consent checks, privacy-safe content |
| #14 Marketing | 41–42 | Segments, campaign drafts, approval workflow, A/B tests |
| #15 Analytics | 43–44 | SQL views, KPI definitions, agent cost and quality metrics |

**Exit checklist**
- [ ] Nothing gets published without passing through the approval queue
- [ ] No private customer data appears in social or marketing drafts (tested)
- [ ] Analytics answers "What was conversion last month?" from SQL, not from guessing

---

## Phase 6: Control tower (weeks 45–52)

| Build | Weeks | New skills |
|---|---|---|
| #16 Risk Review | 45–47 | Policy rules in YAML, risk classification, escalation, adversarial tests |
| #17 Manager Agent | 48–51 | Full orchestration, validation, authorization, retries, recovery |
| Admin Dashboard | 50–52 | Inbox, approvals, ops, money, agent health, KPIs in one place |

**Exit checklist (= Stoupons "Definition of Done")**
- [ ] Every business-changing action goes through authenticated, typed tools
- [ ] Every action is traceable by `transaction_id`
- [ ] Retries and idempotency exist where they matter
- [ ] Failure paths exist and escalate to a human
- [ ] Policy and authorization checks are enforced in code
- [ ] All agent evals pass
- [ ] The final state can be inspected in the Admin Dashboard
- [ ] A full customer journey (lead → quote → order → slot → dispatch → install → QA → payment → maintenance reminder → referral) runs end to end

---

## FDE portfolio checkpoints

Treat each of these as a public demo (GitHub plus a short video). They are the proof of skill an FDE hiring manager looks for.

1. Week 9: RAG chatbot with citations and an eval score
2. Week 14: lead intake, then recommendation, as a structured pipeline
3. Week 20: Manager prototype that routes across agents
4. Week 30: booking agent with real availability and no double booking
5. Week 38: Stripe-backed payment workflow with reconciliation
6. Week 52: the full multi-agent system with tracing, evals and human approvals
