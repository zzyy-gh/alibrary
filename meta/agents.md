# Agents

Four agents maintain the library. Each has a distinct role, a clear trigger model, and access to the shared library store. The first three — indexer, librarian, researcher — are operational workers with read-write access to the library. The fourth — the intern — is an observer with read-only access, whose role is institutional learning.

## Overview

| Agent | Role | Access | Trigger |
|-------|------|--------|---------|
| Indexer | Catalogues raw items, synthesizes initial nuggets, assigns tags, generates embeddings. | Read-write content, read-only governance. | New items in `/inbox/`. Must be fast and cheap. |
| Librarian | Enriches stubs, validates links, merges duplicates, discovers relationships, identifies gaps, manages staleness. | Read-write content, read-only governance. | Scheduled (daily/weekly) + event-driven. |
| Researcher | Handles queries from agents and humans. Determines best retrieval strategy. | Read-write content, read-only governance. | On-demand via tool call or API. |
| Intern | Observes all system activity, surfaces institutional learning. | Read-only everything. Append-only to recommendations queue. | Periodic (end of day/week) or event-batch. |

---

## Indexer (Cataloguer)

The indexer is responsible for both processing new material and maintaining the sanity of `/inbox/`. It performs two roles:

### Inbox Sanity

The indexer owns the health of `/inbox/`. On each run, it scans for items with missing or malformed metadata and repairs them:

- **Frontmatter validation:** Ensure every raw item has properly structured frontmatter/metadata — title, source URL, file type, language, relevant domain, timestamp. Flag or fix items with missing or incomplete fields.
- **Record consistency:** Verify that every file in `/inbox/` has a properly structured MD registration file with complete frontmatter. Detect orphaned artifacts (files with no registration MD) and orphaned registrations (MDs pointing to missing artifacts). Reconcile any mismatches.
- **Deferred cataloguing:** Pick up any items that were dropped into `/inbox/` without going through the indexer (e.g. manual file drops) and catalogue them properly.

### Catalogue and Synthesize

When new material arrives, the indexer catalogues the raw item (frontmatter, tags, embedding) and synthesizes one or more initial nuggets from it. A single raw item may yield multiple nuggets if it covers distinct topics. Each nugget links back to its source via `derived-from`; connections to existing nuggets get additional relationship edges with a `note` explaining the link.

Initial maturity is typically "stub" or "summary" depending on synthesis depth. The indexer should be optimised for speed — smaller, faster models for classification, separate embedding model for vectors, target under 10 seconds per ingest.

---

## Librarian (Curator)

The librarian is the refinement engine. It operates asynchronously on a schedule and through event-driven tasks.

### Refinement Operations

- **Content enrichment:** Take a stub or summary nugget and deepen it: expand the synthesis, add nuance, write standalone prose, update the maturity score. May also revisit the source raw item(s) for details missed during initial indexing.
- **Inference optimisation:** When enriching entries, the goal is not "make this read better" but "make this more inferrable." Reduce ambiguity, increase density, standardise terminology, make relationships explicit, state every constraint and exception.
- **Link validation:** Check source URLs on raw items. Flag broken links, detect redirects, note if content has changed significantly since last check.
- **Deduplication:** Detect nuggets that cover substantially the same insight. Merge them into one richer entry, preserving the best content from each. Update all relationships pointing to merged entries — remap them to the surviving entry.
- **Relationship discovery:** After enriching an entry, scan for related entries. Create `derived-from` edges for dependencies and connections, and `contradicts` edges for incompatible claims. Lateral similarity is handled by vector search, not explicit edges. Also verify and strengthen provenance edges back to source raw items.
- **Cross-source synthesis:** When multiple raw items or nuggets cover related ground, synthesize new higher-order nuggets that capture the underlying pattern or principle — this creates *new* knowledge. These nuggets link back to their multiple sources via "derived-from" relationships. New nuggets inherit relevant relationships from their source nuggets where semantically valid.
- **Consolidation:** When a cluster of related nuggets collectively express a pattern that none captures individually, the librarian distills them into fewer, higher-level nuggets — this *reduces* the nugget count. The consolidated nugget links back to originals via `derived-from` (with `note` indicating what was kept vs. discarded from each). Absorbed originals are marked stale and their relationships remapped to the consolidated nugget. This is how the library develops conceptual depth: many observations become fewer principles.
- **Gap analysis:** Examine the library's shape. Identify domains with thin coverage relative to their importance or usage frequency. Flag gaps for human review or autonomous acquisition.
- **Staleness management:** Apply decay models by knowledge type. Tech-specific entries decay fast (6–12 months), conceptual entries decay slowly (2–5 years). Re-check entries past their review-by date.
- **Quality scoring:** Maintain `quality_score` per entry (completeness, accuracy, recency, usage, link health). A key dimension: whether the nugget's assumptions and constraints are explicitly stated — correctness is always relative to stated constraints. Surface the lowest-quality entries for priority attention.
- **Embedding refresh:** After any content change (enrichment, merge, consolidation, synthesis), regenerate the embedding for affected entries via the **generate-embedding** skill. The vector index stores only IDs and embeddings — stale embeddings cause semantic search to return wrong results.

### User-Prompted Updates After Refinement

After major refinement cycles, the librarian presents a summary of changes. The user decides whether to update governance rules or agent configurations. The library never silently cascades knowledge changes into operational config — the librarian reports; the user decides.

### Refinement Audit Log

Every librarian action produces a log entry: what changed, why, what the entry looked like before, and a confidence level. This enables rollback and builds trust in automated curation.

---

## Researcher (Reference Desk)

The researcher is the query interface. Other agents and humans talk to the researcher when they need knowledge.

- **Query routing:** Determine the best retrieval strategy for each query. Exact match → tag query. Vague question → vector search. Exploratory → graph traversal.
- **Multi-strategy fusion:** For complex queries, combine results from multiple indexes and rank by relevance.
- **Maturity-aware responses:** When returning a stub entry, flag it as low-confidence. When returning a fully enriched entry, flag it as high-confidence. Let the consuming agent decide how to weight it.
- **Gap detection:** When a query returns no results or only stubs, log a "knowledge:gap" event. The indexer or librarian can then prioritise acquiring or enriching that area.
- **Context assembly:** For agents with limited context windows, return concise, pre-digested knowledge — not raw documents. Summarise, extract the relevant section, or provide a structured snippet.
- **Human-readable generation:** When a human queries the library directly, generate a readable response with narrative, examples, and context — produced on the fly from the inference-optimised nuggets. These outputs are disposable: if the source nuggets change, the document is regenerated. If a human spots an error, the correction goes to the source nugget, not the generated document.
- **Visualization:** Generate interactive visual representations of the library. Relationship graph visualization shows nodes and typed edges (derived-from, contradicts) as a D3.js force-directed graph. Embedding visualization shows all items plotted in 2D space via t-SNE dimensionality reduction, revealing semantic clusters and gaps. Both produce self-contained HTML files.

---

## Intern (Institutional Learner)

Read-only to everything — library content, agent logs, event history, user conversations. Append-only to a dedicated recommendations queue.

The intern is the library's capacity for self-awareness at the system level. It cannot write to the library directly. It outputs recommendations into a review queue that humans or senior agents approve or reject.

### What the Intern Observes

- **Query patterns:** Repeated topics, phrasings that miss existing entries, synonym gaps in embeddings.
- **Agent disagreements:** Indexer and librarian disagree on tags, relationships, or synthesis quality.
- **Refinement outcomes:** Reverted merges, degraded enrichments, wrong classifications.
- **User conversation signals:** Concepts, terminology, and knowledge that surfaces in conversation but never gets indexed.
- **System-level gaps:** Structural issues beyond content — missing relationship types, tag vocabulary drift, organizational patterns.

### What the Intern Outputs

All intern output goes into a recommendations queue with a type, a rationale, and a suggested action. Recommendations are never auto-applied. Examples:

- **Policy update:** "The 0.92 cosine threshold for deduplication is too aggressive based on 7 false merges this month. Suggest lowering to 0.88."
- **Missing knowledge:** "Users have asked about 'edge computing deployment patterns' in 12 conversations this month. The library has zero entries. Recommend acquisition."
- **Agent self-improvement:** "The indexer's synthesis quality for technical articles is low — 40% of its nuggets get substantially rewritten by the librarian. Suggest refining the indexer's synthesis strategy."

### Why the Intern Stays Read-Only

The read-only constraint is permanent by design, not a temporary limitation. The intern's value comes from its outsider perspective — it never defends past decisions because it never made any. Giving it write access would turn it into another librarian.
