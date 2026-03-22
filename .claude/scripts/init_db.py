"""Initialize the SQLite event queue database.

Creates the events table and index. Idempotent — safe to run multiple times.

Usage: python .claude/scripts/init_db.py [--db-path PATH]
"""

import argparse
import sqlite3
import sys

from helpers import get_db_path


def init_db(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type   TEXT    NOT NULL,
            payload      TEXT    NOT NULL,
            emitted_by   TEXT    NOT NULL,
            emitted_at   TEXT    NOT NULL,
            processed    INTEGER NOT NULL DEFAULT 0,
            processed_at TEXT    DEFAULT NULL,
            processed_by TEXT    DEFAULT NULL
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_unprocessed
        ON events (event_type, processed)
        WHERE processed = 0
    """)

    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Initialize the event queue database.")
    parser.add_argument("--db-path", default=str(get_db_path()), help="Path to SQLite database")
    args = parser.parse_args()

    try:
        init_db(args.db_path)
        print(f"Database initialized at {args.db_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
