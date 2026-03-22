---
id: 35be87c5-6f04-47fb-86b6-7f6b5e695454
title: "Agent Flattening: Making Standalone Agents Team-Ready"
maturity: summary
summary: >
  Flattening restructures a standalone agent for team or subagent roles by extracting forked skills,
  removing context assumptions, and eliminating hardcoded orchestration. Two patterns apply: delegation
  (teammate pattern with escalation) and splitting (subagent pattern with pre-decomposed work).
tags:
  - agent-flattening
  - delegation
  - splitting
  - teams
  - context-budgeting
  - forked-skills
quality_score: 0.6
decay_rate: slow
review_by: 2026-09-22
created_at: 2026-03-22T00:00:00Z
updated_at: 2026-03-22T00:00:00Z
created_by: indexer
updated_by: indexer
changelog:
  - timestamp: 2026-03-22T00:00:00Z
    agent: indexer
    action: created
    diff: initial synthesis from raw item
    reason: cataloguing inbox/agent-flattening.md
---

Flattening is the process of restructuring a standalone agent so it can operate as a teammate or subagent within a multi-agent system. Standalone agents often rely on forked skills, assume they have full context, or hardcode their own orchestration -- all of which break when the agent runs in a constrained team role where it cannot spawn sub-workers and operates within a limited context window.

Three things must be flattened: forked skills are extracted so the orchestrator handles them as separate subagent invocations; context assumptions are replaced with intermediate storage (shared directories) that pass state between agents without requiring any single agent to hold the full picture; and hardcoded orchestration is removed since spawning workers is the orchestrator's job, not the agent's.

Before flattening, a context budget assessment is needed. This means analyzing personas and skills to ensure no single agent is overwhelmed, and establishing intermediate storage (e.g., a shared tasks/ directory) as a buffer that decouples agents from each other's context windows.

Two flattening patterns exist for different team structures. The delegation pattern applies when the agent runs as a teammate with an orchestrator it can communicate with. Teammates specialize by role, follow clear input/output contracts, and can escalate when they encounter tasks beyond their scope -- the orchestrator then spawns specialist peers or invokes subagents as needed. Autonomous handoffs through dependency-tracked task lists allow agents to self-claim work. The splitting pattern applies when the agent runs as a subagent with no communication channel. Since the subagent cannot ask for help, the orchestrator must pre-decompose the work into pieces small enough for isolated execution.

The choice between patterns depends on coordination needs: delegation when the agent needs to handle unpredictable work and escalate, splitting when the work is fully decomposable upfront. Forked skills always require extraction regardless of pattern -- keeping them inside a teammate breaks the flat execution model.
