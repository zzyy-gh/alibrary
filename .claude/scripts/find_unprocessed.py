"""Find raw items in /inbox/ that have not been processed yet.

An item is considered processed if its ID exists in the ChromaDB vector store.

Usage: python .claude/scripts/find_unprocessed.py [--inbox-path PATH]
"""

import argparse
import json
import sys

from helpers import get_project_root, parse_frontmatter


def _exists_in_chromadb(item_id: str) -> bool:
    """Check if item_id exists in the ChromaDB vector store."""
    try:
        from embeddings import _get_chroma_collection
        collection = _get_chroma_collection()
        result = collection.get(ids=[item_id])
        return bool(result and result["ids"])
    except Exception:
        return False


def find_unprocessed(inbox_dir) -> list[dict]:
    """Return list of {id, file_path} for raw items not yet processed."""
    from pathlib import Path

    inbox_dir = Path(inbox_dir)
    if not inbox_dir.is_dir():
        return []

    unprocessed = []
    for fpath in sorted(inbox_dir.glob("*.md")):
        if fpath.name == ".gitkeep":
            continue
        try:
            fm, _ = parse_frontmatter(fpath)
            item_id = fm.get("id")
            if not item_id:
                # No ID means never catalogued — definitely unprocessed
                unprocessed.append({"id": None, "file_path": str(fpath)})
                continue
            if _exists_in_chromadb(item_id):
                continue
            # Not in ChromaDB — unprocessed
            unprocessed.append({"id": item_id, "file_path": str(fpath)})
        except Exception:
            unprocessed.append({"id": None, "file_path": str(fpath)})

    return unprocessed


def main():
    root = get_project_root()
    parser = argparse.ArgumentParser(description="Find unprocessed raw items in inbox.")
    parser.add_argument("--inbox-path", default=str(root / "inbox"), help="Path to inbox directory")
    args = parser.parse_args()

    results = find_unprocessed(args.inbox_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
