"""Emit an event to the event queue.

Usage: python .claude/scripts/emit_event.py --type EVENT_TYPE --payload JSON --emitter NAME [--db-path PATH]
"""

import argparse
import json
import sqlite3
import sys

from helpers import get_db_path, now_iso

VALID_EVENT_TYPES = [
    "ingest:received",
    "raw:catalogued",
    "entry:created",
    "entry:enriched",
    "entry:merged",
    "entry:consolidated",
    "entry:stale",
    "link:broken",
    "knowledge:gap",
    "review:needed",
    "intern:recommendation",
]


def emit_event(db_path: str, event_type: str, payload: str, emitter: str) -> int:
    if event_type not in VALID_EVENT_TYPES:
        raise ValueError(f"Invalid event type '{event_type}'. Must be one of: {', '.join(VALID_EVENT_TYPES)}")

    try:
        json.loads(payload)
    except json.JSONDecodeError as e:
        raise ValueError(f"Payload is not valid JSON: {e}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (event_type, payload, emitted_by, emitted_at) VALUES (?, ?, ?, ?)",
        (event_type, payload, emitter, now_iso()),
    )
    event_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return event_id


def main():
    parser = argparse.ArgumentParser(description="Emit an event to the queue.")
    parser.add_argument("--type", required=True, dest="event_type", help="Event type")
    parser.add_argument("--payload", required=True, help="JSON payload")
    parser.add_argument("--emitter", required=True, help="Name of the emitting agent")
    parser.add_argument("--db-path", default=str(get_db_path()), help="Path to SQLite database")
    args = parser.parse_args()

    try:
        event_id = emit_event(args.db_path, args.event_type, args.payload, args.emitter)
        print(f"Event {event_id} emitted: {args.event_type}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
