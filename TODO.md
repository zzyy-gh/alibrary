- [x] Simplify knowledge-library-plan.md — reduce over-specification and remove micromanagement of implementation details where possible
- [x] Distill knowledge plan into meta — move governance/design content to `/meta/`, implementation to TODO

## Implementation Phases

The build is structured in four phases. Each phase produces a working system; later phases add sophistication. The goal is to have a usable library from Phase 1, not to wait until everything is built.

### Phase 1 — Foundation (Week 1–2)

Get the storage layer and the indexer working. The library can accept knowledge and store it.

- [x] **Folder initialisation:** Create the top-level folders (`/inbox/`, `/nuggets/`, `/relationships/`). Initialise Git for version control.
- [x] **Responsibility patterns:** Research and document patterns for dividing work across multiple LLM agents (specialization, delegation, observation, pipelines). Separate `meta/` file drawing from `design-principles.md` and external frameworks. Informs how agents, skills, and runtime hooks are structured.
- [x] **Update meta:** Update meta and claude.md based on new design principles and agent patterns.
- [x] **Setup hooks:** Design and setup hooks for meta changes.
- [x] **Event queue setup:** Create a SQLite database with an events table for agent coordination.
- [x] **Indexer agent v1:** Build a minimal indexer that catalogues raw items and synthesizes initial nuggets per `meta/schemas.md`.
- [x] **CLI interface:** A simple command-line tool for ingesting raw items (writes to `/inbox/` or calls the indexer directly) and querying nuggets by tag or keyword. This is the initial human interface.
- **Deliverable:** You can add raw items via CLI, see them catalogued in `/inbox/` with metadata, browse synthesized nuggets in `/nuggets/`, and trace provenance from nuggets back to raw items via relationships.

### Phase 2 — Retrieval (Week 3–4)

Get the researcher working. The library can answer questions.

- [ ] **Vector index:** Integrate an embedding model. Generate embeddings for all existing entries. Store in SQLite-vec or Chroma.
- [ ] **Researcher agent v1:** Build the query interface. Supports tag filtering, semantic search, and graph traversal. Returns results ranked by relevance with maturity/confidence indicators.
- [ ] **Tool interface:** Expose the researcher as a callable tool that any agent runtime can invoke — not just Claude Code. This is the agent-agnostic query API.
- [ ] **Gap logging:** When a query returns no results, log a "knowledge:gap" event with the original query.
- [ ] **Graph exploration:** Interface for traversing the relationship graph within N hops. Neo4j or D3.js force graph for typed relationship exploration.
- **Deliverable:** Any agent can query the library and get useful results. Gaps are tracked. Relationships are explorable.

### Phase 3 — Refinement (Week 5–7)

Get the librarian working. The library improves itself over time.

- [ ] **Librarian agent v1:** Build the scheduled refinement loop — enrichment, link validation, deduplication, relationship discovery, contradiction detection, consolidation, and audit logging per the Librarian spec in `meta/agents.md`.
- [ ] **Key thresholds:** Deduplication at >0.92 cosine similarity. Contradictions create `contradicts` edges and signal opportunities for unifying synthesis.
- **Deliverable:** The library self-heals. Stubs get enriched, links get checked, duplicates get merged, contradictions drive unifying synthesis, overlapping nuggets are consolidated, and relationships emerge.

### Phase 4 — Intelligence (Week 8–10)

Advanced features that make the library proactively useful.

- [ ] **Librarian refinement summaries:** User-prompted updates per the Librarian spec in `meta/agents.md` — the only mechanism for crossing library knowledge into operational config.
- [ ] **Gap analysis & staleness:** Coverage pattern analysis, per-type decay rates, auto-scheduled reviews per the Librarian spec in `meta/agents.md`.
- [ ] **Quality dashboard:** Library health view — maturity distribution, stale entries, broken links, orphaned raw items, coverage heatmap, recent activity. Datasette/Metabase over SQLite for health metrics dashboard.
- [ ] **Intern agent v1:** Build the observation loop per the Intern spec in `meta/agents.md`. Start with query-pattern analysis and tag/relationship quality. Produces typed recommendations into a review queue.
- [ ] **Recommendations queue & review UI:** Approve, reject, or defer intern recommendations. Includes weekly health report. Accepted recommendations become librarian tasks. Threshold alerts on metric breaches.
- **Deliverable:** The library is a self-improving, self-aware knowledge system with proactive gap filling, quality management, user-prompted governance/agent updates, and a complete feedback loop from outcomes back to source nuggets via the intern.

## Post-Phase 4

- [ ] **Move generic docs to inbox:** `meta/design-principles.md`, `meta/agent-composition.md`, `meta/agent-flattening.md` and `meta/responsibility-patterns.md` are too generic for library-specific governance — move them to `/inbox/` as raw source material. Update references in `meta/agents.md` and the respective agent documentations to point to their new location.

## Next Steps

1. **Validate the schemas:** Review the raw item, nugget, and relationship schemas. Adjust fields based on specific domain needs.
2. **Seed the library:** Start with 20–30 raw items you already know are valuable. Drop them in `/inbox/` and let the indexer synthesize initial nuggets.
3. **Build Phase 1:** Folder tree, event queue, indexer, CLI.
4. **Integrate early:** As soon as the researcher is functional (Phase 2), start connecting it to working agents. Real usage reveals what the schema and retrieval need next.
