"""Guardrails: plain-Python safety checks that run before and after the LLM.

Input guardrails run BEFORE the model sees the message.
Output guardrails run AFTER the model answers, before the customer sees it.

They are deliberately simple rules. Rules are cheap, fast, predictable and
easy to test. Later you can add an LLM classifier (Claude Haiku) for the
cases rules miss.
"""
import re
from dataclasses import dataclass, field


@dataclass
class GuardrailResult:
    allowed: bool
    category: str = "ok"          # why it was blocked, e.g. "prompt_injection"
    reply: str = ""               # safe message to show the user when blocked


# Each entry: (category, regex pattern, safe reply to the customer)
_INPUT_RULES = [
    (
        "prompt_injection",
        r"ignore (all |any |the |your )?(previous |prior |above )?(instructions|rules|prompt)"
        r"|disregard (all |your |the )?(previous |prior )?(instructions|rules)"
        r"|you are now\b|developer mode|jailbreak|act as (an? )?(unrestricted|different)",
        "I can only help with questions about Stoupons water-treatment products and services.",
    ),
    (
        "secret_request",
        r"system prompt|(show|reveal|print|repeat|tell me) (me )?your (instructions|prompt|rules)"
        r"|api[ _-]?key|internal (notes|reference)",
        "I'm not able to share internal configuration, but I'm happy to answer questions "
        "about Stoupons products and services.",
    ),
    (
        "dealer_cost_request",
        r"dealer (cost|price)|wholesale|floor price|\bmargins?\b|markup",
        "I can't share internal cost or margin information. I'm happy to connect you with "
        "our pricing team for your customer price.",
    ),
]

# Sensitive data the customer should not be sending us in chat.
_SENSITIVE_PATTERNS = {
    "card_number": r"\b(?:\d[ -]?){13,16}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
}


def check_input(text: str) -> GuardrailResult:
    """Check a user message before any LLM sees it."""
    lowered = text.lower()
    for category, pattern, reply in _INPUT_RULES:
        if re.search(pattern, lowered):
            return GuardrailResult(allowed=False, category=category, reply=reply)
    for category, pattern in _SENSITIVE_PATTERNS.items():
        if re.search(pattern, text):
            return GuardrailResult(
                allowed=False,
                category=f"sensitive_data:{category}",
                reply="For your security, please don't share card numbers or Social Security "
                "numbers in chat. Could you ask your question without them?",
            )
    return GuardrailResult(allowed=True)


# Matches citations written like [KB-SOFT-FAQ] in an answer.
CITATION_PATTERN = re.compile(r"\[(KB-[A-Z0-9-]+)\]")
# Matches dollar amounts like $1,299 or $49.99.
MONEY_PATTERN = re.compile(r"\$\s?\d")


@dataclass
class OutputCheck:
    allowed: bool
    problems: list[str] = field(default_factory=list)


def check_knowledge_output(
    answer: str, status: str, retrieved_source_ids: set[str], canary: str
) -> OutputCheck:
    """Check a Knowledge Agent answer before the customer sees it.

    Rules:
    1. Never leak the system-prompt canary (proves the prompt was not leaked).
    2. An ANSWERED reply must cite at least one source.
    3. Every cited source must have actually been retrieved this turn
       (stops the model from inventing citations).
    4. No dollar amounts - prices come only from the Pricing Agent.
    """
    problems = []
    if canary in answer:
        problems.append("leaked_system_prompt_canary")

    cited = set(CITATION_PATTERN.findall(answer))
    if status == "ANSWERED" and not cited:
        problems.append("answered_without_citation")
    invented = cited - retrieved_source_ids
    if invented:
        problems.append(f"cited_unretrieved_sources:{sorted(invented)}")

    if MONEY_PATTERN.search(answer):
        problems.append("contains_price")

    return OutputCheck(allowed=not problems, problems=problems)
