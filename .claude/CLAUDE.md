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
│   ├── technology.md  # Tech stack, risks & mitigations
│   ├── design-principles.md  # LLM-native pipeline principles
│   └── runtime-guide.md      # Skill mapping, scripts, deployment
├── inbox/             # Raw source material (URLs, files, snippets)
├── nuggets/           # AI-synthesized insights (flat, no hierarchy)
├── relationships/     # Typed edges between items (JSON)
├── .claude/           # Claude Code runtime configuration
│   ├── CLAUDE.md      # This file. Project map.
│   ├── agents/        # Agent orchestration (AGENT.md per agent)
│   ├── skills/        # Skill modules (SKILL.md per skill)
│   ├── scripts/       # Utility scripts (notifications, data transforms, external APIs)
│   └── settings.json  # MCP servers, permissions, hooks, environment
└── TODO.md            # Implementation phases and next steps
```

## Governance

All design and architectural decisions live in `meta/`. Start with `meta/vision.md` for principles, `meta/architecture.md` for the three-layer design (storage, indexing, coordination), and `meta/schemas.md` for data contracts. The library stores knowledge only — governance and operational configuration live outside.

## Agents

Four agents maintain the library (see `meta/agents.md` for full specs):

- **Indexer** — catalogues raw items, synthesizes initial nuggets
- **Librarian** — enriches, deduplicates, discovers relationships, manages quality
- **Researcher** — query interface, returns knowledge with confidence levels
- **Intern** — read-only observer, surfaces institutional learning recommendations

For skill mapping, scripts, and deployment across runtimes, see `meta/runtime-guide.md`.

## Hooks

A `PostToolUse` agent hook monitors the `meta/` folder. Any `Write` or `Edit` to a meta file triggers a coherence check across all meta files — validating cross-references, terminology, structure, and logic consistency. See `meta/runtime-guide.md` § Hooks for details.

## Conventions

- **Content files:** Markdown with YAML frontmatter
- **IDs:** UUID for all items (raw items, nuggets)
- **Relationships:** JSON files in `/relationships/`, append-only per session
- **Tags:** flat labels, lowercase, 2–10 per item
- **Nugget discovery:** via tags, vector embeddings, and graph traversal — not folder hierarchy
