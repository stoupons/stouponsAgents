"""Step 1 of RAG: turn approved documents into searchable chunks.

    python -m agents.knowledge.ingest

What happens:
1. Read every .md file directly in knowledge/ (sub-folders like drafts/ are ignored)
2. Read its header ("front matter"): source_id, title, version, status, ...
3. GOVERNANCE GATE: only documents with `status: approved` are indexed.
   Drafts and samples can never reach customers by accident.
4. Split the body into chunks, one per "## " section. A section may carry its
   own metadata on the line under the heading:
       <!-- meta: {product: water_softener, technology: bluetooth} -->
5. Store each chunk in Chroma. Chroma turns the text into an EMBEDDING
   (a list of numbers that captures its meaning) using a small free model
   that runs on your computer, so similar meanings end up close together.

Re-run this every time you add or change a document.
"""
import re
from pathlib import Path

import chromadb
import yaml
from chromadb.config import Settings

from core.config import CHROMA_DIR, KNOWLEDGE_DIR

COLLECTION_NAME = "stoupons_knowledge"
REQUIRED_FIELDS = ("source_id", "title", "doc_type", "version", "effective_date", "status")
SECTION_META = re.compile(r"^\s*<!--\s*meta:\s*(\{.*?\})\s*-->\s*$", re.MULTILINE)


def get_collection():
    """Open (or create) the vector database collection."""
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False)
    )
    # "cosine" distance: 0 = identical meaning, 2 = opposite.
    return client.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )


def parse_document(path: Path) -> tuple[dict, str]:
    """Split a file into (front-matter dict, body text)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name} is missing its front matter header")
    _, header, body = text.split("---", 2)
    meta = yaml.safe_load(header)
    for key in REQUIRED_FIELDS:
        if key not in meta:
            raise ValueError(f"{path.name} front matter is missing '{key}'")
    return meta, body.strip()


def chunk_document(meta: dict, body: str, file_name: str) -> list[dict]:
    """One chunk per '## ' section. Each chunk keeps the doc title and heading,
    which gives the embedding more context than the bare answer would."""
    chunks = []
    sections = body.split("\n## ")[1:]          # skip everything before the first section
    for n, section in enumerate(sections, start=1):
        heading, _, content = section.partition("\n")

        # Optional per-section metadata, removed from the text itself.
        section_meta = {}
        found = SECTION_META.search(content)
        if found:
            section_meta = yaml.safe_load(found.group(1))
            content = SECTION_META.sub("", content, count=1)

        metadata = {
            "source_id": meta["source_id"],
            "title": meta["title"],
            "doc_type": meta["doc_type"],
            "version": str(meta["version"]),
            "effective_date": str(meta["effective_date"]),
            "status": meta["status"],
            "section": heading.strip(),
            "file": f"knowledge/{file_name}",
        }
        metadata.update({k: str(v) for k, v in section_meta.items()})

        chunks.append({
            "id": f"{meta['source_id']}#{n}",
            "text": f"{meta['title']}\n{heading.strip()}\n{content.strip()}",
            "metadata": metadata,
        })
    return chunks


def load_all_chunks(verbose: bool = False) -> list[dict]:
    chunks = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        meta, body = parse_document(path)
        if meta["status"] != "approved":
            if verbose:
                print(f"  skipped {path.name} (status: {meta['status']})")
            continue
        doc_chunks = chunk_document(meta, body, path.name)
        if verbose:
            print(f"  {path.name}: {len(doc_chunks)} chunks ({meta['source_id']} v{meta['version']})")
        chunks.extend(doc_chunks)
    return chunks


def ingest(verbose: bool = False) -> int:
    """Rebuild the collection from scratch so deleted docs disappear too."""
    collection = get_collection()
    existing = collection.get()["ids"]
    if existing:
        collection.delete(ids=existing)

    chunks = load_all_chunks(verbose)
    if not chunks:
        raise RuntimeError("No approved documents found in knowledge/")
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )
    return len(chunks)


if __name__ == "__main__":
    count = ingest(verbose=True)
    print(f"Indexed {count} approved chunks from {KNOWLEDGE_DIR}")
