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

Rules for structuring agents, skills, and teams. Companion to `design-principles.md` (foundational principles), `agent-flattening.md` (technique for making agents team-ready), and `responsibility-patterns.md` (how to divide work across agents).

## 1. Agents as Personas

- **Role-based, not workflow-based:** Define agents by their specialty (e.g., security-expert, frontend-dev), not by their position in a pipeline.
- **Not team-ready by default:** A standalone agent may use forked skills or assume full context — things that break in teammate/subagent roles. Agents need flattening before they can work in teams (see `agent-flattening.md`).
- **Instructional:** Use agent files to define how the agent thinks and its definition of done — not how it's orchestrated.

## 2. Teammates as Coordinated Peers

- **The power-up:** Teammates are spawned agents that can communicate with each other via a shared mailbox or task list — unlike plain subagents, which run in isolation.
- **The ceiling:** They are still leaves on the tree — they cannot spawn further subagents. Coordination must happen at the orchestrator level.

## 3. Skills as Tasks

- **Task vs. personality:** If it's a specific action (e.g., `/deploy`, `/scan`), make it a skill. If it's a way of thinking, make it an agent.
- **The fork rule:** Only use context forking for massive, independent tasks that need a clean context or a different model (e.g., switching to a larger model for a complex refactor).
- **Composability:** Keeping most skills inline (non-forked) allows any agent — orchestrator, teammate, or subagent — to use them without restriction. Forked skills are only safe when invoked by the orchestrator (the top-level agent managing the workflow) — teammates and subagents can't execute the fork. If a persona needs a forked skill and might run in a team, that skill must be extracted out via flattening (see `agent-flattening.md` §Forked Skills).

## 4. The No-Nesting Rule

- **Never initiate subagents from within an agent's prompt.**
- **Why:** Workspace hygiene — keeping orchestration at one level makes the system easier to reason about, debug, and compose. An agent can call a skill that happens to be forked, but that's the skill's concern, not the agent's.
- **Still need flattening:** The no-nesting rule keeps agents clean, but agents with forked skills still need flattening before they can work as teammates or subagents (see `agent-flattening.md`).

## 5. Non-Overlapping Ownership

Each agent owns a distinct process. If two agents could handle the same trigger, one of them shouldn't exist. Merge them or sharpen the boundary until there's exactly one place to look when a workflow breaks and exactly one place to change when it needs to evolve.

The same applies to skills. Each skill owns a distinct transformation. If two skills could handle the same input, merge them or sharpen the contract until there's exactly one skill for any given task.
