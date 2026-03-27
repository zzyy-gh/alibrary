---
id: b1bfe40d-4a6b-4099-a71a-0495aafa0e76
title: Dynamic Workspace Orchestration
source_type: documentation
artifact_path: inbox/workspace-orchestration.html
summary: An architecture reference for multi-workspace AI agent systems covering the
  orchestrator/workspace/runtime three-layer model. Defines the workspace coherence
  invariant (workflow and outputs must stay paired), decision rules for routing tasks
  (declared cross-refs are safe, undeclared refs trigger a pause or new workspace
  spin-up), and compares the design against industry patterns such as supervisor/worker,
  workspace isolation, and context separation via subagents.
tags:
- orchestration
- multi-agent
- architecture
- agents
- coordination
created_at: '2026-03-27T05:11:09Z'
created_by: unknown
maturity: summary
---

Interactive HTML document covering dynamic workspace orchestration for multi-workspace AI agent systems. The document presents an architecture where an orchestrator lives outside all workspaces and routes agent sessions into purpose-built workspaces, each pairing a workflow (CLAUDE.md + skills + agents) with its outputs.

## Key concepts

**Three-layer architecture**
- Orchestrator: has its own CLAUDE.md for orchestration behaviour, a workspace registry, and workflow templates. Produces no mission outputs.
- Workspace: pairs a workflow (how work is done) with outputs (what was produced). The pairing is the coherence guarantee.
- Runtime: an ephemeral agent session — started by the user directly (`cd workspace && claude`) or by the orchestrator via `query(cwd=...)`. The same rules apply regardless of who started it.

**Workspace coherence invariant**
A workspace is a paired guarantee — the workflow guidelines and the outputs always belong to each other. If a task would break that pairing, spin up a new workspace rather than contaminate an existing one.

**Cross-referencing vs contamination**
- Declared cross-references (a workspace's workflow explicitly lists skills from other workspaces) are safe by design. Outputs are governed by a workflow that accounts for the dependency.
- Undeclared references (an agent needs skills not listed in the current workspace's workflow) are a coherence violation. The orchestrator detects and pauses before proceeding.

**Decision rules**
1. Declared refs → run confidently.
2. Undeclared refs → pause and ask.
3. Mismatch → spin up a new purpose-built workspace with a merged workflow.

**Industry validation**
Aligns with: supervisor/worker pattern (Azure, AWS Bedrock, Google ADK, LangChain), workspace isolation, context separation via subagents, simple composable patterns. Distinctive contributions: coherence invariant (stronger than conflict prevention), declared vs undeclared reference detection, dynamic workspace creation on violation, orchestrator-as-workflow-only entity. Identified gaps: observability/logging, error handling/retry, cost management, workspace versioning.

**Interactive scenarios** (in the HTML)
Four animated scenarios: pure workspace run, cross-referencing workspace, undeclared reference detected, new workspace spun up.
