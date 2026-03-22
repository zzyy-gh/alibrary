---
id: 79f15266-0386-4215-9458-f6440eba93e8
title: "Agent Composition: Structuring Agents, Skills, and Teams"
maturity: summary
summary: >
  Agent composition defines five structural rules: agents are role-based personas (not workflow positions),
  teammates are coordinated peers that cannot spawn sub-workers, skills are discrete tasks (not personalities),
  nesting is forbidden to keep orchestration flat, and ownership must be non-overlapping across both agents and skills.
tags:
  - agent-composition
  - skills
  - orchestration
  - no-nesting
  - non-overlapping-ownership
  - teammates
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
    reason: cataloguing inbox/agent-composition.md
---

Agent composition provides the structural rules for how agents, skills, and teams relate to each other in a multi-agent system. Five principles govern the design.

First, agents are personas defined by specialty (security-expert, frontend-dev), not by their position in a workflow. An agent file describes how the agent thinks and its definition of done -- not how it is orchestrated. Agents are not team-ready by default; they may rely on forked skills or assume full context, both of which break in team roles and require flattening before collaboration.

Second, teammates are spawned agents that can communicate with each other via shared mailboxes or task lists, giving them coordination capability that plain subagents lack. However, teammates remain leaves on the execution tree -- they cannot spawn further subagents, and all coordination must happen at the orchestrator level.

Third, there is a clean distinction between skills and agents: if something is a specific action (deploy, scan), it should be a skill; if it is a way of thinking, it should be an agent. Most skills should remain inline (non-forked) so any agent can use them without restriction. Forked skills -- those requiring a clean context or different model -- are only safe when invoked by the orchestrator, since teammates cannot execute forks.

Fourth, the no-nesting rule prohibits initiating subagents from within an agent's prompt. This keeps orchestration at a single level for easier reasoning, debugging, and composition. An agent may call a forked skill, but that is the skill's concern, not the agent's.

Fifth, ownership must be non-overlapping: each agent owns a distinct process, each skill owns a distinct transformation. If two agents or two skills could handle the same trigger or input, they should be merged or their boundaries sharpened until there is exactly one owner for any given responsibility.
