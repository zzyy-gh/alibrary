"""Find raw items in /inbox/ that have not been processed yet.

An item is considered processed if:
  1. It has a 'raw:catalogued' event in the SQLite event DB, OR
  2. Its ID exists in the ChromaDB vector store.

Usage: python .claude/scripts/find_unprocessed.py [--inbox-path PATH]
"""

import argparse
import json
import sqlite3
import sys

from helpers import get_project_root, get_db_path, parse_frontmatter


def _has_catalogued_event(db_path: str, item_id: str) -> bool:
    """Check if item_id has a raw:catalogued event in the SQLite DB."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM events WHERE event_type = 'raw:catalogued' AND payload LIKE ? LIMIT 1",
            (f'%{item_id}%',),
        )
        found = cursor.fetchone() is not None
        conn.close()
        return found
    except Exception:
        return False


def _exists_in_chromadb(item_id: str) -> bool:
    """Check if item_id exists in the ChromaDB vector store."""
    try:
        from embeddings import _get_chroma_collection
        collection = _get_chroma_collection()
        result = collection.get(ids=[item_id])
        return bool(result and result["ids"])
    except Exception:
        return False


def find_unprocessed(inbox_dir, db_path: str | None = None) -> list[dict]:
    """Return list of {id, file_path} for raw items not yet processed."""
    from pathlib import Path

    inbox_dir = Path(inbox_dir)
    if not inbox_dir.is_dir():
        return []

    if db_path is None:
        db_path = str(get_db_path())

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
            # Primary check: event DB
            if _has_catalogued_event(db_path, item_id):
                continue
            # Fallback check: ChromaDB
            if _exists_in_chromadb(item_id):
                continue
            # Neither — unprocessed
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
