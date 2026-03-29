# The Knowledge Library

A vector database for knowledge — with AI agents that catalogue, search, and synthesize across sources.

At its core, this is a vector database. You put documents in, they get embedded, and you search by meaning. What makes it interesting is the exploration of how knowledge should be represented as vectors — and whether there are better ways than the standard approach.

## What it does

- **Ingest anything** — articles, notes, code snippets, research papers. Drop it in `/inbox/`.
- **Embed and search** — content is converted to vectors (Gemini/OpenAI embeddings) and stored in ChromaDB. Search by meaning, tags, or keywords.
- **Synthesize** — when the librarian finds patterns across multiple sources, it creates nuggets — new knowledge that doesn't exist in any single document.
- **Visualize** — explore your knowledge as an interactive 2D map of semantic similarity, filterable by tags.

## The research question

Standard vector search works: embed text as a single high-dimensional vector, find nearest neighbors by cosine similarity. But there's a lot more to explore:

**Better retrieval** — hybrid search (BM25 + vectors), cross-encoder reranking, contextual chunking, query expansion. These are proven techniques that improve search quality 15-60%.

**Richer representations** — instead of one vector per document, what about multi-facet embeddings (separate vectors per aspect), hyperbolic embeddings (for hierarchical knowledge), or box/region embeddings (concepts as shapes, not points)?

**Self-improving search** — retrieval systems that learn from usage patterns via reinforcement learning, confidence decay on unused knowledge, and topological gap detection.

**New physical substrates** — quantum-inspired embeddings where ambiguity is literal superposition, neuromorphic associative memory that does pattern completion instead of nearest-neighbor search, and hyperdimensional computing with algebraic vector composition.

The library serves as a testbed for these ideas. The current implementation is standard (Gemini embeddings + ChromaDB cosine similarity), but the architecture is designed to swap in different embedding methods, search strategies, and representation approaches.

## Architecture

Simple: filesystem + ChromaDB.

- `/inbox/` — raw documents (Markdown with YAML frontmatter)
- `/nuggets/` — AI-synthesized insights from cross-source patterns
- ChromaDB — vector embeddings for semantic search
- AI agents — indexer (catalogue), retriever (search), librarian (synthesize), tester (verify)

No application database. No event queue. Git-versioned Markdown is the source of truth.

## Getting started

```bash
pip install -r requirements.txt
# Add your API key to .env (GEMINI_API_KEY or OPENAI_API_KEY)
python .claude/scripts/cli.py ingest --text "Your knowledge here" --title "My First Item"
python .claude/scripts/cli.py search --query "your question"
```

## Learn more

- `meta/vision.md` — design principles
- `meta/agents.md` — how the agents work
- `inbox/knowledge-representation-theory-and-practice.md` — epistemology of knowledge representation and practical vector search techniques
