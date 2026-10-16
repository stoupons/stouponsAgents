# Knowledge Base

The Knowledge Agent (#1) answers **only** from the approved documents in this folder.

| Location | What it is | Indexed? |
|---|---|---|
| `knowledge/*.md` with `status: approved` | Approved, customer-facing knowledge | ✅ Yes |
| `knowledge/*.md` with any other status | Work in progress | ❌ No |
| `knowledge/drafts/` | Placeholder sample text written during setup. **Not approved; contains facts that conflict with KB-WS-RO.** | ❌ No |
| `knowledge/originals/` | Original source files (PDF/DOCX) for provenance | ❌ No (the `.md` conversion is what gets indexed) |

## Approved documents
| source_id | File | Version | Converted from |
|---|---|---|---|
| `KB-WS-RO` | [water_softener_ro_kb.md](water_softener_ro_kb.md) | 1.0 | [originals/Stoupons_Water_Softener_RO_Internal_Knowledge_Base.pdf](originals/Stoupons_Water_Softener_RO_Internal_Knowledge_Base.pdf) |

## Adding or updating a document
1. Put the original file in `originals/`.
2. Convert it to a `.md` file in this folder:
   - Front matter: `source_id`, `title`, `doc_type`, `version`, `effective_date`, `status`.
   - One `## ` heading per topic. Each section becomes one search chunk, so keep sections under ~150 words.
   - Optional tags under a heading: `<!-- meta: {product: water_softener, technology: wifi} -->`
   - Keep the approved wording. Don't paraphrase policy text.
3. Set `status: approved` only after Stoupons has signed off on it.
4. Rebuild the index: `python -m agents.knowledge.ingest`
5. Add eval cases for the new content to `evals/knowledge.yaml` and run the evals.

When a document changes, bump its `version`. Per the KB's governance section, any change to capacities, technology, warranty, filters, pricing, installation, maintenance or specialist obligations must be updated here **before** agents use it.
