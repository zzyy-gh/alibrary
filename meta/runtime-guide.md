# Runtime Guide

The library is runtime-agnostic. Any system that can read files, call an LLM, and write files can host the library's agents. The governance documents (`agents.md`, `architecture.md`, `schemas.md`) define what agents do and how they coordinate. This document covers how to deploy them.

## Design Guidance

The implementation follows principles defined in `design-principles.md`:

- **Externalized state (§2):** Agents read from files, write results back to files. No in-memory state passing between agents.
- **Layered ownership (§3):** Each agent owns its own operating instructions. Project-level docs describe structure; agent files orchestrate; skill files execute.
- **Contracts over coupling (§4):** Skills are atomic, agent-unaware operations. Any skill is interchangeable as long as it honours the input/output contract.
- **Scripts:** Utility helpers (notifications, data transforms, external API calls) that agents or skills invoke. Scripts are runtime-specific — they handle integration with external systems that vary by deployment environment.

## Skill Mapping

Skills are the modular capabilities that agents orchestrate. Each skill is a single transformation with clear inputs and outputs. Skills never call other skills and don't know which agent invoked them.

| Skill | Indexer | Librarian | Researcher | Intern |
|-------|---------|-----------|------------|--------|
| validate-frontmatter | ✓ | | | |
| assign-tags | ✓ | ✓ | | |
| generate-embedding | ✓ | ✓ | | |
| synthesize-nugget | ✓ | ✓ | | |
| create-relationship | ✓ | ✓ | | |
| validate-links | | ✓ | | |
| detect-duplicates | | ✓ | | |
| merge-nuggets | | ✓ | | |
| score-quality | | ✓ | | |
| check-staleness | | ✓ | | |
| search-vector | | | ✓ | |
| search-tags | | | ✓ | |
| traverse-graph | | | ✓ | |
| assemble-context | | | ✓ | |
| generate-readable | | | ✓ | |

The intern has no skills — it reads everything and writes only to its recommendations queue.

## Claude Code

Claude Code organises all operational configuration under `.claude/`:

| Path | Contents |
|------|----------|
| `.claude/CLAUDE.md` | Project map. Structure, conventions, navigation. |
| `.claude/agents/{name}/AGENT.md` | Agent orchestration. Each agent has an `AGENT.md` defining its pipeline: triggers, skills wired, execution order. |
| `.claude/skills/{name}/SKILL.md` | Skill modules. Each skill has a `SKILL.md` defining one atomic transformation: input, output, constraints. Skills never call other skills. May include `assets/` and `examples/` subdirectories. |
| `.claude/scripts/` | Utility scripts invoked by agents or skills (e.g. notifications, data transforms, external API calls). |
| `.claude/settings.json` | MCP servers, permissions, hooks, environment configuration. |

The `AGENT.md` files are the executable implementation of the agent specifications in `agents.md`. They translate governance-level design ("the librarian enriches stubs") into runtime-level instructions ("run the synthesize-nugget skill on each stub nugget, then run score-quality").

The `SKILL.md` files implement the skills listed in the skill mapping table above. Each skill honours an input/output contract — the skill doesn't know which agent called it.

### Hooks

Hooks are automated checks configured in `.claude/settings.json`. A `PostToolUse` agent hook monitors the `meta/` folder — any `Write` or `Edit` triggers a coherence check across all meta files, validating cross-references, terminology, structure, and logic consistency.

## Other Runtimes

The same four agents can be implemented in any LLM runtime — Cursor, a custom Python harness, a REST API wrapper, or any other system. To adapt for a different runtime:

- Map each agent's specification to the runtime's orchestration model
- Implement skills as the runtime's equivalent of modular, composable units
- Connect agents to the shared filesystem and event queue as described in `architecture.md`
