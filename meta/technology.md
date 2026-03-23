# Technology Stack & Risks

## Technology Stack

The library is designed to start simple (local, file-based) and scale up as needed. The following are recommended starting points.

| Component | Recommended | Notes |
|-----------|-------------|-------|
| Content store | Filesystem + Git | Markdown files with frontmatter (inbox, nuggets). Git provides versioning, diffing, and rollback. This is the canonical store. |
| Vector index | SQLite-vec / Chroma / Qdrant | Start with SQLite-vec for local. Move to Chroma or Qdrant when dataset exceeds ~50k entries. |
| Embeddings | Gemini / OpenAI / extensible | Model-agnostic via provider pattern. Default: Gemini `text-embedding-004`. Configured via `EMBEDDING_PROVIDER` in `.env`. |
| Event queue | SQLite table | A simple "events" table polled by agents. Upgrade to Redis pub-sub when latency matters. |
| Database (future) | SQLite (local) / PostgreSQL (shared) | Future migration path when file-based storage becomes a bottleneck. Would store node metadata for faster querying. Not required for Phase 1. |
| Agent runtime | Any LLM agent (Claude Code, Cursor, etc.) | The library is agent-agnostic. Each runtime queries the library through the researcher and manages its own configuration independently. |
| API layer | FastAPI / Express | Optional. Exposes library CRUD + search as an HTTP API for remote agents. |

## Risks & Mitigations

| Risk | Mitigation | Likelihood |
|------|-----------|------------|
| Librarian makes bad merges or reclassifications | All changes are logged with before/after state. Implement a "confidence threshold" — low-confidence changes are queued for human review rather than auto-applied. | Medium |
| Library grows large, vector search becomes slow | Start with SQLite-vec. Migrate to Qdrant or Chroma at ~50k entries. Implement tag-filtered search to narrow scope before vector matching. | Low (long-term) |
| Agents over-query the library, high API/token costs | Cache frequent queries. Implement a TTL-based result cache. The researcher can return cached results for identical or near-identical queries within a window. | Medium |
| Knowledge conflicts: two nuggets say different things | Both entries remain valid within their own assumptions. The librarian checks that each entry's assumptions and context are explicitly stated, and may synthesize new unifying knowledge. Quality is measured by whether assumptions are clear, not by which side is "right." | Medium |
| Tag vocabulary drift | Tags grow organically and become inconsistent. The librarian runs periodic tag reviews, the intern detects synonymous tags. | Medium |
| Synthesis quality: AI generates shallow or incorrect nuggets from raw items | Nuggets list their source IDs in the `sources` frontmatter field so provenance is always traceable. The librarian re-checks synthesis against source material during enrichment. Human review at "complete" maturity level. | Medium |
| Intern recommendation noise: too many low-value suggestions | Start with a narrow observation scope (query patterns and agent disagreements only). Expand as the review queue proves its value. Track accept/reject ratios to calibrate the intern's sensitivity. | Medium |
