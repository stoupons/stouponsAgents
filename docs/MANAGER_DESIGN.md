# Manager Agent, Guardrails, RAG & Fine-Tuning

## Manager Agent: how it runs and monitors the workers

The Manager is **built last** (agent #17). Start a simple prototype around week 20 that routes between agents #1, #2, #3 and #5.

### Responsibilities
1. Identify the user and load context (customer, property, active IDs)
2. Run input guardrails
3. Classify intent
4. Pick a worker agent
5. Pass structured context (Pydantic model, not free text)
6. Validate the worker's result against its schema
7. Authorize tool calls (RBAC + approval matrix, **in code**)
8. Detect risk and send high-risk cases to the Risk Review Agent
9. Create a human approval task and stop safely when required
10. Hand off to the next worker when needed
11. Retry failed steps (with backoff and idempotency keys)
12. Run output guardrails
13. Log the trace and cost
14. Return the final customer response

### Routing table

| User intent | Worker |
|---|---|
| Product / feature / warranty question | #1 Knowledge |
| New inquiry | #2 Lead Qualification |
| "Which system should I get?" | #3 Product Recommendation |
| Order status, problem, ticket | #4 Customer Support |
| Price / discount | #5 Pricing & Promotion |
| Ready to buy | #6 Quote & Order |
| Appointment request | #7 Scheduling |
| Specialist operational request | #8 Specialist Support |
| Filter or service due | #9 Maintenance |
| Completion / photos | #10 Installation & QA |
| Provider assignment | #11 Specialist Dispatch |
| Payment / payout | #12 Payment & Payout |
| Projects / referrals / group deals | #13 Social & Referral |
| Campaign / content | #14 Marketing |
| KPI / operations | #15 Analytics |
| Exception / dispute / high risk | #16 Risk Review |

### Design choices

- **Two-step router:** a cheap **Claude Haiku 5.5** classifier returns `{intent, confidence}` as structured output. If confidence is low, **Claude Opus 5.5** decides, and if it's still unclear, the Manager asks the user to clarify.
- **Workers as tools:** the Manager sees each worker as one tool, for example `ask_pricing_agent(context: PricingRequest) -> PricingResult`, so its own tool list stays small and typed.
- **Shared context object** travels with every handoff:
  ```python
  class TransactionContext(BaseModel):
      transaction_id: str
      customer_id: str | None
      property_id: str | None
      order_id: str | None
      job_id: str | None
      channel: str              # web, whatsapp, specialist_app, admin
      user_role: str            # customer, specialist, admin
      collected_fields: dict    # short-term memory for this conversation
  ```
- **Validation:** if a worker result doesn't match its schema, the Manager retries once with the error message. If it fails again, it escalates.
- **Recovery:** every business-changing tool takes an `idempotency_key`, so a retry never creates a second order or booking.

### Pseudocode

```
receive_request()
identify_user_and_context()
run_input_guardrails()
classify_intent()
select_worker_agent()

while task_not_complete:
    worker_result = run_worker()
    validate_worker_result()

    if worker_requests_tool:
        authorize_tool()          # RBAC + ownership + approval matrix, in code
        execute_tool()
        return_tool_result_to_worker()

    if risk_threshold_exceeded:
        route_to_risk_review()

    if human_approval_required:
        create_human_approval_task()
        stop_execution_safely()

    if another_worker_needed:
        handoff_with_structured_context()

run_output_guardrails()
log_trace_and_cost()
return_customer_response()
```

### Monitoring: the "Agent Health" page

For each agent, over the last 24 hours and 7 days:
- Requests handled, success rate, escalation rate
- Tool failure rate, validation failures, retries
- Average latency, cost per completed workflow
- Latest eval pass rate
- Alerts when escalation or failure rate jumps

---

## Guardrails

### Input (before the LLM)
| Check | How |
|---|---|
| Prompt injection ("ignore your instructions…") | Regex patterns + Haiku classifier |
| Requests for secrets or the system prompt | Rules |
| Requests for dealer cost, margin or floor price | Keyword rules → polite refusal |
| Unnecessary sensitive data (SSN, full card number) | Regex → redact before the LLM sees it |
| Abuse / spam | Haiku classifier, rate limits |
| Unsupported service area | `check_serviceability(zip)` |

### Tool (in the tool layer)
Typed schemas, RBAC, ownership checks, margin limits, payment idempotency, slot locking, payout completion requirements, approval gates.

### Output (before the customer sees it)
| Check | How |
|---|---|
| Every `$` amount appears in a tool result from this turn | Number matching against the tool-result log |
| Every date or time slot offered came from `get_available_slots` | Match against the tool-result log |
| No dealer cost, margin, floor price, API keys or internal risk scores | Rules |
| No other customers' personal info or precise neighbor addresses | Rules + Haiku check |

### Human approval matrix (enforced in code)
Refund above threshold · discount beyond automated allowance · custom installation above threshold · payout exception · warranty denial · customer dispute or chargeback · specialist suspension · suspected fraud · legal or regulatory complaint.

Thresholds live in a config file (for example `config/approvals.yaml`) so you can change them without touching prompts.

---

## RAG rules

**Use RAG for:** product manuals, FAQs, installation standards, warranty language, filter procedures, approved scripts, dealer agreement clauses, support playbooks.

**Never use RAG for:** current price, discounts, payment state, appointment slots, specialist availability, dealer payout, order status, active entitlement. Those come from APIs and the database.

**Every retrieval result includes:** `source_id`, `title`, `version` / `effective_date`, `passage`, `score`.

**RAG pipeline (built in agent #1):**
1. Put approved documents in `knowledge/`
2. Split them into chunks (~300–800 words, with overlap)
3. Create an embedding for each chunk
4. Store the embeddings in Chroma (later pgvector)
5. At question time, embed the question and fetch the top 3–5 chunks
6. Claude answers **only** from those chunks, cites `source_id`, and says "I don't know" when the chunks don't cover the question

---

## Memory

| Type | Where | Examples |
|---|---|---|
| Short-term | `TransactionContext` | Current chat, active IDs, collected qualification fields |
| Long-term | Database tables | Customer preferences, property profile, installed assets, service history, warranty, consent |

Conversation memory is **never** an authoritative transaction record.

---

## Evaluation

Keep a golden dataset per agent in `evals/<agent>.yaml` (20–50+ cases each).

**Test:** routing · tool choice · no invented prices · no invented availability · no dealer-cost leakage · RAG grounding and citations · escalation · tool-argument accuracy · task completion · customer-safe wording · prompt injection.

**Track over time:** automation rate · escalation rate · tool failure rate · incorrect action rate · conversion · support resolution · latency · cost per completed workflow · customer satisfaction.

---

## Fine-tuning policy

**Don't fine-tune at the start.** Work through this order:
1. System instructions
2. Structured outputs
3. Tools / function calling
4. RAG
5. Few-shot examples
6. Evaluations
7. Prompt iteration
8. Fine-tuning, only for stable, repetitive error patterns

| Good candidates | Poor candidates |
|---|---|
| Intent classification (the Manager router) | Prices |
| Standardized extraction | Product facts that change |
| Stoupons tone and style | Warranty rules |
| Specialist job-note normalization | Availability |
| Support disposition classification | Customer and order state |

Dynamic facts belong in tools, databases or RAG, never in model weights.
