---
id: a1c52f39-b946-4af2-91f0-7217920ea127
title: Responsibility Patterns
source_type: manual
tags:
- agents
- responsibility
- patterns
- coordination
- multi-agent
created_at: 2026-03-22 00:00:00+00:00
created_by: migration
maturity: summary
---

# Responsibility Patterns

How to divide work across multiple agents. Companion to `agent-composition.md` (structural rules for agents) and `agent-flattening.md` (making agents team-ready). This file answers: given N agents, how do you carve up who does what, when, and how they stay out of each other's way?

Framework-agnostic — these are structural patterns that apply regardless of runtime.

**Status:** Draft

## TODO & Open Questions

- [ ] Research external frameworks (CrewAI, AutoGen, LangGraph, OpenAI Swarm, Claude Agent SDK) — extract patterns, not dependencies
- [ ] Write up coherence-checking as a worked example
- [ ] When does shared-filesystem coordination break down? At what scale do you need a message bus?
- [ ] Can agents span runtimes (e.g., indexer on Claude Code, retriever on a custom API) and still coordinate through the same shared state?
- [ ] Are there real-world examples of the multi-team pattern (separate agent teams coordinating on a shared project)?

---

## Division of Labor

How responsibilities are split across agents. Each pattern implies a different contract between agents about ownership, timing, and coordination.

### 1. Shared state (implicit handoff)

Each agent owns a distinct responsibility but discovers the other's work by reading shared state (filesystem, database). No direct communication — agents coordinate by leaving artifacts for each other.

**Responsibility contract:** Non-overlapping ownership. Each agent reads what others produce but only writes to its own domain.

**Tradeoffs:**

- Simple, debuggable — every state change is inspectable on disk
- No orchestration framework needed
- No real-time coordination — agents discover changes asynchronously
- Works well when agents have distinct, non-overlapping responsibilities

**Example:** The knowledge library's three agents coordinate through the filesystem and ChromaDB. The indexer catalogues raw items; the librarian synthesizes nuggets on its next scheduled run. Ownership is clear: the indexer owns `/inbox/` health and cataloguing; the librarian owns synthesis and refinement.

### 2. Parallel specialization (agent teams)

Multiple agents with distinct roles running in parallel toward the same goal. Each owns a non-overlapping concern. They coordinate through shared state, not messages. The key property: responsibilities are complementary and can execute concurrently.

**Responsibility contract:** Each agent owns a slice of the problem space. If two agents could do the same thing, merge or split until ownership is unambiguous (see `agent-composition.md` §5).

**Tradeoffs:**

- High throughput — work happens in parallel
- Requires clean separation of concerns
- Needs a coordination layer (shared filesystem, database) to prevent conflicts
- Works best when the goal decomposes into independent subtasks

**Example:** After a batch ingest, an indexer team fans out — one agent per raw item — all cataloguing to `/inbox/` in parallel. No agent waits for another.

**Example (Claude Code):** Multiple Claude Code agents running in separate terminals on the same repo, each working on a different file or module.

### 3. Pipeline (sequential handoff)

Agents run in sequence. Each stage owns a transformation; the output of one becomes the input of the next. Responsibility flows forward — once an agent hands off, it's done.

**Responsibility contract:** Each stage owns one transformation. The handoff artifact is the contract — agent A writes to a known path, agent B reads from it.

**Tradeoffs:**

- Clear data flow — easy to reason about and debug
- Each stage can be optimised independently (fast model for classification, large model for synthesis)
- Bottlenecked by the slowest stage
- Natural fit when there's a strict dependency between stages

**Example:** Raw item → Indexer (catalogue + embed) → Librarian (synthesize + enrich) → Retriever (serve). Each stage produces an artifact the next stage consumes.

### 4. Delegation (parent-child)

A parent agent delegates a subtask to a child in an isolated context. The parent retains overall responsibility; the child owns only its narrow piece. The child has no awareness of the broader pipeline.

**Responsibility contract:** The parent defines the scope; the child executes within it. The child writes output to a known location; the parent reads it and continues. See also `agent-flattening.md` §Splitting for how to prepare agents for this pattern.

**Tradeoffs:**

- Lightweight — cheaper to spawn than a full agent; no persistent state, no event queue
- Context isolation — heavy content stays in the child's context, not the parent's
- One level only — children should not spawn their own children (flat execution per `agent-composition.md` §4)
- The parent is blocked while waiting, unless the child runs asynchronously

**Example:** The librarian needs to deeply enrich a nugget from a 50-page PDF. It spawns a subagent with just the PDF and the stub nugget. The subagent writes the enriched nugget to disk. The librarian picks it up and continues with the next item.

**Example (Claude Code):** An agent spawning a subagent with `isolation: "worktree"` to make changes in a separate git branch without affecting the main workspace.

### 5. Observation (read-only oversight)

A dedicated agent with broad visibility but no write access. Its responsibility is meta-level — watching how other agents exercise _their_ responsibilities and surfacing insights. Never intervenes directly.

**Responsibility contract:** Permanently read-only by design, not as a temporary limitation. Outputs recommendations into a queue for humans or other agents to review. Giving it write access turns it into another worker and destroys its outsider perspective.

**Tradeoffs:**

- Safe — can't break anything because it can't write
- Sees cross-cutting patterns that no single operational agent could detect
- Value comes from outsider perspective
- Recommendations need a review mechanism to become actionable

**Example:** A tester agent observes query patterns, agent disagreements, and refinement outcomes. Posts typed recommendations ("dedup threshold too aggressive", "missing coverage in domain X").

### 6. Multi-team (federated ownership)

Multiple independent agent teams, each owning a different domain, working on the same project. Teams don't share agents but coordinate through shared artifacts or a project-level state. Each team has its own internal responsibility structure.

**Responsibility contract:** Teams own non-overlapping artifact domains. Cross-team interaction happens through well-defined interfaces (queries, shared schemas), not shared agents.

**Tradeoffs:**

- Scales to complex projects with genuinely different workstreams
- Each team can use different runtimes, models, or schedules
- Coordination overhead — need clear boundaries for who owns which artifacts
- Risk of conflicting changes if artifact boundaries aren't strict

**Example:** A knowledge library team (indexer/librarian/retriever) runs alongside a code analysis team (scanner/reviewer/fixer). Both teams write to the same repo but own different folders. The code team might query the knowledge library's retriever for context, but the teams don't share agents.

**Open question:** Are there real-world production examples of this pattern? Most multi-agent frameworks focus on single-team coordination.

### 7. Swarm (dynamic responsibility)

A pool of agents with overlapping capabilities. Responsibility is assigned dynamically based on availability, specialization, or load. No fixed ownership — agents pick up tasks they're suited for.

**Responsibility contract:** Fluid. A dispatcher/router assigns responsibility per-task. Any agent in the pool can handle any task, so ownership is transient.

**Tradeoffs:**

- Flexible — adapts to variable workloads
- Complex — needs a dispatcher/router and a way to match tasks to capabilities
- Harder to debug — no fixed agent-to-task mapping
- Works best with homogeneous agents (same model, same tools) where any agent can handle any task

**Example:** A pool of retriever agents handling incoming queries. Queries are routed to whichever agent is free. All agents have the same skills and access.

**Contrast with parallel specialization:** Specialization has fixed roles; swarms have fluid roles. Specialization coordinates through shared state; swarms coordinate through a dispatcher.

---

## Trigger Models

How agents decide when to exercise their responsibilities. These are orthogonal to the patterns above — any pattern can use any trigger model.

| Trigger          | Description                                                                                                                                          | Best for                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Event-driven** | Fires in response to a specific event (e.g., `entry:created`). Reactive — work happens when there's something to do.                                 | Real-time processing, cause-and-effect workflows      |
| **Scheduled**    | Runs on a fixed cadence (hourly, daily, weekly). Processes whatever has accumulated.                                                                 | Batch processing, maintenance tasks, periodic reviews |
| **On-demand**    | Invoked explicitly by a user or another system.                                                                                                      | Query interfaces, ad-hoc tasks                        |
| **Hook-based**   | Fires automatically as a post-action trigger — after a tool call, file edit, commit, or deployment. Tightly coupled to the action that triggered it. | Validation, coherence checking, notifications         |
| **Continuous**   | Runs in a loop, polling for changes. Heavier than event-driven but simpler when no event queue exists.                                               | Watching external systems, file watchers              |

**Hooks vs. events:** Hooks are synchronous post-action triggers (the action waits for the hook to complete). Events are asynchronous (the event is posted and the emitter moves on). Hooks are good for validation gates; events are good for decoupled coordination.

---

## Supporting Responsibilities

Beyond the core domain agents, what infrastructure responsibilities do multi-agent systems need?

### Coherence checker

Validates cross-references, structural consistency, and boundary violations after workspace changes. Can be implemented as a hook (fast, shallow, per-edit) or a scheduled agent (deep, periodic).

### Quality gate

Blocks progression unless criteria are met. Could be a checkpoint in a pipeline, a hook on a promotion event, or a skill that other agents call before committing changes.

### Router / dispatcher

Routes work to the right agent based on content, load, or specialisation. Required for swarm patterns; optional for fixed-role teams.

### Notification bridge

Connects agent outputs to human attention channels (Slack, email, dashboard). Runtime-specific — implemented as scripts or hooks.
