---
id: 4b0495e5-a9cc-49b6-9c8a-db3a12f4cf3c
title: Agent Composition
source_type: manual
tags:
- agents
- composition
- skills
- orchestration
created_at: 2026-03-22 00:00:00+00:00
created_by: migration
maturity: stub
---

# Agent Composition

Rules for structuring agents, skills, and teams. Companion to `agentic-design-principles.md` (foundational principles), `agent-flattening.md` (technique for making agents team-ready), and `agent-responsibility-patterns.md` (how to divide work across agents).

> **Framework context:** The agent/skill/team model here is inspired by and aligned with Claude Code's architecture — agents as AGENT.md files, skills as SKILL.md files, teams as coordinated agent sessions. The underlying patterns (bounded tasks, parallel coordination, externalized state) are common across the multi-agent ecosystem, but the specific framing and terminology follow Claude Code's conventions.

## 1. Agents as Personas or Workflows

- **Judgment is the defining quality:** An agent describes *how to approach work* — whether that's a persona ("think like a security expert") or a workflow ("here's how to catalogue items"). The common thread is judgment: the agent decides what to do next based on what it sees.
- **Personas and workflows are both valid:** A persona-style agent (e.g., security-expert, frontend-dev) brings a perspective. A workflow-style agent (e.g., indexer) orchestrates skills in a sequence that requires decision-making. Both are agents because both exercise judgment.
- **Not team-ready by default:** A standalone agent may use forked skills or assume full context — things that break in teammate/subagent roles. Agents need flattening before they can work in teams.
- **Instructional:** Use agent files to define how the agent thinks and its definition of done — not how it's orchestrated.

## 2. Teammates as Coordinated Peers

- **The power-up:** Teammates are spawned agents that can communicate with each other via a shared mailbox or task list — unlike plain subagents, which run in isolation.
- **The ceiling:** They are still leaves on the tree — they cannot spawn further subagents. Coordination must happen at the orchestrator level.

## 3. Skills as Deterministic Work

- **Determinism is the defining quality:** A skill is a bounded transformation — input in, output out. Given the same input, it should produce roughly the same output. Skills don't decide *what* to do, only *how* to do this one thing. If the unit requires judgment about what to do next, it's agent work.
- **The litmus test:** Tag assignment is a skill (input item, output tags). Frontmatter validation is a skill (schema check, repair). Cross-source synthesis is agent work (requires judgment about what connects and what matters).
- **Forking is an execution concern:** Whether a skill runs inline or in a forked context (clean brain, different model) is a runtime detail — Claude Code handles context isolation. It doesn't change what the skill *is*. Keep most skills inline for composability; fork only when the skill genuinely needs a separate context window.

## 4. The No-Nesting Rule

- **Never initiate subagents from within an agent's prompt.**
- **Why:** Workspace hygiene — keeping orchestration at one level makes the system easier to reason about, debug, and compose. An agent can call a skill that happens to be forked, but that's the skill's concern, not the agent's.
- **Still need flattening:** The no-nesting rule keeps agents clean, but agents with forked skills still need flattening before they can work as teammates or subagents (see `agent-flattening.md`).

## 5. Non-Overlapping Ownership

Each agent owns a distinct process. If two agents could handle the same trigger, one of them shouldn't exist. Merge them or sharpen the boundary until there's exactly one place to look when a workflow breaks and exactly one place to change when it needs to evolve.

The same applies to skills. Each skill owns a distinct transformation. If two skills could handle the same input, merge them or sharpen the contract until there's exactly one skill for any given task.
