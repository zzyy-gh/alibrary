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

The documentation hierarchy mirrors the responsibility hierarchy. Each layer owns exactly one concern:

- **Project file** (e.g., CLAUDE.md) is the map. It describes structure, conventions, and culture. It never orchestrates work or spawns subagents.
- **Agent files** describe processes. They are the *only* place that manages subagents and sequences units. When a workflow breaks, this is where you look.
- **Skill files** are the most modular units. They describe a single transformation with clear inputs and outputs. They never call other skills. A skill may spawn a subagent internally to contain heavy content, but this is isolation, not orchestration.

The same principle applies to the filesystem: every folder should have a uniform sharing scope. Shared, reusable artifacts live in known shared folders; artifacts specific to a session or run stay local to that subfolder. If a folder mixes shared and local concerns, split it -- when you need something reusable, there should be exactly one place to look.

This strict layering makes the system safer to scale. Adding a skill can't introduce orchestration complexity. Adding an agent can't pollute project-level docs.

**Agents are flat and non-overlapping.** Subagents cannot spawn their own subagents, so nesting would break at runtime -- but this is a feature, not a limitation. A flat execution model keeps the mental model simple: one agent, one pipeline, one level of delegation. When you need multi-agent coordination, compose at the team level with independent agents running in parallel. Ownership matters just as much as structure. Each agent owns a distinct process; if two agents could handle the same trigger, one of them shouldn't exist. Merge them or sharpen the boundary until there's exactly one place to look when a workflow breaks and exactly one place to change when it needs to evolve.

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
