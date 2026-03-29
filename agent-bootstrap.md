# Agent Bootstrap

A reference for bootstrapping agents in new projects. Point an agent here to give it access to design principles, planning frameworks, and working examples.

> **Note:** This file can itself become an agent — point it at another project to review its structure, plan improvements, or bootstrap a new workspace from scratch.

## Planning

- [Planning Guide](inbox/planning-guide.md) — a thinking framework for planning any kind of work. Three perspectives: Purpose (why/what), Structure (decomposition/dependencies), Motion (prioritization/execution).

## Agent Design

- [Agent Composition](inbox/agent-composition.md) — rules for structuring agents, skills, and teams. Agents are defined by judgment (personas or workflows), skills by determinism (bounded transformations).
- [Design Principles for LLM-Native Pipelines](inbox/agentic-design-principles.md) — core principles: prose as program, externalized state, layered ownership, contracts over coupling, compression boundaries.
- [Agent Flattening](inbox/agent-flattening.md) — how to restructure standalone agents for team/subagent roles. Context control, delegation, splitting.
- [Responsibility Patterns](inbox/agent-responsibility-patterns.md) — patterns for dividing work across agents: shared state, parallel specialization, pipeline, delegation, observation, multi-team, swarm.
- [Workspace Orchestration](inbox/workspace-orchestration.md) — architecture for multi-workspace agent systems. Orchestrator/workspace/runtime three-layer model.
- [Useful Custom Agents](inbox/useful_agents.md) — catalog of custom agents worth building for Claude Code, across domains.

## Examples

- [claude-stalk](https://github.com/zzyy-gh/claude-stalk) — a working Claude Code project to reference for agent setup and structure.
- [vc-deep-research](https://github.com/zzyy-gh/vc-deep-research) — a research-oriented Claude Code project demonstrating agentic workflows.
