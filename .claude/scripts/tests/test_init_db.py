import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from init_db import init_db


class TestInitDb:
    def test_creates_table(self, tmp_path):
        path = str(tmp_path / "test.db")
        init_db(path)
        conn = sqlite3.connect(path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_creates_index(self, tmp_path):
        path = str(tmp_path / "test.db")
        init_db(path)
        conn = sqlite3.connect(path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_events_unprocessed'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_idempotent(self, tmp_path):
        path = str(tmp_path / "test.db")
        init_db(path)
        init_db(path)  # Should not raise
        conn = sqlite3.connect(path)
        cursor = conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='events'")
        assert cursor.fetchone()[0] == 1
        conn.close()

    def test_table_schema(self, tmp_path):
        path = str(tmp_path / "test.db")
        init_db(path)
        conn = sqlite3.connect(path)
        cursor = conn.execute("PRAGMA table_info(events)")
        columns = {row[1] for row in cursor.fetchall()}
        expected = {"id", "event_type", "payload", "emitted_by", "emitted_at", "processed", "processed_at", "processed_by"}
        assert columns == expected
        conn.close()
