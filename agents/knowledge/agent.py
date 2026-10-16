"""Knowledge Agent: answers Stoupons questions only from approved documents.

The flow for every question:

    question
      -> input guardrails        (block prompt injection, secrets, dealer cost)
      -> Claude + tools          (search the knowledge base, then answer with citations)
      -> output guardrails       (citations real? no prices? no prompt leak?)
      -> trace                   (log everything + cost to logs/traces.jsonl)
      -> answer
"""
import json
import re
import time
from dataclasses import dataclass, field

import anthropic
from anthropic import beta_tool

from agents.knowledge import tools as kb
from agents.knowledge.prompts import CANARY, SYSTEM_PROMPT
from core.config import WORKER_MODEL, estimate_cost
from core.guardrails import CITATION_PATTERN, check_input, check_knowledge_output
from core.tracing import new_transaction_id, write_trace

AGENT_NAME = "knowledge"
STATUS_PATTERN = re.compile(r"\n?\s*STATUS:\s*(ANSWERED|UNKNOWN|OUT_OF_SCOPE)\s*$")
SAFE_FALLBACK = (
    "I'm not completely sure about that, and I don't want to guess. "
    "I can connect you with a Stoupons team member who can help."
)


@dataclass
class KnowledgeResult:
    """What the agent returns. The Manager Agent will consume this later."""
    transaction_id: str
    answer: str
    status: str                       # ANSWERED | UNKNOWN | OUT_OF_SCOPE | BLOCKED | ESCALATED
    citations: list[str] = field(default_factory=list)
    blocked_by: str | None = None     # which guardrail stopped it, if any
    cost_usd: float = 0.0


class KnowledgeAgent:
    def __init__(self, model: str = WORKER_MODEL, client: anthropic.Anthropic | None = None):
        self.model = model
        self.client = client or anthropic.Anthropic()
        # Short-term memory: previous questions and answers (text only).
        self.history: list[dict] = []

    # ------------------------------------------------------------------ tools
    def _make_tools(self, tool_log: list, retrieved_ids: set):
        """Wrap the plain tools so Claude can call them, and record each call
        so the output guardrail knows which sources were really retrieved."""

        def run(name: str, args: dict, fn):
            try:
                result = fn()
            except Exception as exc:  # report tool failures to Claude instead of crashing
                result = {"error": str(exc)}
            items = result if isinstance(result, list) else [result]
            retrieved_ids.update(r["source_id"] for r in items if "source_id" in r)
            tool_log.append({
                "tool": name,
                "args": args,
                "results": [
                    {"chunk_id": r.get("chunk_id", r.get("source_id")), "score": r.get("score")}
                    for r in items
                ],
            })
            return json.dumps(result)

        @beta_tool(strict=True)
        def retrieve_knowledge(query: str) -> str:
            """Search ALL approved Stoupons documents. Use this first.

            Covers FAQs, warranty policy, installation standards and maintenance guides.
            Returns passages with source_id, title, version, effective_date, passage,
            score and a relevant flag.

            Args:
                query: What to search for, e.g. the customer's question in your own words.
            """
            return run("retrieve_knowledge", {"query": query}, lambda: kb.retrieve_knowledge(query))

        @beta_tool(strict=True)
        def search_faq(query: str) -> str:
            """Search only the customer FAQ documents.

            Same result format as retrieve_knowledge.

            Args:
                query: What to search for.
            """
            return run("search_faq", {"query": query}, lambda: kb.search_faq(query))

        @beta_tool(strict=True)
        def get_document(source_id: str) -> str:
            """Get the full text of one approved document.

            Use it when a passage is not enough to answer.

            Args:
                source_id: The document's source_id, e.g. KB-WARRANTY.
            """
            return run("get_document", {"source_id": source_id}, lambda: kb.get_document(source_id))

        return [retrieve_knowledge, search_faq, get_document]

    # -------------------------------------------------------------------- ask
    def ask(self, question: str, transaction_id: str | None = None) -> KnowledgeResult:
        txn = transaction_id or new_transaction_id()
        started = time.perf_counter()
        trace = {"transaction_id": txn, "agent": AGENT_NAME, "model": self.model, "question": question}

        # 1. Input guardrails: the LLM never sees a blocked message.
        gate = check_input(question)
        if not gate.allowed:
            result = KnowledgeResult(txn, gate.reply, "BLOCKED", blocked_by=gate.category)
            write_trace({**trace, "status": "BLOCKED", "blocked_by": gate.category,
                         "latency_s": round(time.perf_counter() - started, 2)})
            return result

        # 2. Claude + tools. The tool runner loops: Claude calls a tool, the SDK
        #    runs our Python function, sends the result back, until Claude is done.
        tool_log, retrieved_ids = [], set()
        runner = self.client.beta.messages.tool_runner(
            model=self.model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            tools=self._make_tools(tool_log, retrieved_ids),
            messages=[*self.history, {"role": "user", "content": question}],
            output_config={"effort": "medium"},
            max_iterations=6,                       # safety stop for runaway loops
            # If Claude's safety classifier declines, retry on a fallback model automatically.
            fallbacks="default",
            betas=["server-side-fallback-2026-07-01"],
        )
        input_tokens = output_tokens = 0
        final = None
        for message in runner:                      # one message per loop step
            input_tokens += message.usage.input_tokens
            output_tokens += message.usage.output_tokens
            final = message

        cost = estimate_cost(self.model, input_tokens, output_tokens)
        raw_text = "".join(b.text for b in final.content if b.type == "text").strip()

        # 3. Read the STATUS line, then hide it from the customer.
        match = STATUS_PATTERN.search(raw_text)
        status = match.group(1) if match else "MISSING"
        answer = STATUS_PATTERN.sub("", raw_text).strip()
        if final.stop_reason == "refusal":
            answer, status = SAFE_FALLBACK, "UNKNOWN"

        # 4. Output guardrails: anything suspicious becomes a safe hand-off.
        check = check_knowledge_output(answer, status, retrieved_ids, CANARY)
        problems = list(check.problems)
        if status == "MISSING":
            problems.append("missing_status_line")
        if problems:
            final_answer, final_status = SAFE_FALLBACK, "ESCALATED"
        else:
            final_answer, final_status = answer, status

        result = KnowledgeResult(
            transaction_id=txn,
            answer=final_answer,
            status=final_status,
            citations=sorted(set(CITATION_PATTERN.findall(final_answer))),
            cost_usd=cost,
        )

        # Remember the conversation for follow-up questions.
        self.history += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": final_answer},
        ]

        # 5. Trace: everything needed to debug this answer later.
        write_trace({
            **trace,
            "status": final_status,
            "model_status": status,
            "stop_reason": final.stop_reason,
            "tool_calls": tool_log,
            "retrieved_sources": sorted(retrieved_ids),
            "citations": result.citations,
            "output_problems": problems,
            "raw_answer": raw_text if problems else None,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 6),
            "latency_s": round(time.perf_counter() - started, 2),
        })
        return result
