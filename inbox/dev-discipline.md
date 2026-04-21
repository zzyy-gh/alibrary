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
created_at: '2026-04-21T03:11:00Z'
created_by: unknown
maturity: summary
---

# Dev Discipline

This applies to everything that touches code — new features, fixes, improvements, small changes. Follow in order. Don't skip steps. For small changes, Steps 1–2 may be brief or skipped; the rest always applies.

---

## The spec is the plan

Implement the spec faithfully. Don't re-plan or redesign. The spec sets direction; pseudocode fills the gaps. Together they form the complete design. Code, comments, tests, and interface definitions must stay in sync with both. If the spec contradicts itself, stop and ask.

---

## Step 1 — Create files with pseudocode and comments

Create each file with its top-level comment and pseudocode in place. Where the spec is silent, fill in the detail — but stay true to its intent.

Every file except `__init__.py` gets at least a top-level comment (what it does, why it exists, how it fits). Reserve detailed pseudocode for non-trivial files: business logic, evaluation, data transformation, external integrations.

---

## Step 2 — Check pseudocode

- Every spec requirement has a code path. No silent gaps.
- Nothing contradicts the spec. Resolve against the spec.
- Where pseudocode filled a spec gap: is the addition sound and consistent with the spec's intent?
- Failure modes are handled: missing data, service errors, unexpected input.
- Remaining edge cases are noted, not silently decided.

---

## Step 3 — Implement

Before writing, check if an existing solution covers the need — a library, a pattern, code already in the repo. Copy or adapt carefully, weighing convenience, overhead, bulkiness, customizability, and reliability. Reinvention is a last resort.

**Critical code: write tests first, confirm they fail, then implement.**

Critical means: logic producing verdicts, scores, or classifications with real consequences; logic assembling output attribution or provenance.

All other code: write tests alongside. Integration tests hit real external dependencies — don't mock at the integration level unless the dependency is unavailable. Configuration values driving logic (thresholds, cutoffs, limits) come from config files — never hardcoded inline.

---

## Step 4 — Run tests

Fix all failures before continuing.

---

## Step 5 — Check implementation

- Everything matches the spec and pseudocode: code, comments, tests, interface definitions.
- Output is traceable to sources. Every claim is attributable.
- Boundaries are tested: values at thresholds, empty inputs, timeouts.
- No scope creep. Nothing more than what the spec and pseudocode describe.
- All properties and metric/dict keys are complete and consistent — when something is added or changed, verify nothing is silently missed elsewhere.
- Nothing surprising left unexplained.
