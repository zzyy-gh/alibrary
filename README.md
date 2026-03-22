# The Knowledge Library

A universal knowledge layer for autonomous agents — the single source of truth for procedural knowledge, reusable patterns, domain facts, and operational context.

## How It Works

Raw material goes into `/inbox/`. The **indexer agent** catalogues it, synthesizes AI-generated **nuggets** in `/nuggets/`, and creates typed **relationships** between items. The **researcher agent** answers queries using semantic search, tag filtering, keyword matching, and graph traversal.

```
Raw Items (inbox/)  -->  Indexer  -->  Nuggets (nuggets/)
                                  -->  Relationships (relationships/)
                                  -->  Embeddings (ChromaDB)

Queries  -->  Researcher  -->  Ranked results with confidence levels
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure embedding provider (Gemini default)
# Edit .env and add your GEMINI_API_KEY

# Ingest a raw item
python .claude/scripts/cli.py ingest --text "Your knowledge here" --title "My Item"

# Search the library
python .claude/scripts/cli.py search --query "your question" --format text

# Generate embeddings for all items
python .claude/scripts/embeddings.py embed-all

# Semantic search
python .claude/scripts/researcher.py search --query "how do agents coordinate" --format text

# Explore the relationship graph
python .claude/scripts/graph_explore.py --all --format text

# Generate visualizations
python .claude/scripts/graph_explore.py --viz          # graph.html
python .claude/scripts/embeddings.py viz               # embeddings.html
```

## Project Structure

```
alibrary/
├── meta/              # Design governance (human-owned)
│   ├── vision.md      # Core principles
│   ├── architecture.md # Three-layer design
│   ├── schemas.md     # Data contracts
│   ├── agents.md      # Agent roles and specs
│   ├── quality.md     # QA and success metrics
│   └── technology.md  # Tech stack
├── inbox/             # Raw source material
├── nuggets/           # AI-synthesized insights
├── relationships/     # Typed edges (JSON)
├── .claude/
│   ├── agents/        # Indexer, Researcher
│   ├── skills/        # Reusable task definitions
│   ├── scripts/       # Python utilities and CLI
│   └── settings.json  # MCP server config
├── requirements.txt
├── TODO.md
└── .env               # API keys (gitignored)
```

## Agents

| Agent | Role | Status |
|-------|------|--------|
| **Indexer** | Catalogues raw items, synthesizes nuggets, assigns tags, generates embeddings | Phase 1 |
| **Researcher** | Query interface — semantic search, tag filtering, graph traversal, visualization | Phase 2 |
| **Librarian** | Enrichment, deduplication, relationship discovery, staleness management | Phase 3 (planned) |
| **Intern** | Read-only observer, surfaces institutional learning | Phase 4 (planned) |

## Search Strategies

The researcher supports multiple retrieval approaches:

- **Semantic search** — find items by meaning via vector embeddings (`--query`)
- **Tag filtering** — filter by metadata tags (`--tags`)
- **Keyword search** — fulltext match in title/summary/body (`--keyword`)
- **Graph traversal** — explore relationships within N hops (`graph_explore.py --id ID --hops N`)
- **Combined** — mix any of the above with post-filtering by maturity or item type

Results include maturity-based confidence levels: stub (low), summary (medium), detailed (high), complete (authoritative).

## Embeddings

Model-agnostic embedding system configured via `.env`:

```
EMBEDDING_PROVIDER=gemini    # or "openai"
GEMINI_API_KEY=your-key      # for Gemini
# OPENAI_API_KEY=your-key    # for OpenAI
```

Switching providers requires resetting the vector index:
```bash
python .claude/scripts/embeddings.py reset
python .claude/scripts/embeddings.py embed-all
```

## MCP Integration

The library exposes an MCP tool server for Claude Code and other MCP-compatible runtimes:

- `library_search` — semantic and tag-based search
- `library_trace` — provenance tracing for nuggets
- `library_graph` — relationship graph exploration

## Tests

```bash
cd .claude/scripts && python -m pytest tests/ -v
```

84 tests covering helpers, event queue, search, graph traversal, embeddings, and CLI.

## Design Principles

- **Filesystem is the database** — Git-versioned Markdown + JSON, no application database required
- **Nuggets are always synthesized** — never copies of source material
- **Flat nuggets, rich connections** — discovery via tags, embeddings, and graph traversal
- **LLM-native** — prose instruction files interpreted directly by agents, no application code
- **Auditability** — every change logged with reason, timestamp, and agent

See `meta/vision.md` for full principles.
