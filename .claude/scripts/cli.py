"""Knowledge Library CLI.

Ingest raw items, query nuggets, and trace provenance.

Usage:
  python .claude/scripts/cli.py ingest --url URL [--title TITLE] [--type TYPE]
  python .claude/scripts/cli.py ingest --file PATH [--title TITLE] [--type TYPE]
  python .claude/scripts/cli.py ingest --text "content" [--title TITLE] [--type TYPE]
  python .claude/scripts/cli.py query --list
  python .claude/scripts/cli.py query --tag TAG [--tag TAG2]
  python .claude/scripts/cli.py query --keyword TERM
  python .claude/scripts/cli.py trace NUGGET_ID
"""

import argparse
import json
import sys
from pathlib import Path

from helpers import (
    generate_uuid,
    get_project_root,
    load_all_relationships,
    now_iso,
    parse_frontmatter,
    slugify,
    unique_filepath,
    write_frontmatter,
)
from emit_event import emit_event
from init_db import init_db


VALID_SOURCE_TYPES = ["article", "documentation", "video", "code", "conversation", "manual", "snippet"]


def cmd_ingest(args):
    root = get_project_root()
    inbox = root / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    # Determine content and source_url
    body = ""
    source_url = None

    if args.url:
        source_url = args.url
        body = args.url
    elif args.file:
        src = Path(args.file)
        if not src.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        body = src.read_text(encoding="utf-8")
    elif args.text:
        body = args.text
    else:
        print("Error: provide --url, --file, or --text", file=sys.stderr)
        sys.exit(1)

    # Build frontmatter
    item_id = generate_uuid()
    title = args.title or (args.url if args.url else Path(args.file).stem if args.file else "Untitled")
    source_type = args.type if args.type in VALID_SOURCE_TYPES else None

    frontmatter = {
        "id": item_id,
        "title": title,
        "created_at": now_iso(),
        "created_by": "cli",
    }
    if source_url:
        frontmatter["source_url"] = source_url
    if source_type:
        frontmatter["source_type"] = source_type
    if args.file:
        frontmatter["artifact_path"] = args.file

    # Write file with slugified title
    slug = slugify(title)
    fpath = unique_filepath(inbox, slug)
    write_frontmatter(fpath, frontmatter, body)

    # Emit event
    db_path = str(get_project_root() / ".claude" / "scripts" / "library.db")
    try:
        init_db(db_path)
        emit_event(
            db_path,
            "ingest:received",
            json.dumps({"path": str(fpath), "type": source_type, "id": item_id}),
            "cli",
        )
    except Exception as e:
        print(f"Warning: event emission failed: {e}", file=sys.stderr)

    print(f"Ingested: {fpath}")
    print(f"ID:       {item_id}")
    print(f"Title:    {title}")


def cmd_query(args):
    root = get_project_root()
    nuggets_dir = root / "nuggets"

    if not nuggets_dir.is_dir():
        print("No nuggets directory found.")
        return

    nugget_files = sorted(nuggets_dir.glob("*.md"))
    if not nugget_files:
        print("No nuggets found.")
        return

    # Load all nuggets
    nuggets = []
    for fpath in nugget_files:
        if fpath.name == ".gitkeep":
            continue
        try:
            fm, body = parse_frontmatter(fpath)
            nuggets.append({"frontmatter": fm, "body": body, "path": str(fpath)})
        except Exception:
            continue

    if not nuggets:
        print("No nuggets found.")
        return

    # Filter
    results = nuggets

    if args.tag:
        tags_needed = set(t.lower() for t in args.tag)
        results = [
            n for n in results
            if tags_needed.issubset(set(t.lower() for t in n["frontmatter"].get("tags", [])))
        ]

    if args.keyword:
        kw = args.keyword.lower()
        results = [
            n for n in results
            if kw in n["frontmatter"].get("title", "").lower()
            or kw in n["frontmatter"].get("summary", "").lower()
            or kw in n["body"].lower()
        ]

    if not results:
        print("No matching nuggets found.")
        return

    # Display
    for n in results:
        fm = n["frontmatter"]
        print(f"[{fm.get('maturity', '?'):>8}] {fm.get('id', '?')[:8]}..  {fm.get('title', 'Untitled')}")
        if fm.get("summary"):
            print(f"           {fm['summary']}")
        if fm.get("tags"):
            print(f"           tags: {', '.join(fm['tags'])}")
        print()


def cmd_trace(args):
    root = get_project_root()
    nugget_id = args.nugget_id

    # Find the nugget
    nuggets_dir = root / "nuggets"
    nugget_file = None
    for fpath in nuggets_dir.glob("*.md"):
        try:
            fm, _ = parse_frontmatter(fpath)
            if fm.get("id") == nugget_id or fm.get("id", "").startswith(nugget_id):
                nugget_file = fpath
                nugget_id = fm["id"]  # resolve partial ID
                break
        except Exception:
            continue

    if not nugget_file:
        print(f"Nugget not found: {nugget_id}", file=sys.stderr)
        sys.exit(1)

    fm, _ = parse_frontmatter(nugget_file)
    print(f"Nugget: {fm.get('title', 'Untitled')}")
    print(f"ID:     {nugget_id}")
    print(f"Maturity: {fm.get('maturity', '?')}")
    print()

    # Load relationships
    relationships = load_all_relationships()
    derived = [r for r in relationships if r.get("source_id") == nugget_id and r.get("type") == "derived-from"]

    if not derived:
        print("No provenance relationships found.")
        return

    print("Derived from:")
    for rel in derived:
        target_id = rel.get("target_id", "?")
        note = rel.get("note", "")

        # Try to find the source item
        source_title = target_id[:8] + ".."
        for d in [root / "inbox", root / "nuggets"]:
            for fpath in d.glob("*.md"):
                try:
                    sfm, _ = parse_frontmatter(fpath)
                    if sfm.get("id") == target_id:
                        source_title = sfm.get("title", source_title)
                        break
                except Exception:
                    continue

        print(f"  → {source_title} ({target_id[:8]}..)")
        if note:
            print(f"    note: {note}")


def cmd_search(args):
    from researcher import search_semantic, search_tags, search_keyword, format_results

    root = get_project_root()
    nuggets_dir = root / "nuggets"
    inbox_dir = root / "inbox"

    results = []

    if args.query:
        where = {}
        if args.tags:
            tag_list = [t.strip() for t in args.tags.split(",")]
            if len(tag_list) == 1:
                where["tags"] = {"$contains": tag_list[0]}
            else:
                where["$and"] = [{"tags": {"$contains": t}} for t in tag_list]

        results = search_semantic(args.query, n=args.n, where=where if where else None)

        if args.keyword:
            kw = args.keyword.lower()
            results = [
                r for r in results
                if kw in r.get("title", "").lower()
                or kw in r.get("summary", "").lower()
            ]
    elif args.tags:
        tag_list = [t.strip() for t in args.tags.split(",")]
        results = search_tags(tag_list, nuggets_dir, inbox_dir)
        results = results[:args.n]
    elif args.keyword:
        results = search_keyword(args.keyword, nuggets_dir, inbox_dir)
        results = results[:args.n]
    else:
        print("Error: provide at least --query, --tags, or --keyword", file=sys.stderr)
        sys.exit(1)

    print(format_results(results, fmt=args.format))


def main():
    parser = argparse.ArgumentParser(description="Knowledge Library CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ingest
    p_ingest = subparsers.add_parser("ingest", help="Add a raw item to inbox")
    p_ingest.add_argument("--url", help="URL to ingest")
    p_ingest.add_argument("--file", help="File path to ingest")
    p_ingest.add_argument("--text", help="Text content to ingest")
    p_ingest.add_argument("--title", help="Title for the raw item")
    p_ingest.add_argument("--type", choices=VALID_SOURCE_TYPES, help="Source type")

    # query
    p_query = subparsers.add_parser("query", help="Search nuggets")
    p_query.add_argument("--tag", action="append", help="Filter by tag (can repeat)")
    p_query.add_argument("--keyword", help="Search by keyword in title/summary/body")
    p_query.add_argument("--list", action="store_true", help="List all nuggets")

    # trace
    p_trace = subparsers.add_parser("trace", help="Show provenance for a nugget")
    p_trace.add_argument("nugget_id", help="Nugget ID (full or prefix)")

    # search
    p_search = subparsers.add_parser("search", help="Multi-strategy search")
    p_search.add_argument("--query", help="Semantic search query")
    p_search.add_argument("--tags", help="Comma-separated tags to filter by")
    p_search.add_argument("--keyword", help="Keyword search in title/summary/body")
    p_search.add_argument("--n", type=int, default=10, help="Max results (default: 10)")
    p_search.add_argument("--format", choices=["json", "text"], default="text", help="Output format")

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "query":
        if not args.tag and not args.keyword and not args.list:
            print("Error: provide --tag, --keyword, or --list", file=sys.stderr)
            sys.exit(1)
        cmd_query(args)
    elif args.command == "trace":
        cmd_trace(args)
    elif args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
