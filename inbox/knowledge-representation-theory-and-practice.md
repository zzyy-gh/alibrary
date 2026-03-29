---
id: f2999364-f468-4685-99d9-85da22427434
title: Knowledge Representation — Theory and Practice
source_type: manual
source_url: meta/vision.md
tags:
  - knowledge-representation
  - epistemology
  - vector-search
  - embeddings
  - retrieval
  - research
created_at: 2026-03-24 00:00:00+00:00
created_by: human
maturity: detailed
---

# Knowledge Representation — Theory and Practice

Why knowledge representation is fundamentally hard, and what to do about it anyway. Covers epistemological foundations, production-ready improvements, experimental approaches, and speculative directions. Domain-general observations distilled in part from the library's own governance design (`meta/vision.md`).

---

## Part 1: Why Representation Is Hard

### Connections are knowledge

In a graph, edges connect nodes. But the relationship between two ideas is itself an insight — it should be a node, which needs its own edges, recursively. The node/edge distinction is a projection we impose, not a property of knowledge itself. Any system that treats relationships as second-class (mere pointers between "real" knowledge) is discarding information.

### Every representation is a scoping act

No representation is neutral. Each one illuminates certain connections while burying others:

| Representation   | Reveals                           | Obscures                                    |
| ---------------- | --------------------------------- | ------------------------------------------- |
| Dense vectors    | Semantic similarity               | Structural, causal, temporal relationships  |
| Graphs           | Named, explicit links             | Latent connections no one has articulated   |
| Hierarchies      | Containment, parent-child         | Multi-membership, cross-cutting concerns    |
| Tags             | Human-curated categorical axes    | Gradation, vocabulary beyond what's defined |
| Dense prose      | Nuance, exceptions, context       | Computationally expensive to search         |
| Provenance links | Causal chains, derivation history | Only connections someone chose to record    |

Choosing a representation is choosing what to see and what to miss. This applies to embeddings too — a model projects text into a fixed-dimensional space, collapsing dimensions it wasn't trained to distinguish.

### The environment defines meaning

An embedding has no meaning in isolation. What it "means" is determined by the space it inhabits: what other embeddings surround it, what the model was trained to distinguish, how the vector store indexes and computes distance. The same vector in a different collection — different neighbors, different density, different training distribution — means something different, because proximity and clustering shift. The storage environment is not a neutral container; it is one of the major interfaces through which we interpret knowledge. Any system that treats embeddings as portable, context-free representations is ignoring this dependency.

### Correctness is contextual

A claim's validity depends on its assumptions and scope. Quality isn't about converging on the right answer — it's about making assumptions explicit and letting the consumer judge applicability. Two contradictory entries can both be correct within their own assumptions.

### The retrieval-discovery tension

Optimizing for retrieval (known-unknowns: "find me something like X") and discovery (unknown-unknowns: "show me something I didn't know to ask for") pull in opposite directions. Retrieval rewards cheap similarity computation. Discovery rewards surfacing surprises — cross-domain analogies, structural isomorphisms, contradictions. A system that optimizes only for retrieval converges on one dominant representation and loses the ability to surprise. The design challenge is serving both.

### Responses to these limits

**Layer complementary projections.** Since no single representation is complete, maintain multiple and look for insight in the gaps between them. Novel and deep connections are most likely to be found _between_ projections — where one representation's blind spot is another's strength. This is why cross-pollination (letting knowledge points interact across representation boundaries) is a first-class concern, not an optimization.

**Compress, don't accumulate.** Knowledge that only grows becomes noise. The deeper operation is compression: many observations collapsing into fewer, denser representations. This is true at every level — individual nuggets getting more precise, redundant nuggets merging, abstraction gradients forming where high-level principles derive lower-level specifics. The test of a mature knowledge system isn't how much it contains but how much it can say with how little.

---

## Part 2: What to Store

Parts 2–4 map the three factors that shape knowledge representation: what information to encode, how to refine it over time, and which techniques enable each.

Current standard: embed semantic meaning as a single dense vector. But text carries more signal:

- **Semantic meaning** — what the content is about (the baseline).
- **Structural position** — where in the document: heading level, code vs prose, argument flow. Two documents with identical content but different structures (tutorial vs reference) serve different purposes.
- **Temporal context** — when this was true. "Best practices in 2024" has a different validity window than a mathematical proof. Freshness matters but isn't currently encoded.
- **Relational context** — what this connects to. Tags and embedding proximity capture some of this, but explicit connections (builds on X, contradicts Y) are lost in a flat vector.
- **Invariance level** — rules that are always true vs claims that depend on context. "Water boils at 100°C" is different from "React is the best frontend framework" — one is invariant, the other is contextual. The representation should distinguish these (see also Part 1: Correctness is contextual).
- **Uncertainty** — proven fact vs well-supported hypothesis vs speculation. Current embeddings treat all content as equally certain.
- **Boundary conditions** — where knowledge _stops being valid_, not just what it's about. A nugget about "event-driven architecture" applies to distributed systems but not to UI event handlers. But boundaries are not fixed — two topics irrelevant under one subtopic may be deeply connected under another. Scope itself is blurry: relevance depends on which question is being asked, not on a static property of the knowledge. Current embeddings encode _what something is about_ but not _where it stops being valid_ or _relative to what_. Box embeddings get closest (a region has edges that can overlap), but explicitly representing context-dependent boundaries is largely open.

---

## Part 3: How to Improve Over Time

Static embeddings are snapshots. Knowledge should evolve:

- **Cross-pollination** — let knowledge points interact to discover better arrangements. Two points near each other in embedding space may reveal a pattern that neither states individually. This can happen at the synthesis level (librarian creating nuggets) or at the embedding level (RL-refined retrieval adjusting vectors based on what actually gets used together).
- **Environmental interaction** — treat the knowledge base as an entity that tests its understanding against the external world. Instead of passively storing information, the system makes predictions, observes outcomes, and updates its representations. A knowledge point that consistently leads to wrong predictions should weaken; one that proves useful should strengthen.
- **Compression** — as knowledge accumulates, represent the same understanding with fewer, denser points. Many similar observations collapse into a single, richer representation. The information isn't lost, it's distilled. (See also Part 1: Compress, don't accumulate.)

---

## Part 4: Practical Techniques

Organized by implementation priority, starting with what improves retrieval today and ending with frontier approaches.

### Tier 1: High Impact, Implement First

**Hybrid search (vector + BM25).** Merge results via Reciprocal Rank Fusion. Vectors catch meaning; BM25 catches exact terms. 15-30% recall improvement. Most vector databases support natively. Highest single-change ROI.

**Contextual retrieval.** Anthropic's technique: before embedding a chunk, pass the full document + chunk to an LLM asking for a short context sentence (e.g., "This chunk describes Q3 revenue for Acme Corp's cloud division"). Prepend that context before embedding. Reduces retrieval failure 35-67%. Under $5 for <1000 items. Straightforward to implement in 1-2 days.

**Cross-encoder reranking.** After initial retrieval of 50-200 candidates, rerank with a cross-encoder that scores query-document pairs jointly. The cross-encoder is slower but much more accurate than cosine similarity alone. +28-40% accuracy, +120ms latency. Use Cohere Rerank v3, FlashRank, or open-source cross-encoders like ms-marco-MiniLM.

**Chunking.** Recursive at ~512 tokens with 25% overlap outperforms semantic chunking (69% vs 54% accuracy). Semantic chunking produces fragments too small for useful context. For knowledge bases with items of varying length, recursive splitting is the better default. Pair with contextual retrieval to solve the context-loss problem.

**Embedding models (2025-2026).** Voyage 3.5 (best quality, $0.06/1M tokens), Voyage 3.5-lite (best cost/quality, $0.02/1M tokens), Cohere Embed v4 (128K context, best multilingual). Open-source: Qwen3-Embedding-8B, BGE-en-ICL. Important: evaluate on retrieval sub-scores on MTEB, not overall averages.

### Tier 2: Add After Tier 1

**Query expansion.** Generate 3-5 query reformulations via LLM, search all, merge with RRF. Helps when the user's phrasing doesn't match the stored content's phrasing. 10-15% improvement on ambiguous queries.

**HyDE.** Embed a hypothetical answer instead of the query. The answer is closer in embedding space to the real answer than the question is. 10-20% recall improvement on ambiguous queries. One extra LLM call per query.

**Metadata-filtered search.** Use tags as pre-filters before vector search. All major vector databases support this. Reduces search space and improves precision. Essentially free for tagged knowledge bases.

**Matryoshka embeddings.** Most modern embedding models support truncating dimensions (e.g., 256 of 3072 for fast initial filtering, full dimensions for reranking). Useful for two-stage retrieval when the corpus grows large.

**Evaluation.** RAGAS for reference-free evaluation with LLM-as-judge. It generates synthetic test questions from your documents and scores faithfulness, context precision, and answer relevancy — no manually labeled data needed. Track Recall@k, MRR, NDCG@10. Can't improve what you don't measure.

### Tier 3: Experimental, Working Implementations

**Multi-facet embeddings.** Instead of one vector per document, decompose into multiple aspect vectors — each independently searchable. A document about "event-driven architecture" gets separate vectors for patterns, messaging, scalability. ColBERT (ICLR 2025) creates per-token vectors. Multi-Aspect Dense Retrieval (KDD) produces explicit aspect vectors. Contextual Document Embeddings (CDE, ICLR 2025) make embeddings corpus-aware. Production-ready via ColBERT, but 2-3x storage overhead.

**Hyperbolic embeddings.** Standard vector spaces are flat (Euclidean), but knowledge is often hierarchical. Hyperbolic space naturally encodes hierarchy — broad concepts near origin, specific at edges. 50-300% improvement for ontology/taxonomy tasks. A 2025 position paper argues hyperbolic embeddings are essential for medical knowledge graphs. Most applicable when your knowledge has clear hierarchical structure.

**Self-improving retrieval (RL).** The R3 framework (2025) uses downstream generation rewards to relabel retrieved documents and fine-tune retriever embeddings via contrastive learning. The system observes which retrievals actually helped produce good answers and adjusts embeddings accordingly. 5.2% improvement, trainable in one day on 4 GPUs. MDP-based RAG optimization formalizes retrieval as a reinforcement learning problem. Multi-turn RL search achieves 85% vs 33% for naive RAG on complex queries.

**TDA gap detection.** Persistent homology finds "holes" in embedding space — areas where knowledge is missing. Maps the shape of your knowledge and reveals gaps without knowing what should fill them. The killer application for knowledge bases: automatically detecting what topics are under-covered. Libraries: giotto-tda, GUDHI. Experimental but usable.

**Geometric representations.** Instead of representing knowledge as points, represent it as regions or shapes. Box embeddings represent concepts as hyperrectangles — enabling subset, overlap, and containment reasoning ("agents" is a box that overlaps with "automation" and "orchestration"). Gaussian embeddings (KG2E) represent uncertainty — a well-understood concept has a tight distribution, a vague one is spread out. Cone embeddings capture partial order. Poincare embeddings capture hierarchy. Libraries for geometric approaches: geoopt, geomstats. Experimental with working implementations.

**Adaptive query routing.** Classify queries by type (lookup vs synthesis vs exploratory) and route to different retrieval strategies. A lightweight classifier at the front of the pipeline. Simpler than full agentic RAG, captures most benefit.

### Tier 4: Frontier Research

**Structural embeddings.** Encode not just what a document says but how it's organized — heading hierarchy, code vs prose, argument flow, section relationships. Tree-structured positional embeddings work for code ASTs (2025). Graph positional encoders are mature in GNN literature (ICLR 2025 MoSE). But encoding document structure into embeddings is largely unexplored — a genuine opportunity gap. The intuition: two documents with the same content but different structure (tutorial vs reference) should have different representations.

**Quantum-inspired embeddings.** Words as superpositions in complex-valued Hilbert spaces. Ambiguity is literal quantum superposition until "measured" by context. Composition produces interference patterns. Quantinuum's lambeq is the only real toolkit. A 2025 paper demonstrated cosine similarity on actual quantum hardware. Theoretically elegant for polysemy but years from practical use for knowledge retrieval.

**Embodied / interactive knowledge.** The frontier implementation of Part 3's environmental interaction principle. Systems that learn by interacting with environments rather than just reading text. DreamerV3 does "virtual interaction" via world models — imagining scenarios to test understanding. IJCAI 2025 addresses grounding LLM knowledge to the real world. A knowledge base that verifies claims by testing them remains speculative. The more immediate angle: active learning — choosing what to learn next based on detected gaps rather than passively accepting what's ingested.

**Neuromorphic memory.** Modern Hopfield Networks achieve exponential storage capacity and are mathematically connected to transformer attention. They do pattern completion — "given fragments, find the full pattern" — rather than nearest-neighbor search. Hyperdimensional Computing uses random high-dimensional binary vectors composed algebraically, with no gradient descent needed. The distinction: current vector search finds "what's closest to this query" while associative memory finds "what pattern is this fragment part of." Radically different from current retrieval.

**GraphRAG.** Uses an LLM to extract entities and relationships from documents, builds a knowledge graph, clusters into communities, and generates community summaries. At query time, retrieves relevant community summaries for "global" questions. LinkedIn: 40→15 hour ticket resolution. But 3-5x extraction cost, needs domain tuning. Most beneficial for "big picture" questions over 5,000+ items. For small knowledge bases, long context windows can substitute.

**Embedding fine-tuning.** Contrastive learning on domain-specific query-document pairs. Data requirements: 1,000-5,000 pairs for narrow domains, 10,000+ for complex ones. One study showed 7% improvement with 6,300 samples at under $0.10 compute. Tools: sentence-transformers, OpenAI fine-tuning API. A smaller fine-tuned model often outperforms a larger general-purpose one on domain-specific tasks. Not a priority until simpler approaches are exhausted.

---

## Part 5: Production Patterns (ruflo case study)

Analysis of ruflo (ruvnet/ruflo), a multi-agent orchestration framework with 60+ agents, reveals several retrieval patterns worth adopting.

**MMR diversification (high value, easy).** Maximal Marginal Relevance prevents near-duplicate results. Score each candidate as `0.7 * relevance + 0.3 * diversity`, where diversity is the distance from already-selected results. Simple post-processing on top of any retrieval.

**Confidence lifecycle (medium value, medium effort).** Each entry has a confidence score that decays over time (-0.005/hour) and strengthens on access (+0.03). Below threshold: candidate for archival or refresh. Above consolidation threshold (10+ accesses): trigger learning. Self-pruning.

**Multi-strategy merging (medium value, easy).** Combine semantic, tag, and keyword results. Four merge approaches: union (all results from all strategies), intersection (only results found by multiple), semantic-first (vector results boosted, others supplementary), structured-first (tag/keyword matches boosted). Choose based on query type — exploratory queries benefit from union, precise lookups from intersection.

**Graph-boosted ranking (high value if graph exists).** Build a knowledge graph from entries (typed edges: reference, similarity, temporal, co-access), run PageRank, blend: 70% cosine + 30% PageRank. Structurally important nodes get boosted. Most relevant for large knowledge bases with rich interconnections.

**Notable gaps.** Despite sophisticated orchestration, ruflo has no built-in embedding generation (injected externally), no chunking strategies, no contextual enrichment, no hybrid BM25+vector search. Hash-based fallback embeddings have no semantic understanding. The retrieval pipeline is simpler than it appears from the README.

---

## What's Overhyped vs Underappreciated

| Overhyped                               | Underappreciated                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------- |
| Pure vector search as complete solution | BM25/keyword search (embarrassingly effective for exact terms)               |
| GraphRAG for small datasets             | Chunking strategy (bigger impact than model choice)                          |
| Full agentic RAG for simple Q&A         | Cross-encoder reranking (highest ROI single addition after basic retrieval)  |
| "Just use a bigger context window"      | Evaluation frameworks (can't improve unmeasured)                             |
|                                         | TDA gap detection (finds missing knowledge without knowing what to look for) |

---

## Technique Substrate Reference

| Technique                                   | What it encodes                                                       | Best for                         |
| ------------------------------------------- | --------------------------------------------------------------------- | -------------------------------- |
| Standard dense vectors                      | Semantic meaning (baseline, good at meaning, weak at everything else) | General-purpose similarity       |
| Quantum-inspired                            | Ambiguity, superposition                                              | Polysemous content               |
| Structural                                  | Document organization                                                 | Mixed-format corpora             |
| Geometric (hyperbolic, box, cone, Poincare) | Hierarchy, regions, partial order                                     | Taxonomies, ontologies           |
| Multi-facet                                 | Cross-cutting aspects                                                 | Multi-topic documents            |
| Neuromorphic                                | Associative patterns                                                  | Pattern completion               |
| Topological                                 | Knowledge shape, gaps                                                 | Gap detection, coverage analysis |

---
