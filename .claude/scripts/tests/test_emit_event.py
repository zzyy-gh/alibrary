import json
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from emit_event import emit_event
from init_db import init_db


class TestEmitEvent:
    def test_valid_event(self, db_path):
        event_id = emit_event(db_path, "ingest:received", '{"path": "/test"}', "test-agent")
        assert isinstance(event_id, int)
        assert event_id > 0

    def test_event_stored(self, db_path):
        emit_event(db_path, "raw:catalogued", '{"id": "abc"}', "indexer")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM events WHERE id = 1").fetchone()
        assert row["event_type"] == "raw:catalogued"
        assert row["emitted_by"] == "indexer"
        assert row["processed"] == 0
        assert json.loads(row["payload"])["id"] == "abc"
        conn.close()

    def test_invalid_event_type(self, db_path):
        with pytest.raises(ValueError, match="Invalid event type"):
            emit_event(db_path, "bogus:type", '{}', "test")

    def test_invalid_json_payload(self, db_path):
        with pytest.raises(ValueError, match="not valid JSON"):
            emit_event(db_path, "ingest:received", "not json", "test")

    def test_multiple_events(self, db_path):
        id1 = emit_event(db_path, "ingest:received", '{}', "a")
        id2 = emit_event(db_path, "entry:created", '{}', "b")
        assert id2 > id1
