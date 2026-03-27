---
id: e7ffcd64-fec7-4baf-b6f0-7bbe93b14cbb
title: Design Principles for LLM-Native Pipelines
source_type: manual
tags:
- llm-native
- agentic-design-principles
- pipelines
- architecture
created_at: 2026-03-22 00:00:00+00:00
created_by: migration
maturity: summary
---

# Design Principles for LLM-Native Pipelines

Core concepts for building multi-step workflows where an LLM is the runtime, not a component. Original in arrangement, derivative in every other way.

## 1. Prose as program

The system has no application code. Markdown instruction files define what each unit does, what it takes as input, and what it produces. The LLM interprets and executes them directly. This eliminates dependency management, build steps, and framework bugs -- the entire codebase is human-readable prose.

This is the foundational bet: the LLM is capable enough to be the runtime, so the "code" can be natural language. Everything else in this document builds on that assumption.

## 2. Externalized state

The single most consequential design decision: state lives on disk, not in the LLM's context window. Units don't pass data through memory or return values -- each stage writes a named output file, and the next stage reads it. Everything else flows from this:

**Functional composition.** With state externalized, units behave like pure functions: input files in, output files out, no mutation of shared state. The pipeline becomes a chain of composable transformations wired through the filesystem. This isn't strictly pure -- agents carry context windows, and units have side effects (network calls, file writes). But the *intent* is functional: keep units stateless relative to each other, compose by wiring outputs to inputs.

**Parallelism.** When units write to separate directories and share no in-memory state, concurrency is free. Fan out one subagent per independent item; serialize only where there's a real data dependency. The result is a DAG that runs as wide as the data allows. This isn't an optimization -- it's a structural property of the design.

**Debuggability.** Every intermediate file is a checkpoint. When output is wrong, inspect the input and output of each stage to isolate the break. Re-run any single stage by pointing it at existing inputs -- no need to replay the full pipeline.

**Navigability.** Use predictable, self-describing naming conventions: timestamps in folder names, slugified identifiers, numbered file prefixes for processing order. When the layout is consistent, you can reason about the system with `ls`. The output directory *is* the audit trail -- no database, no log aggregator.

## 3. Layered ownership, flat execution

The documentation hierarchy mirrors the responsibility hierarchy. Each layer owns exactly one concern: project files describe structure, agent files describe processes, skill files describe transformations. Keep orchestration flat — the orchestrator spawns workers, workers don't spawn their own workers.

The same principle applies to the filesystem: every folder should have a uniform sharing scope. Shared, reusable artifacts live in known shared folders; artifacts specific to a session or run stay local to that subfolder. If a folder mixes shared and local concerns, split it.

For agent composition (personas, teammates, skills, forked skills, no-nesting) see `agent-composition.md`. For making agents team-ready, see `agent-flattening.md`.

## 4. Contracts over coupling

Units are interchangeable as long as they honor the input/output contract. This shows up in two ways:

**Shared units, multiple wirings.** Different workflows (batch runs, ad-hoc single items, scheduled monitoring) reuse the same skill units, wired differently by different agents. The skill doesn't know or care which agent called it -- it reads its input file and writes its output file. This avoids duplicating logic while supporting varied usage patterns.

**Templates and examples as specifications.** Ship concrete examples of expected output alongside the unit that produces it. LLMs generate more consistent output when they have a real example to match, not just abstract formatting rules. The example *is* the contract. When the example changes, the output changes -- no code to update.

## 5. Compression boundaries

When a pipeline stage produces output that is orders of magnitude smaller than its input, treat that as a deliberate compression boundary. Stages downstream of the boundary operate on the compressed artifact and never see the raw source.

This is the LLM-specific corollary to externalized state. Disk solves the problem of passing data between units without bloating the orchestrator's context. Compression boundaries solve the problem of working with data that is too large even for individual units. By designing explicit reduction points into the pipeline, you can process arbitrarily large or numerous inputs in batch without exceeding any single agent's context window.

## 6. Explicit failure handling

When a stage can fail transiently (external APIs, missing data that appears later), model retry as a first-class concept with its own state file. Track what failed, why, and whether to retry -- separate from the main pipeline flow.

This follows naturally from externalized state: retry state is just another file on disk, inspectable and editable. It avoids re-running successful stages and gives the user visibility into what's pending without requiring them to parse logs or re-trigger the entire pipeline.
