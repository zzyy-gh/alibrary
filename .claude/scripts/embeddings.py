"""Embedding generation and ChromaDB vector store for the Knowledge Library.

Generates embeddings via OpenAI text-embedding-3-small and stores them in a
persistent ChromaDB collection for semantic search.

Usage:
  python .claude/scripts/embeddings.py embed --file PATH
  python .claude/scripts/embeddings.py embed-all
  python .claude/scripts/embeddings.py search --query TEXT [--tags t1,t2] [--n 10]
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import parse_frontmatter, get_project_root


def _get_openai_client():
    """Return an OpenAI client, exiting with a clear error if no API key."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Set it with: export OPENAI_API_KEY='sk-...'", file=sys.stderr)
        sys.exit(1)
    from openai import OpenAI
    return OpenAI(api_key=api_key)


def _get_chroma_collection():
    """Return the persistent ChromaDB collection."""
    import chromadb
    chroma_path = str(get_project_root() / ".claude" / "scripts" / "chroma_db")
    client = chromadb.PersistentClient(path=chroma_path)
    return client.get_or_create_collection(name="library")


def _build_embed_text(frontmatter: dict, body: str) -> str:
    """Concatenate title, summary, and body for embedding."""
    parts = []
    if frontmatter.get("title"):
        parts.append(frontmatter["title"])
    if frontmatter.get("summary"):
        parts.append(frontmatter["summary"])
    parts.append(body)
    return "\n".join(parts)


def _build_metadata(frontmatter: dict, file_path: str) -> dict:
    """Build metadata dict for ChromaDB storage."""
    tags = frontmatter.get("tags", [])
    if isinstance(tags, list):
        tags = ",".join(tags)

    # Determine item_type from file path
    item_type = "nugget" if "/nuggets/" in file_path.replace("\\", "/") else "raw"

    return {
        "id": frontmatter.get("id", ""),
        "title": frontmatter.get("title", ""),
        "tags": tags,
        "maturity": frontmatter.get("maturity", ""),
        "item_type": item_type,
        "file_path": file_path,
    }


def generate_embedding(text: str) -> list[float]:
    """Call OpenAI text-embedding-3-small and return 1536-dim vector."""
    client = _get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def store_embedding(item_id: str, text: str, metadata: dict) -> None:
    """Generate embedding and upsert into ChromaDB."""
    embedding = generate_embedding(text)
    collection = _get_chroma_collection()
    collection.upsert(
        ids=[item_id],
        embeddings=[embedding],
        metadatas=[metadata],
        documents=[text],
    )


def search_similar(query: str, n_results: int = 10, where: dict | None = None) -> list[dict]:
    """Semantic search with optional metadata filters. Returns list of result dicts."""
    query_embedding = generate_embedding(query)
    collection = _get_chroma_collection()

    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
    }
    if where:
        kwargs["where"] = where

    try:
        results = collection.query(**kwargs)
    except Exception:
        # Collection may be empty
        return []

    output = []
    if results and results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            distance = results["distances"][0][i] if results["distances"] else 0.0
            document = results["documents"][0][i] if results["documents"] else ""
            output.append({
                "id": meta.get("id", doc_id),
                "title": meta.get("title", ""),
                "tags": meta.get("tags", ""),
                "maturity": meta.get("maturity", ""),
                "item_type": meta.get("item_type", ""),
                "file_path": meta.get("file_path", ""),
                "relevance_score": 1.0 - distance,  # Convert distance to similarity
                "document": document,
            })
    return output


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
    metadata = _build_metadata(fm, str(fpath.resolve()))

    try:
        store_embedding(item_id, text, metadata)
        print(f"Embedded: {fm.get('title', fpath.name)} ({item_id[:8]}..)")
    except Exception as e:
        print(f"Error embedding {fpath.name}: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_embed_all(args):
    """Scan inbox/ and nuggets/, embed all markdown files not already in ChromaDB."""
    root = get_project_root()
    collection = _get_chroma_collection()

    # Get existing IDs
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
                metadata = _build_metadata(fm, str(fpath.resolve()))
                store_embedding(item_id, text, metadata)
                embedded += 1
                print(f"  Embedded: {fm.get('title', fpath.name)}")
            except Exception as e:
                print(f"  Warning: failed to embed {fpath.name}: {e}", file=sys.stderr)
                failed += 1
                continue

    print(f"\nDone. Embedded: {embedded}, Skipped: {skipped}, Failed: {failed}")


def cmd_search(args):
    """Search for similar items."""
    where = {}
    if args.tags:
        tag_list = [t.strip() for t in args.tags.split(",")]
        if len(tag_list) == 1:
            where["tags"] = {"$contains": tag_list[0]}
        else:
            where["$and"] = [{"tags": {"$contains": t}} for t in tag_list]

    if where:
        results = search_similar(args.query, n_results=args.n, where=where)
    else:
        results = search_similar(args.query, n_results=args.n)

    if not results:
        print("No results found.")
        return

    for r in results:
        score = r.get("relevance_score", 0)
        print(f"[{score:.3f}] {r.get('title', '?')} ({r.get('id', '?')[:8]}..)")
        if r.get("tags"):
            print(f"         tags: {r['tags']}")
        print(f"         type: {r.get('item_type', '?')}, maturity: {r.get('maturity', '?')}")
        print(f"         path: {r.get('file_path', '?')}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Embedding generation and search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # embed
    p_embed = subparsers.add_parser("embed", help="Embed a single file")
    p_embed.add_argument("--file", required=True, help="Path to markdown file")

    # embed-all
    subparsers.add_parser("embed-all", help="Embed all items in inbox/ and nuggets/")

    # search
    p_search = subparsers.add_parser("search", help="Semantic search")
    p_search.add_argument("--query", required=True, help="Search query")
    p_search.add_argument("--tags", help="Comma-separated tags to filter by")
    p_search.add_argument("--n", type=int, default=10, help="Number of results (default: 10)")

    args = parser.parse_args()

    if args.command == "embed":
        cmd_embed(args)
    elif args.command == "embed-all":
        cmd_embed_all(args)
    elif args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
