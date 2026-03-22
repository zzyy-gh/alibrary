---
id: b9382f47-2117-49b8-bd3a-99939c2dc850
title: "Prose as Program: Designing LLM-Native Pipelines"
maturity: summary
summary: >
  LLM-native pipelines treat the language model as the runtime itself, replacing application code with
  prose instructions. Six principles govern their design: prose as program, externalized state on disk,
  layered ownership with flat execution, contracts over coupling, compression boundaries for large data,
  and explicit failure handling with retry state files.
tags:
  - llm-native
  - pipeline-design
  - externalized-state
  - prose-as-program
  - contracts
  - compression-boundaries
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
    reason: cataloguing inbox/design-principles.md
---

LLM-native pipelines invert the traditional software architecture: instead of embedding an LLM as a component within application code, the LLM becomes the runtime that interprets and executes natural-language instruction files directly. This eliminates build systems, dependency management, and framework-specific bugs in favor of human-readable prose that doubles as the program.

The architecture rests on externalized state as its most consequential decision. Every pipeline stage reads input files and writes output files to disk rather than passing data through memory or context windows. This yields functional composition (units behave like pure functions), free parallelism (no shared in-memory state means concurrency is structural, not an optimization), full debuggability (every intermediate file is an inspectable checkpoint), and navigability (predictable naming conventions make the output directory its own audit trail).

Ownership is layered but execution stays flat: project files describe structure, agent files describe processes, skill files describe transformations, and orchestrators spawn workers without workers spawning their own sub-workers. Units interact through input/output contracts rather than tight coupling -- different workflows can reuse the same skill units with different wirings, and concrete output examples serve as living specifications.

Two additional principles handle scale and failure. Compression boundaries are deliberate reduction points where a stage's output is orders of magnitude smaller than its input, allowing downstream stages to operate on compressed artifacts without exceeding context limits. Explicit failure handling models retry as a first-class concept with its own state file, tracking what failed and whether to retry, separate from the main pipeline flow.
