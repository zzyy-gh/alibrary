---
id: c5ca653b-0912-4136-b474-135239469d2f
title: "Multi-Agent Responsibility Patterns"
maturity: summary
summary: >
  Seven patterns for dividing work across agents -- shared state, parallel specialization, pipeline,
  delegation, observation, multi-team, and swarm -- each with distinct coordination contracts.
  Five trigger models (event-driven, scheduled, on-demand, hook-based, continuous) determine when
  agents act. Supporting roles include coherence checkers, quality gates, routers, and notification bridges.
tags:
  - responsibility-patterns
  - multi-agent
  - coordination
  - shared-state
  - pipeline
  - delegation
  - observation
  - swarm
  - trigger-models
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
    reason: cataloguing inbox/responsibility-patterns.md
---

This nugget captures seven structural patterns for dividing responsibilities across multiple agents, regardless of framework or runtime.

**Shared state (implicit handoff)** is the simplest pattern: agents own non-overlapping responsibilities and coordinate by reading artifacts left by others on a shared filesystem or database. No direct communication is needed. This works well when responsibilities are distinct and real-time coordination is unnecessary.

**Parallel specialization** places multiple agents with complementary roles working concurrently toward the same goal. Each owns a non-overlapping slice of the problem space. High throughput, but requires clean separation of concerns and a coordination layer to prevent conflicts.

**Pipeline (sequential handoff)** chains agents in sequence where each stage owns one transformation and hands off via a known artifact path. Clear data flow and per-stage optimization, but bottlenecked by the slowest stage.

**Delegation (parent-child)** has a parent agent delegate subtasks to children in isolated contexts. Children have no awareness of the broader pipeline and write output to known locations. Limited to one level of depth -- children should not spawn their own children.

**Observation (read-only oversight)** gives a dedicated agent broad visibility but no write access. It watches how other agents exercise their responsibilities and surfaces meta-level insights. Its value comes from the outsider perspective that write access would destroy.

**Multi-team (federated ownership)** coordinates multiple independent agent teams, each owning a different domain. Teams interact through well-defined interfaces rather than shared agents, enabling different runtimes, models, or schedules per team.

**Swarm (dynamic responsibility)** uses a pool of agents with overlapping capabilities where a dispatcher assigns work dynamically based on availability or load. Unlike parallel specialization's fixed roles, swarm roles are fluid and transient.

Orthogonal to these patterns, five trigger models determine when agents act: event-driven (reactive to specific events), scheduled (fixed cadence), on-demand (explicit invocation), hook-based (synchronous post-action triggers), and continuous (polling loops). Hooks are synchronous gates; events are asynchronous coordination.

Supporting responsibilities round out multi-agent systems: coherence checkers validate structural consistency, quality gates block progression unless criteria are met, routers dispatch work to the right agent, and notification bridges connect agent outputs to human attention channels.
