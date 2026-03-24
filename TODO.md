- [x] Simplify knowledge-library-plan.md — reduce over-specification and remove micromanagement of implementation details where possible
- [x] Distill knowledge plan into meta — move governance/design content to `/meta/`, implementation to TODO

## Implementation Phases

The build is structured in four phases. Each phase produces a working system; later phases add sophistication. The goal is to have a usable library from Phase 1, not to wait until everything is built.

### Phase 1 — Foundation (Week 1–2)

Get the storage layer and the indexer working. The library can accept knowledge and store it.

- [x] **Folder initialisation:** Create the top-level folders (`/inbox/`, `/nuggets/`). Initialise Git for version control.
- [x] **Responsibility patterns:** Research and document patterns for dividing work across multiple LLM agents (specialization, delegation, observation, pipelines). Separate `meta/` file drawing from `design-principles.md` and external frameworks. Informs how agents, skills, and runtime hooks are structured.
- [x] **Update meta:** Update meta and claude.md based on new design principles and agent patterns.
- [x] **Setup hooks:** Design and setup hooks for meta changes.
- [x] **Indexer agent v1:** Build a minimal indexer that catalogues raw items (frontmatter, tags, embeddings) per `meta/schemas.md`.
- [x] **CLI interface:** A simple command-line tool for ingesting raw items (writes to `/inbox/` or calls the indexer directly) and querying nuggets by tag or keyword. This is the initial human interface.
- **Deliverable:** You can add raw items via CLI, see them catalogued in `/inbox/` with metadata, and search them via tags and embeddings.

### Phase 2 — Retrieval (Week 3–4)

Get the retriever working. The library can answer questions.

- [x] **Vector index:** Integrated OpenAI `text-embedding-3-small` with ChromaDB vector store. `embeddings.py` handles generation, storage, and search.
- [x] **Retriever agent v1:** Multi-strategy search (tag, semantic, keyword) with maturity-aware search. `retriever.py` + `retriever/AGENT.md`.
- [x] **Tool interface:** MCP stdio server (`mcp_retriever.py`) exposes `library_search` tool.
- [x] **Move generic docs to inbox:** Moved `design-principles.md`, `agent-composition.md`, `agent-flattening.md`, `responsibility-patterns.md` to `/inbox/` with raw item frontmatter.
- **Deliverable:** Any agent can query the library and get useful results. Gaps are tracked.

### Phase 3 — Refinement (Week 5–7)

Get the librarian working. The library improves itself over time.

- [ ] **Librarian agent v1:** Build the scheduled refinement loop — enrichment, link validation, deduplication, contradiction detection, consolidation, and audit logging per the Librarian spec in `meta/agents.md`.
- [ ] **Key thresholds:** Deduplication at >0.92 cosine similarity. Contradictions signal opportunities for unifying synthesis.
- **Deliverable:** The library self-heals. Stubs get enriched, links get checked, duplicates get merged, contradictions drive unifying synthesis, and overlapping nuggets are consolidated.

### Phase 4 — Intelligence (Week 8–10)

Advanced features that make the library proactively useful.

- [ ] **Librarian refinement summaries:** User-prompted updates per the Librarian spec in `meta/agents.md` — the only mechanism for crossing library knowledge into operational config.
- [ ] **Gap analysis & staleness:** Coverage pattern analysis, per-type decay rates, auto-scheduled reviews per the Librarian spec in `meta/agents.md`.
- [ ] **Quality dashboard:** Library health view — maturity distribution, stale entries, broken links, orphaned raw items, coverage heatmap, recent activity. Datasette/Metabase for health metrics dashboard.
- [ ] **Intern agent v1:** Build the observation loop per the Intern spec in `meta/agents.md`. Start with query-pattern analysis and tag quality. Produces typed recommendations into a review queue.
- [ ] **Recommendations queue & review UI:** Approve, reject, or defer intern recommendations. Includes weekly health report. Accepted recommendations become librarian tasks. Threshold alerts on metric breaches.
- **Deliverable:** The library is a self-improving, self-aware knowledge system with proactive gap filling, quality management, user-prompted governance/agent updates, and a complete feedback loop from outcomes back to source nuggets via the intern.

## Next Steps

1. **Validate the schemas:** Review the raw item and nugget schemas. Adjust fields based on specific domain needs.
2. **Seed the library:** Start with 20–30 raw items you already know are valuable. Drop them in `/inbox/` and let the indexer catalogue them. The librarian will synthesize nuggets when cross-source patterns emerge.
3. **Build Phase 1:** Folder tree, indexer, CLI.
4. **Integrate early:** As soon as the retriever is functional (Phase 2), start connecting it to working agents. Real usage reveals what the schema and retrieval need next.
