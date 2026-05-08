---
id: 62f4e94d-6d76-4cb2-8ac4-d530ef3af303
title: Epistemic Mediator Framework
source_url: https://github.com/zzyy-gh/mediator
source_type: documentation
tags:
- decision-making
- epistemology
- framework
- knowledge-representation
- active-inference
created_at: '2026-05-08T02:59:07Z'
created_by: unknown
maturity: summary
---

# Framework

A language-native epistemic mediator. Sits between intent, world, and self. Domain-free. Knows only how knowledge bounds, fuzzes, cascades, and iterates. Optimizes the next step — zoom in, zoom out, clarify, probe, execute, reflect — until commitment is warranted.

Built on three prior threads: structure-and-movement (reality-framework), fuzziness-and-ego (nature-of-being), and unified iteration (this synthesis).

---

## 1. Purpose

Help a user move from unclear intent and incomplete world-knowledge to a warranted next action — one step at a time, with reasoning preserved.

The framework does not decide. It scaffolds. The user (and their taste) remains the principal.

General-purpose: the same engine applies to investing, research, medicine, career, design — domain knowledge lives in the user's graph, not in the framework. The framework itself is co-built with the user: seed primitives, ontology, and operation set emerge from contact with real decisions, not handed down. Load-bearing parts are §1–3; §4 onward illustrate one workable shape, not prescription.

---

## 2. Core ontology

Two primitives and one modifier. Everything else composes from these.

### Structure (S-node)
Any bounded knowledge cluster: a belief, a hypothesis, a goal, a constraint, a scope, a taste pattern, the framework itself.

Properties:
- confidence
- resolution
- bandwidth
- provenance (where it came from)
- reversibility-cost-to-change
- fuzz-halo (residual uncertainty not captured by confidence alone)

### Movement (M-node)
Any operation that activates or reshapes structure: a question, an experiment, a decision, a reflection, a learning step.

Properties:
- target (which S-node)
- reversibility
- latency
- layer (object, method, or meta)
- fuzz-halo

### Fuzziness
Inherent property of every S-node and M-node. Boundaries are never perfectly sharp. Fuzziness is not noise — it is the substrate where reframing and discontinuous leaps live. The framework preserves fuzz until decision-collapse forces commitment.

### Relations
- **activates** — M reads S
- **reshapes** — M writes or modifies S (including self)

---

## 3. The three poles

The framework mediates between three poles, not two. Each pole is a region of the user's graph.

```
        INTENT                WORLD
          \                    /
           \                  /
            \                /
             FRAMEWORK (mediator)
                  |
                  |
                SELF (ego, taste, history)
```

- **Intent** — what the user wants. Often fuzzy. Probed by intent-probes.
- **World** — what is. Probed by world-probes (data, experiment, expert).
- **Self** — who is asking. Capability, taste, track record, blind spots. Probed by self-probes.

Many decisions stall not because intent or world is unclear, but because the self pole is unclear. Self-probing is a first-class move.

---

## 4. The operation set

At its purest, the framework is a small set of domain-free operations on structure. Example seed set:

1. **Bound** — define an S-node.
2. **Connect** — relate two S-nodes.
3. **Probe** — generate a question targeting fuzziness (intent, world, self, or **prior art** — field literature, tools, methods, what has already been tried). External lookup is first-class, not afterthought.
4. **Collapse** — commit to a specific value (decision).
5. **Reframe** — re-cut existing structure differently.
6. **Zoom** — change resolution, in or out.
7. **Compose** — combine S-nodes into a larger one.
8. **Decompose** — split an S-node into parts.
9. **Test** — apply structure against outcome or contradiction.
10. **Update** — reshape structure given new evidence.
11. **Reflect** — apply any of the above to the framework itself.

Plan, execute, reflect are not separate phases. They are all movements on structure. They differ only in continuous properties — reversibility, resolution, target layer. Same operation class, different targets.

---

## 5. The optimization step

At every step, the framework selects the next operation by trading off two things (Active Inference framing):

- **Epistemic value** — expected reduction in fuzziness.
- **Pragmatic value** — expected progress toward intent.

Probes dominate while fuzz is high; execution dominates once expected information gain falls below cost-of-asking. That crossover is the stop rule — commit and act.

**Feasibility gate** — before Collapse, check path-existence: capability (Self) × constraints (World) × budget (Intent). If any fail, route to Reframe or Probe instead of forcing commit. Possible is not assumed; it is verified.

---

## 6. Self-iteration

The framework includes itself as an S-node. It can be reshaped by movements. Three layers of iteration:

1. **Object level** — beliefs update from evidence (Bayesian-shaped).
2. **Method level** — how updates happen updates (meta-learning).
3. **Meta level** — how the framework decides how to update itself updates (constitution amendment).

Iteration runs at two cadences:
- **In-task** — Reflect mid-decision: swap operations, retune resolution, patch a local heuristic, register a new blind spot. Lightweight, no ledger.
- **Cross-task** — amendment process below: ledger-tracked, calibration-tested, slower. In-task patches that recur are promoted to cross-task amendments.

Nothing is strictly invariant. Every part can change. Tiers, processes, and practices that keep iteration disciplined:

- **Constitution** — highest-gated tier. User-as-principal, provenance preservation, append-only ledger, human-in-loop at Collapse. Changes here require explicit user input, impact analysis, and propagation across the workspace.
- **Amendments** — lighter-gated tier. Primitives, heuristics, schemas, prompts. Proposed change → tested on historical decisions → calibration delta measured → accept or reject.
- **Propagation** — every accepted change scans the workspace for dependents (system prompt, README, schemas, ledger conventions, related amendments) and either updates them or surfaces them for the user to update. No silent drift between core and dependents.
- **Triggers** — changes fire only on calibration drift, repeated scope misses, new domain, taste shift, or external regime change. No churn without trigger.
- **Shadow registry** — known blind spots, probed regularly. Without adversarial probe, the framework drifts into ego-confirmation.

---

## 7. Taste

Taste is the user's compressed judgment about which scopes and hypotheses are worth attention. It is the moat — generic framework plus this user's taste equals something only this user can run.

Taste cannot be fully extracted by interview. It is built by **revealed preference** — log decisions, what was considered, what was dismissed, what was chosen, why. A model fits to this log over months and mirrors the user's leaning at scale.

Taste is private. Framework is shareable. The split is intentional.

---

## 8. Grounding

The framework needs two anchors to avoid drift:

- **External grounding** — outcome ledger. Real-world feedback. Calibration scores. Was the prediction right? Did the action work? Without this, the framework Goodharts itself.
- **Internal grounding** — coherence with constitution and existing graph. Does new structure integrate without contradiction? Without this, the framework becomes reactive and incoherent.

Tension between the two is productive. Neither alone suffices.

---

## 9. Anti-patterns to watch

- **Premature ontology** — perfect primitives before any use. Counter: dogfood week one on a real decision.
- **Framework-of-frameworks trap** — meta upon meta, no action. Counter: every primitive must reach a concrete decision within three hops.
- **Completeness obsession** — try to subsume every prior framework. Some contradict. Pick stance.
- **Tool sprawl** — features that no real pain demanded.
- **Probe-paralysis** — keep asking, never commit. Counter: stop rule above.
- **Mediator-as-oracle** — user treats framework as authority. It is a lens, not a verdict.
- **Premature collapse** — force fuzz into crisp values too early. Loses the substrate where leaps happen.
- **Empty-elegance** — beautiful but unpopulated. Ship with bootstrap templates.

---

## 10. Build path

1. **Week 1-2** — pick one live decision. Represent as S-nodes and M-nodes only. No other vocabulary. Note where the model strains.
2. **Month 1** — codify primitives into a markdown plus YAML schema. Minimal CRUD: add S-node, add M-node, link them.
3. **Month 2** — LLM layer. Natural language in, structured nodes out. User talks; system structures.
4. **Month 3** — calibration layer. Predictions logged, outcomes scored, feedback to taste model.
5. **Month 4-6** — second domain. Force generalization. Refactor primitives if they leak.
6. **Month 6+** — taste model. Fine-tune small model on the decision log, or RAG over it.
7. **Year 2+** — share framework, keep taste private.

If primitives leak in case one, iterate them.

---

## 11. Agent setup

Use this README as reference. Each project builds its own setup — file layout, tool surface, and amendment cadence are tuned to the project. Concrete examples will follow.

Guiding split, mirroring §6: bake the highest-gated tier (constitution, poles, operations, stop rule, feasibility gate, cadence) into the system prompt as the reflex layer; keep the lighter-gated rest (amendments, ledger, registries, taste, domain notes) as files the agent reads on demand. Agent writes to files, never to its own prompt. Constitution edits require explicit user input plus a propagation pass across all dependent files. Amendments override the README on conflict.

---

## 12. Theoretical lineage

Closest single match: **Active Inference / Free Energy Principle (Friston)**. Mathematical formalization of unified epistemic-plus-pragmatic step selection.

Closest single read: **Pólya — How to Solve It**. Practical, short, generalizes immediately.

Other ancestors worth knowing:
- Bounded rationality and satisficing (Simon)
- Adaptive toolbox (Gigerenzer)
- Ill-structured problems (Simon, Newell)
- OODA and Destruction & Creation (Boyd)
- Bayesian experimental design
- Exploration vs exploitation (RL, bandits)
- Pragmatism and abduction (Peirce, Dewey)
- Conjectures and refutations (Popper)
- Research programmes — hard core and protective belt (Lakatos)
- Madhyamaka emptiness (Nāgārjuna) — fuzziness lineage
- Process philosophy (Whitehead) — structure as frozen movement
- Requisite variety (Ashby)
- Causal inference (Pearl) — when committing to a resolution
- Tacit knowledge (Polanyi) — taste lineage
- Pattern language (Alexander)
- ReAct, Tree of Thoughts, Constitutional AI — modern AI substrate
- Category theory — formal kin (objects, morphisms, composition)

White space, not yet integrated by any of the above:
- Personal taste as first-class.
- Language as primary substrate, not math or code.
- Human-in-loop as design center.
- Fuzziness preserved across steps.
- Self-iteration of framework itself with ledger.

---

## 13. One-line summary

The framework is **epistemic mediation, made operational** — a small set of domain-free operations on structure, executed under preserved fuzziness, scoped by the user's taste, grounded by outcome, and capable of reshaping itself.
