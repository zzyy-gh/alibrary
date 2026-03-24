---
id: f2999364-f468-4685-99d9-85da22427434
title: Improving Vector Search and Knowledge Representation
source_type: manual
tags:
- vector-search
- embeddings
- retrieval
- research
created_at: 2026-03-24 00:00:00+00:00
created_by: human
maturity: summary
---

# Improving Vector Search and Knowledge Representation

Research on practical and frontier techniques for improving how knowledge bases store, search, and represent information. Covers production-ready improvements, experimental approaches, and speculative directions. Organized by implementation priority.

---

## Tier 1: High Impact, Implement First

### Hybrid Search (Vector + BM25)

Combine vector similarity search with traditional keyword search (BM25) and merge results using Reciprocal Rank Fusion (RRF). Vectors catch semantic meaning; BM25 catches exact terms that embeddings sometimes miss. 15-30% recall improvement. Most vector databases support this natively. The single highest-ROI change for most systems.

### Contextual Retrieval

Anthropic's technique: before embedding each chunk, pass the full document + chunk to an LLM asking for a short context sentence (e.g., "This chunk describes Q3 revenue for Acme Corp's cloud division"). Prepend that context to the chunk before embedding. Reduces retrieval failure by 35-67%. Cost: under $5 for a corpus of <1000 items. Straightforward to implement in 1-2 days.

### Cross-Encoder Reranking

After initial retrieval of 50-200 candidates via vector search, rerank with a cross-encoder model that scores query-document pairs jointly. The cross-encoder is slower but much more accurate than cosine similarity alone. +28-40% accuracy for only +120ms latency. Use Cohere Rerank v3, FlashRank, or open-source cross-encoders like ms-marco-MiniLM.

### Chunking Strategy

Recursive chunking at ~512 tokens with 25% overlap outperforms semantic chunking in benchmarks (69% vs 54% accuracy). Semantic chunking produces fragments too small for useful context. For knowledge bases with items of varying length, recursive splitting is the better default. Pair with contextual retrieval to solve the context-loss problem.

### Embedding Model Choice

Current leaders for retrieval (2025-2026): Voyage 3.5 (best quality, $0.06/1M tokens), Voyage 3.5-lite (best cost/quality, $0.02/1M tokens), Cohere Embed v4 (128K context, best multilingual). Open-source: Qwen3-Embedding-8B, BGE-en-ICL. Important: evaluate on retrieval sub-scores on MTEB, not overall averages.

---

## Tier 2: Medium Impact, Add After Tier 1

### Query Expansion / Multi-Query

Generate 3-5 reformulations of the user's query via LLM, search all variants, merge results with RRF. Helps when the user's phrasing doesn't match the stored content's phrasing. 10-15% improvement on ambiguous queries.

### HyDE (Hypothetical Document Embeddings)

Instead of embedding the query directly, ask an LLM to generate a hypothetical answer to the query, then embed that answer and search. The hypothetical answer is closer in embedding space to the real answer than the question is. 10-20% recall improvement on ambiguous queries. One extra LLM call per query.

### Metadata-Filtered Search

Use tags and structured metadata as pre-filters before vector search. All major vector databases support this. Reduces search space and improves precision. For a tagged knowledge base, this is essentially free.

### Matryoshka Embeddings

Most modern embedding models support truncating dimensions (e.g., use 256 of 3072 dimensions for fast initial filtering, full dimensions for reranking). Useful for two-stage retrieval when the corpus grows large.

### Evaluation Framework

Use RAGAS for reference-free evaluation with LLM-as-judge. It generates synthetic test questions from your documents and scores faithfulness, context precision, and answer relevancy — no manually labeled data needed. Track Recall@k, MRR, and NDCG@10 as you add techniques. You can't improve what you don't measure.

---

## Tier 3: Experimental, Real Implementations Exist

### Multi-Facet / Decomposed Embeddings

Instead of one vector per document, decompose into multiple aspect vectors. A document about "event-driven architecture" gets separate vectors for architecture patterns, messaging, and scalability — each independently searchable. ColBERT (late interaction, ICLR 2025) creates one vector per token. Multi-Aspect Dense Retrieval (KDD) produces explicit aspect vectors. Contextual Document Embeddings (CDE, ICLR 2025) make embeddings corpus-aware. Production-ready via ColBERT, but 2-3x storage overhead.

### Hyperbolic Embeddings

Standard vector spaces are flat (Euclidean), but knowledge is often hierarchical. Hyperbolic space naturally encodes hierarchy — broad concepts near the origin, specific ones at the edges. 50-300% improvement over Euclidean for ontology and taxonomy tasks. Python libraries: geoopt, geomstats. A 2025 position paper argues hyperbolic embeddings are essential for medical knowledge graphs. Most applicable when your knowledge has clear hierarchical structure.

### Self-Improving Retrieval (RL)

The R3 framework (2025) uses downstream generation rewards to relabel retrieved documents and fine-tune retriever embeddings via contrastive learning. The system observes which retrievals actually helped produce good answers and adjusts embeddings accordingly. 5.2% improvement, trainable in one day on 4 GPUs. MDP-based RAG optimization formalizes retrieval as a reinforcement learning problem. Multi-turn RL search achieves 85% vs 33% for naive RAG on complex queries.

### TDA Gap Detection

Topological data analysis finds "holes" in your embedding space — areas where knowledge is missing. Persistent homology maps the shape of your knowledge and reveals gaps without knowing what should fill them. The killer application for knowledge bases: automatically detecting what topics are under-covered. Libraries: giotto-tda, GUDHI. Experimental but usable.

### Geometric / Shape-Based Representations

Instead of representing knowledge as points in vector space, represent it as regions or shapes. Box embeddings represent concepts as hyperrectangles — enabling subset, overlap, and containment reasoning ("agents" is a box that overlaps with "automation" and "orchestration"). Gaussian embeddings (KG2E) represent uncertainty — a well-understood concept has a tight distribution, a vague one is spread out. Cone embeddings capture partial order. Poincare embeddings capture hierarchy. Libraries: geoopt, geomstats. Experimental with working implementations.

### Adaptive Query Routing

Classify queries into types (simple lookup vs needs synthesis vs exploratory) and route to different retrieval strategies. Simpler than full agentic RAG but captures most of the benefit. A lightweight classifier at the front of the pipeline.

---

## Tier 4: Frontier Research, Speculative

### Structural Embeddings

Encode not just what a document says but how it's organized — heading hierarchy, code vs prose, argument flow, section relationships. Tree-structured positional embeddings work for code ASTs (2025). Graph positional encoders are mature in GNN literature (ICLR 2025 MoSE). But encoding document structure into embeddings is largely unexplored — a genuine opportunity gap. The intuition: two documents with the same content but different structure (tutorial vs reference) should have different representations.

### Quantum-Inspired Embeddings

Words as superpositions in complex-valued Hilbert spaces. Ambiguity is literal quantum superposition — a word with multiple meanings exists in all of them simultaneously until "measured" by context. Composition produces interference patterns. Quantinuum's lambeq is the only real toolkit. A 2025 paper demonstrated cosine similarity on actual quantum hardware. Theoretically elegant for polysemy but years from practical use for knowledge retrieval.

### Embodied / Interactive Knowledge

Systems that learn by interacting with environments rather than just reading text. DreamerV3 does "virtual interaction" via world models — imagining scenarios to test understanding. IJCAI 2025 addresses grounding LLM knowledge to the real world. A knowledge base that verifies claims by testing them remains speculative. The more immediate angle: active learning — choosing what to learn next based on detected gaps rather than passively accepting what's ingested.

### Neuromorphic Memory

Modern Hopfield Networks achieve exponential storage capacity and are mathematically connected to transformer attention. They do pattern completion — "given fragments, find the full pattern" — rather than nearest-neighbor search. Hyperdimensional Computing uses random high-dimensional binary vectors composed algebraically, with no gradient descent needed. Radically different from current retrieval approaches. The distinction: current vector search finds "what's closest to this query" while associative memory finds "what pattern is this fragment part of."

### GraphRAG (Microsoft)

Uses an LLM to automatically extract entities and relationships from documents, builds a knowledge graph, clusters into communities, and generates community summaries. At query time, retrieves relevant community summaries for "global" questions. LinkedIn reduced ticket resolution from 40 to 15 hours. But extraction costs 3-5x more than baseline RAG and requires domain-specific tuning. Most beneficial for "big picture" questions over large corpora (5,000+ items). For small knowledge bases, long context windows can substitute.

### Embedding Fine-Tuning

Training custom embeddings on your specific domain using contrastive learning on query-document pairs. Data requirements: 1,000-5,000 pairs for narrow domains, 10,000+ for complex ones. One study showed 7% improvement with 6,300 samples at under $0.10 compute. Tools: sentence-transformers, OpenAI fine-tuning API. A smaller fine-tuned model often outperforms a larger general-purpose one on domain-specific tasks. Not a priority until simpler approaches are exhausted.

---

## What's Overhyped vs Underappreciated

**Overhyped:**
- Pure vector search as the complete solution
- GraphRAG for small datasets
- Full agentic RAG loops for simple Q&A
- "Just use a bigger context window"

**Underappreciated:**
- BM25 / keyword search (embarrassingly effective for exact terms)
- Good chunking strategy (bigger impact than model choice)
- Reranking (highest ROI single addition after basic retrieval)
- Evaluation frameworks (can't improve what you don't measure)
- Topological gap detection (finds what's missing without knowing what to look for)

---

## Patterns from Production Systems (ruflo case study)

Analysis of ruflo (ruvnet/ruflo), a multi-agent orchestration framework with 60+ agents, reveals several retrieval patterns worth adopting.

### MMR Diversification (high value, easy)

Maximal Marginal Relevance prevents returning near-duplicate results. Score each candidate as `0.7 * relevance + 0.3 * diversity`, where diversity is the distance from already-selected results. Simple to implement on top of any vector search — just post-process the top-k results before returning them.

### Confidence Lifecycle (medium value, medium effort)

Memories aren't static — they decay and strengthen based on usage. Each entry has a confidence score that drops over time (-0.005/hour) and increases when accessed (+0.03 per access). Entries below a threshold are candidates for archival or refresh. Entries above a consolidation threshold (10+ accesses) trigger learning. This makes the knowledge base self-pruning: unused knowledge fades, frequently accessed knowledge gets reinforced.

### Multi-Strategy Search Merging (medium value, easy)

Formalize how to combine results from different search strategies (semantic, tag-based, keyword). Four merge approaches: union (all results from all strategies), intersection (only results found by multiple strategies), semantic-first (vector results boosted, others supplementary), structured-first (tag/keyword matches boosted). Choose based on query type — exploratory queries benefit from union, precise lookups from intersection.

### Graph-Boosted Ranking (high value if graph exists)

Build a knowledge graph from entries (typed edges: reference, similarity, temporal, co-access), run PageRank, then blend scores: 70% cosine similarity + 30% PageRank influence. Structurally important nodes get boosted even if their raw similarity score is lower. Most relevant for large knowledge bases with rich interconnections.

### Notable gaps in ruflo's approach

Despite sophisticated orchestration, ruflo has no built-in embedding generation (injected externally), no chunking strategies, no contextual enrichment, and no hybrid BM25+vector search. Their hash-based fallback embeddings have no semantic understanding. The retrieval pipeline is simpler than it appears from the README.

---

## Sources

- Anthropic: Contextual Retrieval (2024)
- ICLR 2025: ColBERT, Contextual Document Embeddings, ColPali
- KDD: Multi-Aspect Dense Retrieval
- R3 Framework (2025): RL for retrieval
- Microsoft Research: GraphRAG
- Quantinuum: lambeq QNLP toolkit
- 2025 surveys: TDA for NLP, Interpretable Embeddings (EMNLP), Agentic RAG
- MTEB benchmark results (2025-2026)
- Production reports: Superlinked, Weaviate, Together AI, NVIDIA
