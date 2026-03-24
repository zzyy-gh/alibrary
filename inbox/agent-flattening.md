---
id: 5d890b18-69b7-4042-be59-3b0c54e2c417
title: Agent Flattening
source_type: manual
tags:
- agents
- flattening
- teams
- orchestration
created_at: 2026-03-22 00:00:00+00:00
created_by: migration
maturity: summary
---

# Agent Flattening

Companion to `agent-composition.md` (the rules), `design-principles.md` (foundational principles), and `responsibility-patterns.md` (how to divide work across agents).

Flattening is the process of restructuring a standalone agent so it can work as a teammate or subagent. A standalone agent may rely on forked skills, assume full context, or hardcode orchestration — all things that break in team roles, where the agent can't spawn subagents and has a constrained context window.

**What to flatten:**

- **Forked skills** — extract them; the orchestrator handles them as separate subagent invocations
- **Context assumptions** — the agent can't assume it has the full picture; use intermediate storage to pass state
- **Hardcoded orchestration** — the agent shouldn't spawn workers; that's the orchestrator's job

## Context Control

Before flattening, assess the team's context budget:

- **Context budgeting:** Analyse personas and skills to ensure no single agent is overwhelmed by too many files or long-winded planning noise.
- **Intermediate storage:** Use a shared directory (e.g., `tasks/`) as a buffer to store state and results outside of the LLM context. This is the key enabler for both delegation and splitting — it decouples agents from each other's context windows.

## Delegation (Teammate Pattern)

Delegation applies when a persona is invoked as a **teammate** — it has an orchestrator it can communicate with. The persona can message the orchestrator, receive instructions, and coordinate with other teammates through a shared mailbox or task list.

- **Role specialization:** Instead of one complex agent, use a team where each persona has a specific role (e.g., Coder vs. Validator) and a clear input/output contract.
- **Escalation protocol:** If a teammate encounters a forked skill or task requiring massive context or capabilities beyond its scope, it escalates by messaging the orchestrator. The orchestrator has full orchestration capability — it can spawn a new specialist peer, invoke a subagent to handle a forked skill, or split the work itself.
- **Autonomous handoffs:** Use a shared task list with dependency tracking so agents can self-claim work as blockers are cleared.

**Not applicable** when the persona is a subagent — subagents can't communicate with an orchestrator or peers. See splitting below.

## Splitting (Subagent Pattern)

Splitting applies when a persona is invoked as a **subagent** — it has no orchestrator to delegate to, no peers to communicate with. Since the subagent can't coordinate on its own, the **orchestrator** (the top-level agent managing the workflow) must split the work as required — breaking context-hungry or parallelizable parts into separate subagent invocations.

**Key difference from delegation:** In delegation, the persona can ask for help. In splitting, the persona can't — so the orchestrator must pre-decompose the work into pieces small enough for isolated subagents.

## When to Use Which

- **Delegation** when the agent needs to coordinate, ask for help, or handle unpredictable work — it can escalate to the orchestrator.
- **Splitting** when the work is fully decomposable upfront and the agent doesn't need to communicate — the orchestrator pre-divides the work into isolated units.

## Forked Skills

Always respect forked skills — separate them out to flatten. A forked skill requires its own context (a clean brain, a different model, or heavy isolated processing). Since teammates cannot spawn subagents, any persona with a forked skill must have that skill extracted and handled by the orchestrator as a separate subagent invocation. Keeping a forked skill inside a teammate breaks the flat execution model.
