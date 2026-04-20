---
id: 6aae4138-a8c4-4179-aa16-8813785092c9
title: Everything is an interface
source_type: manual
tags:
- architecture
- composition
- patterns
- abstraction
- systems-design
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

## Data is an interface

A dataset is not a passive artifact. It transduces physical reality into a consumable form — just like a sensor, except the observation already happened.

A raw CSV has bandwidth (what was captured), prior knowledge (column names encode what someone thought mattered), resolution (sampling rate), and fidelity (how faithfully the numbers represent what happened). The same data cleaned and annotated is a different interface with different properties.

Data quality is interface quality. Data transforms are compositions. The AI agent should know a dataset's properties the same way it knows a sensor's.

---

## Composition

Interfaces compose when the output of one is useful as input to another.

A single sensor sees one thing. A sensor composed with an algorithm and a belief state sees something none of them could see alone. That emergent capability is the point.

Composition can be sequential, parallel, conditional, or agent-directed. The most powerful compositions are discovered at runtime, not designed upfront.

---

## Processes

A process is a sequence of interface invocations. A process is itself an interface.

---

## Projects define their own structure

This foundation is domain-agnostic. It contains zero domain-specific items.

Every project built on this foundation will define its own interfaces, its own conventions, and whatever structure its domain requires. A Singapore infrastructure project will have observation schemas, zone models, and belief state conventions. A biosignal project will have entirely different ones.

That structure is necessary and good — it belongs to the project, not to the foundation. The foundation provides the vocabulary. The project provides the specifics.

---

## Sanity

The core discipline. Everything above is guidance. This is governance.

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

## Lineage

**Unix (1970s)** — "Everything is a file." Collapse diverse resources into one abstraction. Compose via pipes. Do one thing well.

**Entity-Component-System (1998–)** — Entities are IDs with arbitrary components. No inheritance. Composition over hierarchy. Proven in games, robotics, and large-scale simulations.

**Functional programming** — Interfaces as pure functions. Composition as the primary operation. Swap any piece and the system still works.

**Structure & Movement** — The original articulation. No categories, only properties. Interfaces compose. Structure and movement are two lenses on the same thing.

---

## Principles

1. **No categories, only properties.**
2. **Flat by default.** Add structure per project, not per foundation.
3. **Data is an interface.**
4. **Composition produces emergence.**
5. **Sanity before modularity.**
6. **The AI interprets.** Loose is fine when the consumer can reason.
7. **Start coarse, refine under pressure.**

---

*Version: 0.4*
