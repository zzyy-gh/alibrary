"""Poll events from the event queue.

Usage: python .claude/scripts/poll_events.py [--type TYPE] [--unprocessed] [--mark-processed AGENT] [--limit N] [--db-path PATH]
"""

import argparse
import json
import sqlite3
import sys

from helpers import get_db_path, now_iso


def poll_events(db_path: str, event_type: str | None, unprocessed: bool, limit: int) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    conditions = []
    params = []

    if unprocessed:
        conditions.append("processed = 0")
    if event_type:
        conditions.append("event_type = ?")
        params.append(event_type)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT * FROM events {where} ORDER BY id ASC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def mark_processed(db_path: str, event_ids: list[int], agent: str) -> None:
    if not event_ids:
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    placeholders = ",".join("?" for _ in event_ids)
    cursor.execute(
        f"UPDATE events SET processed = 1, processed_at = ?, processed_by = ? WHERE id IN ({placeholders})",
        [now_iso(), agent] + event_ids,
    )
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Poll events from the queue.")
    parser.add_argument("--type", dest="event_type", help="Filter by event type")
    parser.add_argument("--unprocessed", action="store_true", default=True, help="Only unprocessed events (default)")
    parser.add_argument("--all", action="store_true", help="Include processed events")
    parser.add_argument("--mark-processed", dest="mark_agent", help="Mark returned events as processed by AGENT")
    parser.add_argument("--limit", type=int, default=100, help="Max events to return (default 100)")
    parser.add_argument("--db-path", default=str(get_db_path()), help="Path to SQLite database")
    args = parser.parse_args()

    unprocessed = not args.all

    try:
        events = poll_events(args.db_path, args.event_type, unprocessed, args.limit)
        print(json.dumps(events, indent=2))

        if args.mark_agent and events:
            event_ids = [e["id"] for e in events]
            mark_processed(args.db_path, event_ids, args.mark_agent)
            print(f"Marked {len(event_ids)} event(s) as processed by {args.mark_agent}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
