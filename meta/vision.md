# Vision & Principles

The Knowledge Library is a persistent, structured, agent-accessible knowledge store. It serves as the single source of truth for procedural knowledge, reusable patterns, domain facts, and operational context. Any agent can query it at any time; a dedicated team of library agents maintains, enriches, and refines it continuously. The library stores knowledge only — agent configurations, governance, and operational rules live outside the library, managed by their respective owners.

## Core Principles

- **Ingest raw, synthesize across sources.** Raw material enters through `/inbox/` in any format — URLs, files, snippets, conversations. The indexer catalogues each raw item with metadata and embeddings but does not synthesize or move it. Raw items stay in `/inbox/` permanently as source material. Nuggets are created by the librarian only when cross-source patterns are discovered — combining insights from multiple raw items or existing nuggets into new knowledge that doesn't exist in any single source. This keeps the ingest barrier low while ensuring that everything in `/nuggets/` represents genuine synthesized insight.

- **Flat nuggets, rich connections.** `/nuggets/` is a flat folder — no subfolders, no hierarchy. Organization comes entirely from tags and vector embeddings. Discovery is through search, not browsing a tree.

- **Two kinds of content, one system.** Raw items in `/inbox/` are source material. Nuggets in `/nuggets/` are AI-synthesized insights. Provenance is tracked in nugget frontmatter via the `sources` field, linking each nugget back to the raw items and nuggets it was synthesized from. Discovery uses tags and vector embeddings.

- **Refinement over accumulation.** A library that only grows becomes a junkyard. The librarian agent continuously merges duplicates, validates links, and identifies gaps. Quality compounds; clutter compounds too.

- **Auditability.** Every change is logged with a reason, a timestamp, and the agent that made it. Knowledge can be versioned, reverted, and traced.

- **Inference-first content design.** Nuggets are optimised for agent consumption, not human readability. This means: high information density per token, explicit declarative statements rather than narrative prose, consistent terminology, and every constraint and exception stated rather than implied. Human-readable versions are generated on demand by the retriever.

- **Correctness is contextual.** Every nugget's health is evaluated relative to its stated assumptions and constraints, not in absolute terms. Higher-level nuggets naturally have looser constraints and broader applicability — they combine with other nuggets to derive more specific lower-level ones. The library embraces this abstraction gradient rather than demanding uniform specificity.
