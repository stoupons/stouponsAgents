"""Tracing: write one JSON line per agent run to logs/traces.jsonl.

A trace answers "what happened, why, and what did it cost?" for every
request. Later you can send the same data to Langfuse or Arize Phoenix;
for now a local file is enough to learn the habit.
"""
import json
import uuid
from datetime import datetime, timezone

from core.config import LOGS_DIR


def new_transaction_id() -> str:
    """A unique ID that follows a request through every agent and tool."""
    return f"txn_{uuid.uuid4().hex[:12]}"


def write_trace(record: dict) -> None:
    """Append one trace record to logs/traces.jsonl."""
    LOGS_DIR.mkdir(exist_ok=True)
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), **record}
    with open(LOGS_DIR / "traces.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")
