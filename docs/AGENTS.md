# Agent Catalog: All 17 Agents, Easiest to Hardest

## The 10-step recipe (use it for every agent)

1. **Agent card:** write `agents/<name>/README.md` covering its job, inputs, outputs, tools, what it must never do, and when it escalates.
2. **Mock data:** add what it needs to `data/mock/*.json`.
3. **Tools first, no LLM:** write the tools as plain Python functions with Pydantic input and output types, then test them with pytest.
4. **System prompt:** role, rules, tone, refusal and escalation behavior.
5. **Connect to Claude:** use the Anthropic SDK Tool Runner with `strict: true` tool schemas.
6. **Guardrails:** input checks before the LLM, output checks after it.
7. **Tracing:** log every LLM and tool call with `transaction_id`, tokens and cost.
8. **Evals:** write 20–50 cases in `evals/<agent>.yaml`: normal, edge, adversarial and prompt injection.
9. **Iterate:** run the evals, fix the prompt or tools, and repeat until they pass.
10. **Register:** add the agent to the Manager's routing table and the Admin Dashboard.

Default model per agent: **Opus 5.5** for #16 and #17, **Sonnet 5.5** for workers, **Haiku 5.5** for routers and classifiers. Measure with your evals before you change any of them.

---

## Level 1: Beginner (prompting, RAG, simple tools)

### #1 Knowledge Agent (difficulty 1/10)
- **Job:** answer product, feature, warranty, filter and installation questions **only** from approved Stoupons documents.
- **Tools:** `retrieve_knowledge(query)`, `get_document(source_id)`, `search_faq(query)`
- **Build steps:**
  1. Put 5–10 approved docs in `knowledge/` (FAQ, softener manual, RO manual, warranty terms).
  2. Write `ingest.py`: load files, chunk them, embed the chunks, store them in Chroma.
  3. Write `retrieve_knowledge()` to return the top chunks with `source_id`, title, version, passage and score.
  4. System prompt: "Answer only from the provided passages. Cite source_id. If the passages don't answer it, say you don't know and offer a human."
  5. Evals: 20 answerable questions, 5 unanswerable ones, and 3 injection attempts.
- **Must never:** answer price, availability or order status questions. Those get handed back to the Manager.
- **Done when:** it answers only from trusted documents and says when it doesn't know.

### #2 Lead Qualification Agent (2/10)
- **Job:** turn a conversation into a clean, structured lead.
- **Collects:** ZIP, household size, home size, service requested, water issues, loop availability, preferred package, preferred date, installation notes.
- **Tools:** `create_lead()`, `update_lead()`, `check_serviceability(zip)`
- **Build steps:**
  1. Define a Pydantic `Lead` model; required fields are non-optional.
  2. After each turn, Claude extracts the fields it learned (structured output) and the code merges them into the lead.
  3. The code works out which fields are still missing, and Claude asks for them one or two at a time.
  4. Check serviceability as soon as the ZIP is known, and end politely if the area isn't served.
- **Done when:** any chat produces a valid `Lead` record with no manual typing.

### #3 Product Recommendation Agent (3/10)
- **Job:** recommend a 48K, 64K or 96K softener, an RO system, or a package, and explain why.
- **Tools:** `get_product_catalog()`, `get_customer_profile()`, `retrieve_knowledge()`
- **Build steps:**
  1. Write the sizing rule **in Python**, for example people × ~75 gal/day × hardness (gpg) × days between regenerations → grain capacity.
  2. Claude calls the rule tool and only *explains* the result in friendly language, along with a comparison table.
- **Done when:** recommendations always match the Python rule and the explanation cites the reasons.

### #4 Customer Support Agent (3/10)
- **Job:** order status, FAQs, troubleshooting, warranty intake, tickets.
- **Tools:** `get_customer()`, `get_order()`, `get_installed_asset()`, `get_ticket()`, `create_ticket()`, `retrieve_knowledge()`
- **Build steps:** detect intent, call the right tools, answer or troubleshoot from the knowledge base, and create a ticket when unsure.
- **Must:** check that the person asking owns the order (ownership check in the tool).
- **Done when:** it resolves common questions and creates a ticket whenever it can't solve something safely.

## Level 2: Intermediate (deterministic business logic)

### #5 Pricing & Promotion Agent (4/10)
- **Job:** explain approved prices and incentives.
- **Tools:** `get_price(product, zip)`, `get_promotion_eligibility(customer)`, `calculate_quote(items, zip, promo)`
- **Hard rules:** the LLM **never** calculates prices. `calculate_quote` is pure Python. Dealer cost, margin and floor price never leave the tool.
- **Guardrail:** the output check blocks any `$` amount that doesn't appear in this turn's tool results.
- **Done when:** every price shown came from the pricing engine (50 evals, zero invented numbers).

### #6 Quote & Order Agent (5/10)
- **Job:** create a quote, then turn it into an order after an explicit "yes".
- **Tools:** `create_quote()`, `accept_quote()`, `create_order()`, `get_payment_link()`
- **Build steps:** state machine `draft → presented → confirmed → ordered`. `create_order` requires `quote.status == confirmed` and takes an idempotency key.
- **Done when:** an approved quote safely becomes an order exactly once.

### #7 Scheduling Agent (5/10)
- **Job:** offer real slots; book, reschedule and cancel.
- **Tools:** `get_available_slots()`, `book_slot()`, `reschedule_slot()`, `cancel_slot()`
- **Build steps:** slots are generated from specialist calendars. `book_slot` uses a database transaction or lock.
- **Done when:** it only offers real slots, and a concurrent-booking test never double-books.

### #8 Specialist Support Agent (5/10)
- **Job:** dealers and specialists manage their assigned jobs and availability.
- **Tools:** `get_specialist()`, `get_job()`, `update_availability()`, `acknowledge_service_request()`, `record_specialist_response()`
- **Must:** role = specialist, and every tool checks `job.specialist_id == caller_id`.
- **Done when:** specialists self-serve without staff coordinating over WhatsApp.

## Level 3: Advanced (workflow automation, operational state)

### #9 Maintenance Agent (6/10)
- **Job:** filter replacements, preventive maintenance, reminders, warranty visits.
- **Tools:** `get_installed_asset()`, `get_maintenance_schedule()`, `create_maintenance_job()`, `get_available_slots()`, `book_slot()`, `create_ticket()`
- **Build steps:** a daily cron finds assets that are due, drafts reminders, and books visits on reply.
- **Done when:** filter and warranty visits are initiated, scheduled and tracked without Excel.

### #10 Installation & QA Agent (6/10)
- **Job:** verify checklists, signatures, completion photos and job completion.
- **Tools:** `get_job()`, `upload_completion_photo()`, `record_checklist()`, `record_signature()`, `mark_job_complete()`, `create_issue()`
- **Build steps:** Claude vision checks the photos against required shots (bypass loop, drain line, unit label). `mark_job_complete` refuses if any evidence is missing.
- **Done when:** no job can be completed without the required evidence.

### #11 Specialist Dispatch Agent (7/10)
- **Job:** match orders to the best eligible specialist.
- **Tools:** `rank_specialists()`, `offer_job()`, `reoffer_job()`, `assign_specialist()`
- **Scoring (Python):** availability, service area, skill match, distance, rating, SLA, workload, payout, prior customer relationship.
- **Build steps:** offer → wait N minutes → if declined or no answer, re-offer to the next one → after X tries, escalate.
- **Done when:** jobs are assigned automatically, with retries on decline.

### #12 Payment & Payout Agent (8/10)
- **Job:** track customer payments and dealer payouts.
- **Tools:** `get_payment_status()`, `record_customer_payment()`, `create_payout_request()`, `get_payout_status()`
- **Hard rules:** truth comes only from Stripe webhooks. No money moves on chat confirmation alone. A payout requires a QA-complete job, and exceptions go to approval.
- **Done when:** the database and Stripe always match (reconciliation job + alerts).

## Level 4: Advanced AI product engineering

### #13 Social & Referral Agent (8/10)
- **Job:** neighborhood project posts, referrals, group deals, social proof.
- **Tools:** `get_project()`, `get_customer_consent()`, `create_project_post_draft()`, `get_referral_status()`, `get_group_deal()`
- **Must:** consent check first. Never publish exact addresses or names without consent. Drafts go to the approval queue.

### #14 Marketing Agent (8/10)
- **Job:** localized campaigns, follow-ups, abandoned-quote drafts.
- **Tools:** `get_campaign_rules()`, `get_market()`, `get_offer()`, `create_campaign_draft()`
- **Must:** use approved offers only, define a measurable objective for every campaign, and require human approval before sending.

### #15 Analytics Agent (8/10)
- **Job:** answer KPI questions: conversion, automation rate, SLA, revenue, margin, escalations, agent cost.
- **Tools:** `query_metrics()` (read-only SQL views), `get_agent_traces()`, `get_cost_metrics()`
- **Must:** read-only. Metric definitions live in one place (a semantic layer).

### #16 Risk Review Agent (9/10)
- **Job:** review exceptions, disputes, unusual discounts, custom installs, suspected fraud, repeated quality failures.
- **Tools:** `get_policy()`, `get_order()`, `get_customer()`, `get_specialist()`, `create_escalation()`
- **Build steps:** policies live in YAML. Claude classifies the case against the policy and returns `approve | block | escalate` with reasons. Adversarial evals try to trick it.
- **Done when:** high-risk actions are consistently blocked, approved or escalated according to policy.

## Level 5: Expert

### #17 Manager Agent (10/10)
See [MANAGER_DESIGN.md](MANAGER_DESIGN.md).
- **Done when:** a customer request moves through multiple agents and systems while the Manager maintains context, policy, auditability and recovery.

---

## Suggested first six projects

1. Water Softener FAQ RAG chatbot → #1
2. Water Softener lead intake agent → #2
3. 48K/64K/96K recommendation agent → #3
4. ZIP-based pricing tool connected to an agent → #5
5. Appointment availability and booking agent → #7
6. **Manager prototype** that routes among the first five

After these work, gradually replace the mock JSON with real Stoupons APIs and databases.
