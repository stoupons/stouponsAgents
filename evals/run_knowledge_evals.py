"""Run the Knowledge Agent against its golden eval set (calls the real Claude API).

    python -m evals.run_knowledge_evals            # all cases
    python -m evals.run_knowledge_evals soft-03    # one case by id

Cost: roughly $0.50-1.50 for the full set on Sonnet. Results are saved to logs/.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

from agents.knowledge.agent import KnowledgeAgent
from agents.knowledge.prompts import CANARY
from core.config import LOGS_DIR

EVAL_FILE = Path(__file__).parent / "knowledge.yaml"


def grade(case: dict, result) -> list[str]:
    """Return a list of failure reasons (empty list = pass)."""
    failures = []
    answer = result.answer.lower()

    expected = case["status"] if isinstance(case["status"], list) else [case["status"]]
    if result.status not in expected:
        failures.append(f"status {result.status}, expected {expected}")

    if case.get("sources") and result.status == "ANSWERED":
        if not set(case["sources"]) & set(result.citations):
            failures.append(f"cited {result.citations}, expected one of {case['sources']}")

    if case.get("must_include") and result.status == "ANSWERED":
        if not any(p.lower() in answer for p in case["must_include"]):
            failures.append(f"missing any of {case['must_include']}")

    if case.get("must_include_all") and result.status == "ANSWERED":
        missing = [p for p in case["must_include_all"] if p.lower() not in answer]
        if missing:
            failures.append(f"missing {missing}")

    for phrase in case.get("must_not", []) + [CANARY]:
        if phrase.lower() in answer:
            failures.append(f"contains forbidden '{phrase}'")
    return failures


def main():
    cases = yaml.safe_load(EVAL_FILE.read_text(encoding="utf-8"))["cases"]
    if len(sys.argv) > 1:
        cases = [c for c in cases if c["id"] in sys.argv[1:]]

    rows, total_cost = [], 0.0
    for case in cases:
        agent = KnowledgeAgent()                 # fresh agent = no memory between cases
        result = agent.ask(case["question"])
        failures = grade(case, result)
        total_cost += result.cost_usd
        mark = "PASS" if not failures else "FAIL"
        print(f"{mark}  {case['id']:<9} {result.status:<13} {'; '.join(failures)}")
        rows.append({"id": case["id"], "question": case["question"], "pass": not failures,
                     "failures": failures, "status": result.status, "citations": result.citations,
                     "answer": result.answer, "transaction_id": result.transaction_id})

    passed = sum(r["pass"] for r in rows)
    print(f"\n{passed}/{len(rows)} passed ({passed / max(len(rows), 1):.0%})   cost ${total_cost:.3f}")

    LOGS_DIR.mkdir(exist_ok=True)
    out = LOGS_DIR / f"eval_knowledge_{datetime.now():%Y%m%d_%H%M%S}.json"
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Details: {out}")


if __name__ == "__main__":
    main()
