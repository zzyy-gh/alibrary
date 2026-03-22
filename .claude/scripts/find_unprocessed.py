"""Find raw items in /inbox/ that have no derived-from relationship.

These are items that haven't been processed by the indexer yet.

Usage: python .claude/scripts/find_unprocessed.py [--inbox-path PATH] [--relationships-path PATH]
"""

import argparse
import json
import sys

from helpers import get_project_root, load_all_relationships, parse_frontmatter


def find_unprocessed(inbox_dir, rel_dir) -> list[dict]:
    """Return list of {id, file_path} for raw items with no derived-from target edge."""
    from pathlib import Path

    inbox_dir = Path(inbox_dir)
    if not inbox_dir.is_dir():
        return []

    # Collect all target_ids from derived-from relationships
    relationships = load_all_relationships(rel_dir)
    processed_ids = {
        r["target_id"]
        for r in relationships
        if r.get("type") == "derived-from" and "target_id" in r
    }

    # Scan inbox for items not in processed set
    unprocessed = []
    for fpath in sorted(inbox_dir.glob("*.md")):
        if fpath.name == ".gitkeep":
            continue
        try:
            fm, _ = parse_frontmatter(fpath)
            item_id = fm.get("id")
            if item_id and item_id not in processed_ids:
                unprocessed.append({"id": item_id, "file_path": str(fpath)})
            elif not item_id:
                # No ID means never catalogued — definitely unprocessed
                unprocessed.append({"id": None, "file_path": str(fpath)})
        except Exception:
            unprocessed.append({"id": None, "file_path": str(fpath)})

    return unprocessed


def main():
    root = get_project_root()
    parser = argparse.ArgumentParser(description="Find unprocessed raw items in inbox.")
    parser.add_argument("--inbox-path", default=str(root / "inbox"), help="Path to inbox directory")
    parser.add_argument("--relationships-path", default=str(root / "relationships"), help="Path to relationships directory")
    args = parser.parse_args()

    results = find_unprocessed(args.inbox_path, args.relationships_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
