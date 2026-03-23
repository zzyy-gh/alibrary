# The Knowledge Library

A living knowledge base that AI agents can read, write, and learn from. Drop in any information — articles, notes, ideas, documents — and the library organizes it, connects it, and makes it searchable.

## What it does

You put raw material in. AI agents turn it into structured, connected knowledge.

- **Ingest anything** — articles, notes, code snippets, meeting notes, research papers. Just drop it in.
- **Automatic synthesis** — AI agents read your material and create concise, standalone summaries (called "nuggets") that capture the key insights.
- **Smart connections** — the library automatically discovers how pieces of knowledge relate to each other, building a graph of ideas you can explore.
- **Search by meaning** — ask questions in plain language and get relevant answers ranked by confidence, not just keyword matches.
- **Visual exploration** — see your knowledge as an interactive graph of connected ideas, or as a map of topics clustered by similarity.

## Who it's for

- **Individuals** building a personal knowledge base that grows smarter over time
- **Teams** that need a shared source of truth across projects, decisions, and institutional knowledge
- **AI agent builders** who need a structured knowledge layer their agents can query and contribute to

## What makes it different

- **Knowledge, not files.** The library doesn't just store documents — it synthesizes understanding from them. Every nugget is a standalone insight, not a copy of the source.
- **Self-organizing.** Connections between ideas are discovered automatically. You don't need to manually tag, categorize, or link things.
- **Agent-native.** Built for AI agents to use directly. Any agent can query the library, and the library's own agents maintain and improve the knowledge over time.
- **Transparent.** Every piece of knowledge traces back to its source. Every change is logged. You can always see where an insight came from and why it was created.

## The agents

Four AI agents maintain the library:

- **Indexer** — processes new material as it arrives, creates summaries, finds connections
- **Researcher** — answers questions by searching across meaning, tags, keywords, and relationships
- **Tester** — verifies that everything stays consistent and correct as the library grows
- **Librarian** *(coming soon)* — deepens knowledge over time, merges duplicates, fills gaps, manages quality
- **Intern** *(coming soon)* — observes patterns across the whole system and recommends improvements

## Getting started

```bash
pip install -r requirements.txt
# Add your API key to .env (see .env.example)
python .claude/scripts/cli.py ingest --text "Your knowledge here" --title "My First Item"
python .claude/scripts/cli.py search --query "your question"
```

## Learn more

The `meta/` folder contains the full design — start with `meta/vision.md` for principles and `meta/agents.md` for how the agents work.
