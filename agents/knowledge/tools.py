"""The Knowledge Agent's tools, written as plain Python functions.

They are tested WITHOUT any LLM (see tests/test_knowledge.py). The agent
gets wrapped versions of them in agent.py.

Every result includes source_id, title, version, effective_date, passage
and score, as the Stoupons RAG rules require.
"""
import re

from agents.knowledge.ingest import KNOWLEDGE_DIR, get_collection, parse_document

# Per-section tags from the KB (section 18 "Recommended RAG Metadata").
TAG_FIELDS = ("product", "technology", "ro_type", "feature", "policy")

# Results scoring below this are "probably not relevant". The model is told
# about it so it can say "I don't know" instead of stretching a weak match.
# Tune it with your evals. (0.25: unrelated questions score < 0.2 on the approved KB.)
RELEVANCE_THRESHOLD = 0.25


def _search(query: str, top_k: int, where: dict | None = None) -> list[dict]:
    collection = get_collection()
    if collection.count() == 0:
        raise RuntimeError("Knowledge base is empty. Run: python -m agents.knowledge.ingest")
    found = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        where=where,
    )
    results = []
    for chunk_id, text, meta, distance in zip(
        found["ids"][0], found["documents"][0], found["metadatas"][0], found["distances"][0]
    ):
        score = round(1 - distance, 3)          # cosine similarity: 1.0 = same meaning
        results.append({
            "source_id": meta["source_id"],
            "chunk_id": chunk_id,
            "title": meta["title"],
            "section": meta["section"],
            "version": meta["version"],
            "effective_date": meta["effective_date"],
            "tags": {k: meta[k] for k in TAG_FIELDS if k in meta},
            "passage": text,
            "score": score,
            "relevant": score >= RELEVANCE_THRESHOLD,
        })
    return results


def retrieve_knowledge(query: str, top_k: int = 4) -> list[dict]:
    """Semantic search over ALL approved Stoupons documents."""
    return _search(query, top_k)


def search_faq(query: str, top_k: int = 4) -> list[dict]:
    """Semantic search over FAQ documents only."""
    return _search(query, top_k, where={"doc_type": "faq"})


def get_document(source_id: str) -> dict:
    """Return a whole APPROVED document by its source_id."""
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        meta, body = parse_document(path)
        if meta["source_id"] == source_id and meta["status"] == "approved":
            return {
                "source_id": source_id,
                "title": meta["title"],
                "version": str(meta["version"]),
                "effective_date": str(meta["effective_date"]),
                "content": re.sub(r"<!--.*?-->\s*", "", body, flags=re.DOTALL),  # drop internal notes
            }
    return {"error": f"No approved document with source_id '{source_id}'."}
