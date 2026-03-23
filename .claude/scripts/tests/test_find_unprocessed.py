import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, generate_uuid, now_iso
from find_unprocessed import find_unprocessed
from init_db import init_db
from emit_event import emit_event


class TestFindUnprocessed:
    def test_item_with_event_is_processed(self, tmp_project, db_path):
        """Item with a raw:catalogued event should be excluded (processed)."""
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        emit_event(db_path, "raw:catalogued", json.dumps({"id": item_id}), "test")
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox", db_path)
        assert len(result) == 0

    def test_item_in_chromadb_is_processed(self, tmp_project, db_path):
        """Item found in ChromaDB should be excluded (processed)."""
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        with patch("find_unprocessed._exists_in_chromadb", return_value=True):
            result = find_unprocessed(tmp_project / "inbox", db_path)
        assert len(result) == 0

    def test_item_with_neither_is_unprocessed(self, tmp_project, db_path):
        """Item with no event and not in ChromaDB should be unprocessed."""
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox", db_path)
        assert len(result) == 1
        assert result[0]["id"] == item_id

    def test_empty_inbox(self, tmp_project, db_path):
        """Empty inbox should return empty list."""
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox", db_path)
        assert result == []

    def test_no_id_is_unprocessed(self, tmp_project, db_path):
        """Item with no ID in frontmatter should be unprocessed."""
        (tmp_project / "inbox" / "no-id.md").write_text("---\ntitle: No ID\n---\nbody", encoding="utf-8")
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox", db_path)
        assert len(result) == 1
        assert result[0]["id"] is None

    def test_gitkeep_ignored(self, tmp_project, db_path):
        """The .gitkeep file should be ignored."""
        (tmp_project / "inbox" / ".gitkeep").touch()
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox", db_path)
        assert result == []
