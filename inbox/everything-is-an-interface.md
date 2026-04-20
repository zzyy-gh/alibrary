---
id: 6aae4138-a8c4-4179-aa16-8813785092c9
title: Everything is an interface
source_type: manual
tags:
- architecture
- composition
- abstraction
- framework
- patterns
created_at: '2026-04-20T02:06:25Z'
created_by: unknown
maturity: summary
---

# Everything is an interface

A foundation for composable systems.

---

## The idea

Anything that takes in information and produces information is an **interface**.

A sensor. An algorithm. A dataset. A belief. An agent. A display. A process. A person.

These are all interfaces. They differ on properties, not on kind.

This is the same move Unix made with files. A keyboard, a disk, a network socket, and a printer are all "files" — accessed through the same operations. The diversity of the physical world is collapsed into one abstraction. What changes is not what they *are* but how they *behave*.

We do the same thing, one level up. Everything that transduces reality into understanding is an interface. What changes between them is properties.

---

## An interface

```
interface:
  id: anything unique
  description: what does it do, in one line
  properties: { ... }
```

Properties are a flat bag of key-values. Nothing is required. Add what helps someone — human or AI — understand and use this interface. Omit what doesn't.

### Useful properties (not required)

Four continuous properties describe any interface and are useful for comparison and reasoning about composition:

- **Input bandwidth** — how much can it take in?
- **Prior knowledge** — how much does it already know?
- **Resolution** — how fine-grained?
- **Output fidelity** — how faithful to reality?

---

## Principles

1. **No categories, only properties.**
2. **Flat by default.** Add structure per project, not per foundation.
3. **Data is an interface.**
4. **Composition produces emergence.**
5. **Justify every boundary.** The cost of formalism must be less than the value of the separation.
6. **The AI interprets.** Loose is fine when the consumer can reason.
7. **Start coarse, refine under pressure.**

These principles are operationalized through five tests, a golden rule, and anti-patterns.

### Five tests (before creating any new interface boundary)

1. **Independence** — can it be tested alone?
2. **Swap** — would anyone replace just this piece?
3. **Contract simplicity** — is the interface simpler than the implementation?
4. **Communication overhead** — is the boundary cost justified?
5. **Cohesion** — does it do one thing?

### The golden rule

**If formalizing costs more than the AI figuring it out, don't formalize.**

### Anti-patterns

- **Over-decomposition.** Splitting small things into smaller things with no swap scenario.
- **Premature abstraction.** Formalizing something used once.
- **Schema proliferation.** Rigid types for data with one producer and one consumer.
- **Category creep.** Inventing hierarchies. Properties already tell you what it is.

---

## Instances

The abstraction applies broadly. Four cases worth spelling out explicitly.

### Data is an interface

A dataset is not a passive artifact. It transduces physical reality into a consumable form — just like a sensor, except the observation already happened.

A raw CSV has bandwidth (what was captured), prior knowledge (column names encode what someone thought mattered), resolution (sampling rate), and fidelity (how faithfully the numbers represent what happened). The same data cleaned and annotated is a different interface with different properties.

Data quality is interface quality. Data transforms are compositions. The AI agent should know a dataset's properties the same way it knows a sensor's.

### Processes

A process is a sequence of interface invocations. A process is itself an interface.

This means processes are composable by the same rules as any other interface. A data pipeline, a multi-step agent loop, a human approval workflow — all are interfaces with inputs, outputs, and properties. They can be swapped, composed, and reasoned about the same way a sensor or dataset can.

### Algorithms

An algorithm is a derived interface — it takes existing interfaces as inputs and produces new measurements as outputs. A heat stress extrapolation, an anomaly detector, a risk index — these are interfaces with defined inputs, output measurements, confidence levels, and labeling.

The key discipline: derived outputs are always labeled as such. A consumer knows whether they are receiving a measured reading or an algorithm's estimate. Both are interfaces. Neither pretends to be the other.

### Belief states

A belief state captures what a consumer brings to a composition: context, constraints, risk tolerance, action vocabulary, thresholds. A construction supervisor bound by regulatory guidelines, a caregiver checking conditions for an elderly parent, a building's HVAC controller — each is a belief state interface with properties.

Belief states close the loop. Composition is not just about combining sources — it is about producing output that is useful to whoever is receiving it. The consumer's interface shapes what gets selected, evaluated, and returned.

---

## Capabilities

What the framework enables when interfaces are in play.

### Composition

Interfaces compose when the output of one is useful as input to another.

A single sensor sees one thing. A sensor composed with an algorithm and a belief state sees something none of them could see alone. That emergent capability is the point.

Composition can be sequential, parallel, conditional, or agent-directed. The most powerful compositions are discovered at runtime, not designed upfront.

### Incremental delivery

Because every interface is independently useful, any subset of the system is already shippable. You do not need all interfaces to deliver value — two interfaces that compose well are a working system. A third extends it. A fourth enriches it further.

This means milestones are naturally carved by which interfaces are registered. The full system is never a prerequisite for the first useful output. Scope contracts around what's available today and expands as more interfaces are added.

### Observability

Because composition is a chain of interface invocations with explicit inputs and outputs, the full reasoning trace is structural — not bolted on. Every composition can record which interfaces were discovered, selected, and discarded; how thresholds were evaluated; how sources were combined; and why the output took the form it did.

Observability is not a feature. It is a property of the framework. Trust comes from being able to see the chain.

### Extensibility

New interfaces integrate by registration, not by rebuilding. An interface definition describes what the component produces or consumes, its properties, and how to reach it. That definition is the integration contract. Existing interfaces are unaffected.

The system grows by addition. No adapters, no breaking changes, no coordination overhead. Anyone can contribute a new sensor, algorithm, persona, or visualization — and it composes with everything already registered.

### Projects define their own structure

This foundation is domain-agnostic. It contains zero domain-specific items.

Every project built on this foundation will define its own interfaces, its own conventions, and whatever structure its domain requires. A Singapore infrastructure project will have observation schemas, zone models, and belief state conventions. A biosignal project will have entirely different ones.

That structure is necessary and good — it belongs to the project, not to the foundation. The foundation provides the vocabulary. The project provides the specifics.

---

## Lineage

**Unix (1970s)** — "Everything is a file." Collapse diverse resources into one abstraction. Compose via pipes. Do one thing well.

**Entity-Component-System (1998–)** — Entities are IDs with arbitrary components. No inheritance. Composition over hierarchy. Proven in games, robotics, and large-scale simulations.

**Functional programming** — Interfaces as pure functions. Composition as the primary operation. Swap any piece and the system still works.

**Structure & Movement** — The original articulation. No categories, only properties. Interfaces compose. Structure and movement are two lenses on the same thing.

---

*Version: 0.7*
