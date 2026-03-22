# Skill: generate-embedding

Generate a vector embedding for a library item and store it in ChromaDB.

## Input

- A file path to a Markdown file (raw item or nugget)

## Process

Run the embedding script:

```bash
python .claude/scripts/embeddings.py embed --file <path>
```

This will:
1. Parse the file's frontmatter and body
2. Generate an embedding via the configured provider (set in `.env`)
3. Upsert the embedding into the ChromaDB vector store

Supported providers: `gemini` (default), `openai`. Configured via `EMBEDDING_PROVIDER` in `.env`.

## Output

- Embedding vector stored in ChromaDB (`.claude/scripts/chroma_db/`)
- Confirmation message printed to stdout

## Constraints

- Do not block the indexer pipeline — if this fails, log the error and continue processing
- Requires the appropriate API key set in `.env` (e.g. `GEMINI_API_KEY` or `OPENAI_API_KEY`)
- Switching providers requires running `python .claude/scripts/embeddings.py reset` then `embed-all`
