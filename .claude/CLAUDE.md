# The Knowledge Library

A universal knowledge layer for autonomous agents — the single source of truth for procedural knowledge, reusable patterns, domain facts, and operational context.

## Structure

```
alibrary/
├── meta/              # Design governance (human-owned, agents read for guidance)
│   ├── vision.md      # Core principles
│   ├── architecture.md # Storage, indexing, coordination
│   ├── schemas.md     # Data contracts (raw items, nuggets, relationships)
│   ├── agents.md      # Agent roles, boundaries, operational specs
│   ├── quality.md     # QA loops, feedback triggers, success metrics
│   └── technology.md  # Tech stack, risks & mitigations
├── inbox/             # Raw source material (URLs, files, snippets)
├── nuggets/           # AI-synthesized insights (flat, no hierarchy)
├── relationships/     # Typed edges between items (JSON)
├── .claude/           # Claude Code runtime configuration
│   ├── CLAUDE.md      # This file. Project map.
│   ├── agents/
│   │   ├── indexer/AGENT.md    # Indexer agent orchestration
│   │   └── researcher/AGENT.md # Researcher agent — query interface
│   ├── skills/
│   │   ├── coherence-check/    # Validate meta/ and .claude/ coherence
│   │   ├── validate-frontmatter/ # Validate/repair raw item frontmatter
│   │   ├── assign-tags/        # Generate tags for items
│   │   ├── synthesize-nugget/  # Create nuggets from raw items
│   │   ├── create-relationship/ # Create typed relationship edges
│   │   └── generate-embedding/ # Generate vector embeddings via OpenAI
│   ├── scripts/
│   │   ├── helpers.py          # Shared utilities (UUID, frontmatter, relationships)
│   │   ├── init_db.py          # Initialize SQLite event queue
│   │   ├── emit_event.py       # Emit events to the queue
│   │   ├── poll_events.py      # Poll/consume events from the queue
│   │   ├── find_unprocessed.py # Find raw items with no derived-from edge
│   │   ├── cli.py             # CLI: ingest, query, trace, search
│   │   ├── embeddings.py      # Embedding generation + ChromaDB vector store
│   │   ├── researcher.py      # Multi-strategy search (tag, semantic, keyword)
│   │   ├── graph_explore.py   # Relationship graph traversal + visualization
│   │   └── mcp_researcher.py  # MCP tool server for library search
│   └── settings.json  # MCP servers, permissions, environment
└── TODO.md            # Implementation phases and next steps
```

## Governance

All design and architectural decisions live in `meta/`. Start with `meta/vision.md` for principles, `meta/architecture.md` for the three-layer design (storage, indexing, coordination), and `meta/schemas.md` for data contracts. The library stores knowledge only — governance and operational configuration live outside.

## Conventions

- **Content files:** Markdown with YAML frontmatter
- **IDs:** UUID for all items (raw items, nuggets)
- **Relationships:** JSON files in `/relationships/`, append-only per session
- **Tags:** flat labels, lowercase, 2–10 per item
- **Nugget discovery:** via tags, vector embeddings, and graph traversal — not folder hierarchy
