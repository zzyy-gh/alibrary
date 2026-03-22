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
2. Generate an embedding via OpenAI text-embedding-3-small
3. Upsert the embedding into the ChromaDB vector store

## Output

- Embedding vector stored in ChromaDB (`.claude/scripts/chroma_db/`)
- Confirmation message printed to stdout

## Constraints

- Do not block the indexer pipeline — if this fails, log the error and continue processing
- Requires `OPENAI_API_KEY` environment variable to be set
