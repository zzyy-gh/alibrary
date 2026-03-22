"""Multi-strategy search engine for the Knowledge Library.

Supports semantic search (via ChromaDB), tag-based filtering, and keyword search.
Automatically emits knowledge:gap events when searches return no results.

Usage:
  python .claude/scripts/researcher.py search --query TEXT [--tags t1,t2] [--keyword TEXT] [--maturity M] [--type raw|nugget] [--n 10] [--format json|text]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import parse_frontmatter, get_project_root, load_all_relationships, now_iso
from emit_event import emit_event
from init_db import init_db


MATURITY_CONFIDENCE = {
    "stub": "low",
    "summary": "medium",
    "detailed": "high",
    "complete": "authoritative",
}

MATURITY_RANK = {
    "stub": 0,
    "summary": 1,
    "detailed": 2,
    "complete": 3,
}


def _scan_files(nuggets_dir: Path, inbox_dir: Path) -> list[dict]:
    """Scan inbox and nuggets directories, returning parsed file data."""
    items = []
    for d, item_type in [(inbox_dir, "raw"), (nuggets_dir, "nugget")]:
        if not d.is_dir():
            continue
        for fpath in sorted(d.glob("*.md")):
            if fpath.name == ".gitkeep":
                continue
            try:
                fm, body = parse_frontmatter(fpath)
                items.append({
                    "frontmatter": fm,
                    "body": body,
                    "path": str(fpath),
                    "item_type": item_type,
                })
            except Exception:
                continue
    return items


def _to_result(item: dict, relevance_score: float = 0.0) -> dict:
    """Convert a scanned item to a result dict."""
    fm = item["frontmatter"]
    maturity = fm.get("maturity", "stub")
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return {
        "id": fm.get("id", ""),
        "title": fm.get("title", ""),
        "maturity": maturity,
        "confidence_level": MATURITY_CONFIDENCE.get(maturity, "low"),
        "relevance_score": relevance_score,
        "summary": fm.get("summary", ""),
        "tags": tags,
        "file_path": item.get("path", ""),
        "item_type": item.get("item_type", ""),
    }


def search_tags(tags: list[str], nuggets_dir: Path, inbox_dir: Path) -> list[dict]:
    """Filter items by tag match."""
    items = _scan_files(nuggets_dir, inbox_dir)
    tags_needed = set(t.lower() for t in tags)
    results = []
    for item in items:
        item_tags = item["frontmatter"].get("tags", [])
        if isinstance(item_tags, str):
            item_tags = [t.strip() for t in item_tags.split(",")]
        item_tags_lower = set(t.lower() for t in item_tags)
        if tags_needed.intersection(item_tags_lower):
            # Score by how many tags match
            match_count = len(tags_needed.intersection(item_tags_lower))
            score = match_count / len(tags_needed)
            results.append(_to_result(item, relevance_score=score))

    results.sort(key=lambda r: (-r["relevance_score"], -MATURITY_RANK.get(r["maturity"], 0)))
    return results


def search_keyword(keyword: str, nuggets_dir: Path, inbox_dir: Path) -> list[dict]:
    """Fulltext search in title/summary/body."""
    items = _scan_files(nuggets_dir, inbox_dir)
    kw = keyword.lower()
    results = []
    for item in items:
        fm = item["frontmatter"]
        title = fm.get("title", "").lower()
        summary = fm.get("summary", "").lower()
        body = item["body"].lower()

        # Simple relevance: title match > summary match > body match
        score = 0.0
        if kw in title:
            score = 1.0
        elif kw in summary:
            score = 0.7
        elif kw in body:
            score = 0.4

        if score > 0:
            results.append(_to_result(item, relevance_score=score))

    results.sort(key=lambda r: (-r["relevance_score"], -MATURITY_RANK.get(r["maturity"], 0)))
    return results


def _build_id_lookup(nuggets_dir: Path, inbox_dir: Path) -> dict:
    """Build a lookup from item ID to parsed file data."""
    items = _scan_files(nuggets_dir, inbox_dir)
    return {item["frontmatter"].get("id"): item for item in items if item["frontmatter"].get("id")}


def search_semantic(query: str, n: int = 10) -> list[dict]:
    """Semantic search via ChromaDB embeddings. Resolves metadata from files."""
    from embeddings import search_similar
    raw_results = search_similar(query, n_results=n)

    if not raw_results:
        return []

    root = get_project_root()
    lookup = _build_id_lookup(root / "nuggets", root / "inbox")

    results = []
    for r in raw_results:
        item = lookup.get(r["id"])
        if item:
            result = _to_result(item, relevance_score=r["relevance_score"])
            results.append(result)
        else:
            # ID in ChromaDB but file not found — stale entry
            results.append({
                "id": r["id"],
                "title": "(unresolved)",
                "maturity": "",
                "confidence_level": "low",
                "relevance_score": r["relevance_score"],
                "summary": "",
                "tags": [],
                "file_path": "",
                "item_type": "",
            })
    return results


def _emit_gap_event(query_text: str, strategies: list[str]) -> None:
    """Emit a knowledge:gap event when search returns no results."""
    try:
        db_path = str(get_project_root() / ".claude" / "scripts" / "library.db")
        init_db(db_path)
        payload = json.dumps({
            "query": query_text,
            "strategies": strategies,
            "timestamp": now_iso(),
        })
        emit_event(db_path, "knowledge:gap", payload, "researcher")
    except Exception as e:
        print(f"Warning: failed to emit gap event: {e}", file=sys.stderr)


def format_results(results: list[dict], fmt: str = "text") -> str:
    """Format results as JSON or human-readable text."""
    if fmt == "json":
        return json.dumps(results, indent=2, ensure_ascii=False)

    if not results:
        return "No results found."

    lines = []
    for r in results:
        score = r.get("relevance_score", 0)
        confidence = r.get("confidence_level", "low")
        lines.append(f"[{score:.3f}] {r.get('title', '?')} ({r.get('id', '?')[:8]}..)")
        lines.append(f"         confidence: {confidence}, maturity: {r.get('maturity', '?')}, type: {r.get('item_type', '?')}")
        if r.get("summary"):
            lines.append(f"         {r['summary']}")
        if r.get("tags"):
            tags_str = ", ".join(r["tags"]) if isinstance(r["tags"], list) else r["tags"]
            lines.append(f"         tags: {tags_str}")
        lines.append(f"         path: {r.get('file_path', '?')}")
        lines.append("")
    return "\n".join(lines)


def cmd_search(args):
    """Execute search based on provided flags."""
    root = get_project_root()
    nuggets_dir = root / "nuggets"
    inbox_dir = root / "inbox"

    results = []
    strategies = []

    if args.query:
        strategies.append("semantic")
        results = search_semantic(args.query, n=args.n)

        # Post-filter by keyword if provided
        if args.keyword:
            strategies.append("keyword")
            kw = args.keyword.lower()
            results = [
                r for r in results
                if kw in r.get("title", "").lower()
                or kw in r.get("summary", "").lower()
            ]
    elif args.tags and not args.query:
        strategies.append("tag")
        results = search_tags(
            [t.strip() for t in args.tags.split(",")],
            nuggets_dir, inbox_dir,
        )
        results = results[:args.n]
    elif args.keyword and not args.query:
        strategies.append("keyword")
        results = search_keyword(args.keyword, nuggets_dir, inbox_dir)
        results = results[:args.n]
    else:
        print("Error: provide at least --query, --tags, or --keyword", file=sys.stderr)
        sys.exit(1)

    # Post-filter by tags, maturity, type (applied after any search strategy)
    if args.tags and args.query:
        tag_set = set(t.strip().lower() for t in args.tags.split(","))
        results = [r for r in results if tag_set.intersection(
            set(t.lower() for t in r.get("tags", []))
        )]
    if args.maturity:
        results = [r for r in results if r.get("maturity") == args.maturity]
    if args.type:
        results = [r for r in results if r.get("item_type") == args.type]

    # Gap logging
    query_text = args.query or args.keyword or (args.tags if args.tags else "")
    if not results:
        _emit_gap_event(query_text, strategies)

    print(format_results(results, fmt=args.format))


def main():
    parser = argparse.ArgumentParser(description="Knowledge Library multi-strategy search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_search = subparsers.add_parser("search", help="Search the library")
    p_search.add_argument("--query", help="Semantic search query")
    p_search.add_argument("--tags", help="Comma-separated tags to filter by")
    p_search.add_argument("--keyword", help="Keyword search in title/summary/body")
    p_search.add_argument("--maturity", help="Filter by maturity level")
    p_search.add_argument("--type", choices=["raw", "nugget"], help="Filter by item type")
    p_search.add_argument("--n", type=int, default=10, help="Max results (default: 10)")
    p_search.add_argument("--format", choices=["json", "text"], default="text", help="Output format")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
