import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, generate_uuid, now_iso
from find_unprocessed import find_unprocessed


class TestFindUnprocessed:
    def test_item_in_chromadb_is_processed(self, tmp_project):
        """Item found in ChromaDB should be excluded (processed)."""
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        with patch("find_unprocessed._exists_in_chromadb", return_value=True):
            result = find_unprocessed(tmp_project / "inbox")
        assert len(result) == 0

    def test_item_not_in_chromadb_is_unprocessed(self, tmp_project):
        """Item not in ChromaDB should be unprocessed."""
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox")
        assert len(result) == 1
        assert result[0]["id"] == item_id

    def test_empty_inbox(self, tmp_project):
        """Empty inbox should return empty list."""
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox")
        assert result == []

    def test_no_id_is_unprocessed(self, tmp_project):
        """Item with no ID in frontmatter should be unprocessed."""
        (tmp_project / "inbox" / "no-id.md").write_text("---\ntitle: No ID\n---\nbody", encoding="utf-8")
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox")
        assert len(result) == 1
        assert result[0]["id"] is None

    def test_gitkeep_ignored(self, tmp_project):
        """The .gitkeep file should be ignored."""
        (tmp_project / "inbox" / ".gitkeep").touch()
        with patch("find_unprocessed._exists_in_chromadb", return_value=False):
            result = find_unprocessed(tmp_project / "inbox")
        assert result == []
