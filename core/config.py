"""Shared settings for every Stoupons agent.

Everything that might change (model names, prices, folder paths) lives here,
so you change it in ONE place instead of hunting through every agent.
"""
from pathlib import Path

from dotenv import load_dotenv

# Folder that contains this repo (core/ is one level down from it).
ROOT = Path(__file__).resolve().parent.parent

# Reads ANTHROPIC_API_KEY (and anything else) from the .env file.
load_dotenv(ROOT / ".env")

# --- Folders ---------------------------------------------------------------
KNOWLEDGE_DIR = ROOT / "knowledge"      # approved documents for RAG
CHROMA_DIR = ROOT / "chroma_db"         # the local vector database (git-ignored)
LOGS_DIR = ROOT / "logs"                # trace logs (git-ignored)

# --- Models ----------------------------------------------------------------
# Worker agents use Sonnet (see docs/AGENTS.md). Change it here, then re-run
# the evals to check quality before keeping the change.
WORKER_MODEL = "claude-sonnet-5-5"

# Price per 1 million tokens in US dollars: (input, output).
# Source: Anthropic price table, Oct 2026. Used only to estimate cost in traces.
MODEL_PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Return the estimated cost in dollars for one or more API calls."""
    price_in, price_out = MODEL_PRICES.get(model, (0.0, 0.0))
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000
