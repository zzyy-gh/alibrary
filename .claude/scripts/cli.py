"""Knowledge Library CLI.

Ingest raw items and search the library.

Usage:
  python .claude/scripts/cli.py ingest --url URL [--title TITLE] [--type TYPE]
  python .claude/scripts/cli.py ingest --file PATH [--title TITLE] [--type TYPE]
  python .claude/scripts/cli.py ingest --text "content" [--title TITLE] [--type TYPE]
  python .claude/scripts/cli.py search --query "semantic query" [--tags TAG1,TAG2] [--keyword TERM]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import (
    generate_uuid,
    get_project_root,
    now_iso,
    parse_frontmatter,
    slugify,
    unique_filepath,
    write_frontmatter,
)
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

    print(f"Ingested: {fpath}")
    print(f"ID:       {item_id}")
    print(f"Title:    {title}")


def cmd_search(args):
    from retriever import search_semantic, search_tags, search_keyword, format_results

    root = get_project_root()
    nuggets_dir = root / "nuggets"
    inbox_dir = root / "inbox"

    results = []

    if args.query:
        results = search_semantic(args.query, n=args.n)

        # Post-filter by tags
        if args.tags:
            tag_set = set(t.strip().lower() for t in args.tags.split(","))
            results = [r for r in results if tag_set.intersection(
                set(t.lower() for t in r.get("tags", []))
            )]

        # Post-filter by keyword
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
    elif args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
