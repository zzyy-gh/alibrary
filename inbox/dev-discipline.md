---
id: cdbb4b7f-9d5b-41af-a035-a7582c8380d0
title: Dev Discipline
source_type: manual
tags:
  - planning
  - execution
  - patterns
  - testing
  - reference
created_at: "2026-04-21T03:11:00Z"
created_by: unknown
maturity: summary
---

# Dev Discipline

This applies to everything that touches code — new features, fixes, improvements, small changes. Follow in order. Don't skip steps.

---

## Principles

**The spec is the plan.** The spec sets direction; pseudocode fills the gaps. Together they form the complete design. Code, comments, tests, and interface definitions must stay in sync with both. Implement faithfully — no additions beyond what the spec and pseudocode describe.

**Proportionality.** For trivial changes — obvious, reversible, well-scoped — Steps 1–4 can be brief or collapsed. Steps 5–6 always apply in full.

**Confirmation gates.** After Steps 2 and 4, present to the user and get confirmation before proceeding.

**Feedback loops.** Development isn't linear. If a later step reveals a problem from an earlier one, loop back to the right step rather than working around it inline.

**Escalate, don't redesign.** If the spec or plan turns out to be wrong, infeasible, or contradictory at any point, stop and ask. Don't redesign unilaterally.

---

## Step 1 — Plan

Review the spec for soundness: contradictions, incoherence, and feasibility. If something is off, stop and ask before going further.

Identify every file that needs to be created or changed. For each, write its top-level comment: what it does, why it exists, how it fits. Where the spec is silent, fill in the detail — but stay true to its intent. Every file except `__init__.py` gets at least a top-level comment.

Check for existing solutions — external libraries, frameworks, established patterns, or code already in the repo — before deciding what to build. Reinvention is a last resort.

Apply clean code principles and established best practices: clarity, single responsibility, DRY, appropriate abstractions.

If the work touches connected architecture where a broader improvement is clearly warranted — performance, structural clarity, code hygiene, better framework fit — note it and present it as an option. Only raise it where the benefit is significant and worth the disruption.

---

## Step 2 — Check the plan

- Every spec requirement is accounted for. No silent gaps.
- Nothing contradicts the spec.
- Where the plan filled a spec gap: is the addition sound and consistent with the spec's intent?
- Failure modes are considered: missing data, service errors, unexpected input.
- Remaining edge cases are noted, not silently decided.

---

## Step 3 — Write pseudocode and comments

Fill in detailed pseudocode for non-trivial files: business logic, evaluation, data transformation, external integrations. Simple files may need only their top-level comment. Pseudocode must be specific enough that implementation is mechanical.

Include test design alongside the pseudocode: what scenarios to cover, what boundaries and edge cases matter.

---

## Step 4 — Check pseudocode

- Every file's pseudocode matches its top-level comment and the confirmed plan.
- Data flows and interfaces are consistent across files — no mismatches at the boundaries.
- Every edge case from Step 2 is handled in the pseudocode.
- Test designs are complete and cover meaningful boundaries.
- Nothing has been added beyond the confirmed plan.

---

## Step 5 — Implement

Implement according to the pseudocode and write the tests designed in Step 3. Run all tests and fix every failure before considering the step done. Integration tests hit real external dependencies — don't mock at the integration level unless the dependency is unavailable. Configuration values driving logic (thresholds, cutoffs, limits) come from config files — never hardcoded inline.

---

## Step 6 — Check implementation

- Everything matches the spec and pseudocode: code, comments, tests, interface definitions.
- Output is traceable to sources.
- Boundaries are tested: values at thresholds, empty inputs, timeouts.
- No scope creep. Nothing more than what the spec and pseudocode describe.
- All properties and metric/dict keys are complete and consistent — when something is added or changed, verify nothing is silently missed elsewhere.
