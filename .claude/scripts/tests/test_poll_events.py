import json
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from emit_event import emit_event
from poll_events import poll_events, mark_processed


class TestPollEvents:
    def test_poll_all(self, db_path):
        emit_event(db_path, "ingest:received", '{}', "a")
        emit_event(db_path, "entry:created", '{}', "b")
        events = poll_events(db_path, None, False, 100)
        assert len(events) == 2

    def test_filter_by_type(self, db_path):
        emit_event(db_path, "ingest:received", '{}', "a")
        emit_event(db_path, "entry:created", '{}', "b")
        events = poll_events(db_path, "ingest:received", False, 100)
        assert len(events) == 1
        assert events[0]["event_type"] == "ingest:received"

    def test_unprocessed_only(self, db_path):
        emit_event(db_path, "ingest:received", '{}', "a")
        mark_processed(db_path, [1], "test")
        emit_event(db_path, "entry:created", '{}', "b")
        events = poll_events(db_path, None, True, 100)
        assert len(events) == 1
        assert events[0]["event_type"] == "entry:created"

    def test_limit(self, db_path):
        for i in range(5):
            emit_event(db_path, "ingest:received", '{}', "a")
        events = poll_events(db_path, None, False, 3)
        assert len(events) == 3


class TestMarkProcessed:
    def test_marks_fields(self, db_path):
        emit_event(db_path, "ingest:received", '{}', "a")
        mark_processed(db_path, [1], "librarian")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM events WHERE id = 1").fetchone()
        assert row["processed"] == 1
        assert row["processed_by"] == "librarian"
        assert row["processed_at"] is not None
        conn.close()

    def test_empty_list(self, db_path):
        mark_processed(db_path, [], "test")  # Should not raise
