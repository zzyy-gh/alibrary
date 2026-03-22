import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, generate_uuid, now_iso
from find_unprocessed import find_unprocessed


class TestFindUnprocessed:
    def test_all_unprocessed(self, tmp_project):
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        result = find_unprocessed(tmp_project / "inbox", tmp_project / "relationships")
        assert len(result) == 1
        assert result[0]["id"] == item_id

    def test_processed_excluded(self, tmp_project):
        item_id = generate_uuid()
        write_frontmatter(tmp_project / "inbox" / "item.md", {"id": item_id, "title": "T"}, "body")
        rels = [{"source_id": "nugget-1", "target_id": item_id, "type": "derived-from"}]
        (tmp_project / "relationships" / "s.json").write_text(json.dumps(rels), encoding="utf-8")
        result = find_unprocessed(tmp_project / "inbox", tmp_project / "relationships")
        assert len(result) == 0

    def test_no_id(self, tmp_project):
        (tmp_project / "inbox" / "no-id.md").write_text("---\ntitle: No ID\n---\nbody", encoding="utf-8")
        result = find_unprocessed(tmp_project / "inbox", tmp_project / "relationships")
        assert len(result) == 1
        assert result[0]["id"] is None

    def test_empty_inbox(self, tmp_project):
        result = find_unprocessed(tmp_project / "inbox", tmp_project / "relationships")
        assert result == []

    def test_gitkeep_ignored(self, tmp_project):
        (tmp_project / "inbox" / ".gitkeep").touch()
        result = find_unprocessed(tmp_project / "inbox", tmp_project / "relationships")
        assert result == []
