# Skill: generate-embedding

Generate a vector embedding for a library item.

**STATUS: STUB — Phase 2 implementation.**

## Input

- A file path to a Markdown file (raw item or nugget)

## Process

Phase 2 will integrate an embedding model (Voyage / OpenAI / local) and store embeddings in the vector index (SQLite-vec / Chroma).

Currently: no-op. Log that embedding generation is deferred to Phase 2.

## Output

- Current: no output (stub)
- Phase 2: embedding vector stored in vector index

## Constraints

- Do not block the indexer pipeline — if this fails, continue processing
