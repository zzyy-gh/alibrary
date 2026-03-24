"""Embedding generation and ChromaDB vector store for the Knowledge Library.

Model-agnostic: supports multiple embedding providers (Gemini, OpenAI, etc.)
configured via EMBEDDING_PROVIDER in .env file.

Usage:
  python .claude/scripts/embeddings.py embed --file PATH
  python .claude/scripts/embeddings.py embed-all
  python .claude/scripts/embeddings.py search --query TEXT [--n 10]
  python .claude/scripts/embeddings.py reset
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import parse_frontmatter, get_project_root

# Load .env file
from dotenv import load_dotenv
load_dotenv(get_project_root() / ".env")


# --- Provider implementations ---

def _embed_gemini(text: str) -> list[float]:
    """Generate embedding via Google Gemini (gemini-embedding-001, 3072-dim)."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env file.", file=sys.stderr)
        sys.exit(1)
    from google import genai
    client = genai.Client(api_key=api_key)
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values


def _embed_openai(text: str) -> list[float]:
    """Generate embedding via OpenAI (text-embedding-3-small, 1536-dim)."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set in .env file.", file=sys.stderr)
        sys.exit(1)
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


PROVIDERS = {
    "gemini": _embed_gemini,
    "openai": _embed_openai,
}


def _get_provider() -> str:
    """Return the configured embedding provider name."""
    provider = os.environ.get("EMBEDDING_PROVIDER", "gemini").lower()
    if provider not in PROVIDERS:
        print(f"Error: unknown EMBEDDING_PROVIDER '{provider}'. Options: {', '.join(PROVIDERS)}", file=sys.stderr)
        sys.exit(1)
    return provider


# --- Core functions ---

def _get_chroma_collection():
    """Return the persistent ChromaDB collection."""
    import chromadb
    chroma_path = str(get_project_root() / ".claude" / "scripts" / "chroma_db")
    client = chromadb.PersistentClient(path=chroma_path)
    return client.get_or_create_collection(name="library", metadata={"hnsw:space": "cosine"})


def _build_embed_text(frontmatter: dict, body: str) -> str:
    """Concatenate title, summary, and body for embedding."""
    parts = []
    if frontmatter.get("title"):
        parts.append(frontmatter["title"])
    if frontmatter.get("summary"):
        parts.append(frontmatter["summary"])
    parts.append(body)
    return "\n".join(parts)


def generate_embedding(text: str) -> list[float]:
    """Generate embedding using the configured provider."""
    provider = _get_provider()
    return PROVIDERS[provider](text)


def store_embedding(item_id: str, text: str) -> None:
    """Generate embedding and upsert into ChromaDB. Stores only id + embedding."""
    embedding = generate_embedding(text)
    collection = _get_chroma_collection()
    collection.upsert(
        ids=[item_id],
        embeddings=[embedding],
    )


def search_similar(query: str, n_results: int = 10) -> list[dict]:
    """Semantic search. Returns list of {id, relevance_score}. Metadata resolved from files by caller."""
    query_embedding = generate_embedding(query)
    collection = _get_chroma_collection()

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
    except Exception:
        return []

    output = []
    if results and results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            distance = results["distances"][0][i] if results["distances"] else 0.0
            output.append({
                "id": doc_id,
                "relevance_score": 1.0 - distance,
            })
    return output


# --- CLI commands ---

def cmd_embed(args):
    """Embed a single file."""
    fpath = Path(args.file)
    if not fpath.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    fm, body = parse_frontmatter(fpath)
    item_id = fm.get("id")
    if not item_id:
        print(f"Error: file has no 'id' in frontmatter: {args.file}", file=sys.stderr)
        sys.exit(1)

    text = _build_embed_text(fm, body)

    try:
        store_embedding(item_id, text)
        print(f"Embedded: {fm.get('title', fpath.name)} ({item_id[:8]}..)")
    except Exception as e:
        print(f"Error embedding {fpath.name}: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_embed_all(args):
    """Scan inbox/ and nuggets/, embed all markdown files not already in ChromaDB."""
    root = get_project_root()
    provider = _get_provider()
    print(f"Provider: {provider}")

    collection = _get_chroma_collection()

    try:
        existing = set(collection.get()["ids"])
    except Exception:
        existing = set()

    dirs = [root / "inbox", root / "nuggets"]
    embedded = 0
    skipped = 0
    failed = 0

    for d in dirs:
        if not d.is_dir():
            continue
        for fpath in sorted(d.glob("*.md")):
            if fpath.name == ".gitkeep":
                continue
            try:
                fm, body = parse_frontmatter(fpath)
                item_id = fm.get("id")
                if not item_id:
                    print(f"  Warning: skipping {fpath.name} (no id)", file=sys.stderr)
                    skipped += 1
                    continue

                if item_id in existing:
                    skipped += 1
                    continue

                text = _build_embed_text(fm, body)
                store_embedding(item_id, text)
                embedded += 1
                print(f"  Embedded: {fm.get('title', fpath.name)}")
            except Exception as e:
                print(f"  Warning: failed to embed {fpath.name}: {e}", file=sys.stderr)
                failed += 1
                continue

    print(f"\nDone. Embedded: {embedded}, Skipped: {skipped}, Failed: {failed}")


def cmd_search(args):
    """Search for similar items. Returns IDs and relevance scores."""
    results = search_similar(args.query, n_results=args.n)

    if not results:
        print("No results found.")
        return

    for r in results:
        score = r.get("relevance_score", 0)
        print(f"[{score:.3f}] {r['id']}")
    print(f"\n{len(results)} result(s). Use retriever.py for full metadata.")


def _resolve_id(item_id: str) -> dict:
    """Resolve an item ID to metadata by scanning inbox/ and nuggets/."""
    root = get_project_root()
    for d, item_type in [(root / "inbox", "raw"), (root / "nuggets", "nugget")]:
        if not d.is_dir():
            continue
        for fpath in d.glob("*.md"):
            if fpath.name == ".gitkeep":
                continue
            try:
                fm, _ = parse_frontmatter(fpath)
                if fm.get("id") == item_id:
                    maturity = fm.get("maturity", "stub")
                    tags = fm.get("tags", [])
                    if isinstance(tags, list):
                        tags = ", ".join(tags)
                    return {
                        "id": item_id,
                        "title": fm.get("title", fpath.stem),
                        "item_type": item_type,
                        "maturity": maturity,
                        "tags": tags,
                    }
            except Exception:
                continue
    return {"id": item_id, "title": item_id[:12], "item_type": "unknown", "maturity": "stub", "tags": ""}


def cmd_viz(args):
    """Generate a 2D scatter plot of embeddings."""
    import json

    collection = _get_chroma_collection()
    data = collection.get(include=["embeddings"])

    if not data["ids"]:
        print("No embeddings found. Run 'embed-all' first.")
        return

    ids = data["ids"]
    embeddings = data["embeddings"]
    print(f"Loaded {len(ids)} embeddings ({len(embeddings[0])}-dim)")

    # Reduce to 2D
    try:
        from sklearn.manifold import TSNE
        import numpy as np
        arr = np.array(embeddings)
        perplexity = min(5, len(ids) - 1) if len(ids) > 2 else 1
        coords = TSNE(n_components=2, perplexity=perplexity, random_state=42).fit_transform(arr)
        print("Reduced via t-SNE")
    except ImportError:
        # Fallback to PCA if sklearn not available
        import numpy as np
        arr = np.array(embeddings)
        mean = arr.mean(axis=0)
        centered = arr - mean
        cov = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        top2 = eigenvectors[:, -2:]
        coords = centered @ top2
        print("Reduced via PCA (install scikit-learn for t-SNE)")

    # Build data points
    points = []
    for i, item_id in enumerate(ids):
        meta = _resolve_id(item_id)
        meta["x"] = float(coords[i][0])
        meta["y"] = float(coords[i][1])
        points.append(meta)

    # Load template and inject data
    template_path = Path(__file__).parent / "embed_viz_template.html"
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("__EMBED_DATA__", json.dumps(points, ensure_ascii=False))

    output = args.output if args.output else str(get_project_root() / "embeddings.html")
    Path(output).write_text(html, encoding="utf-8")
    print(f"Visualization written to {output}")


def cmd_reset(args):
    """Delete and recreate the ChromaDB collection. Required when switching providers."""
    import chromadb
    chroma_path = str(get_project_root() / ".claude" / "scripts" / "chroma_db")
    client = chromadb.PersistentClient(path=chroma_path)
    try:
        client.delete_collection("library")
        print("Collection 'library' deleted.")
    except Exception:
        print("Collection 'library' did not exist.")
    client.get_or_create_collection(name="library")
    print("Fresh collection created. Run 'embed-all' to re-embed with the new provider.")


def main():
    parser = argparse.ArgumentParser(description="Embedding generation and search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_embed = subparsers.add_parser("embed", help="Embed a single file")
    p_embed.add_argument("--file", required=True, help="Path to markdown file")

    subparsers.add_parser("embed-all", help="Embed all items in inbox/ and nuggets/")

    p_search = subparsers.add_parser("search", help="Semantic search")
    p_search.add_argument("--query", required=True, help="Search query")
    p_search.add_argument("--n", type=int, default=10, help="Number of results (default: 10)")

    p_viz = subparsers.add_parser("viz", help="Visualize embeddings as 2D scatter plot")
    p_viz.add_argument("--output", help="Output HTML path (default: embeddings.html in project root)")

    subparsers.add_parser("reset", help="Reset ChromaDB collection (required when switching providers)")

    args = parser.parse_args()

    if args.command == "embed":
        cmd_embed(args)
    elif args.command == "embed-all":
        cmd_embed_all(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "viz":
        cmd_viz(args)
    elif args.command == "reset":
        cmd_reset(args)


if __name__ == "__main__":
    main()
