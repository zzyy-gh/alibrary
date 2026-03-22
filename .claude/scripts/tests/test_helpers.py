import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import helpers


class TestSlugify:
    def test_normal(self):
        assert helpers.slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert helpers.slugify("Hello! @World#") == "hello-world"

    def test_multiple_spaces(self):
        assert helpers.slugify("hello   world") == "hello-world"

    def test_leading_trailing(self):
        assert helpers.slugify("  hello  ") == "hello"

    def test_empty(self):
        assert helpers.slugify("") == "untitled"

    def test_underscores(self):
        assert helpers.slugify("hello_world_test") == "hello-world-test"

    def test_unicode(self):
        result = helpers.slugify("cafe resume")
        assert "caf" in result


class TestGenerateUuid:
    def test_format(self):
        uid = helpers.generate_uuid()
        assert len(uid) == 36
        assert uid.count("-") == 4

    def test_unique(self):
        a = helpers.generate_uuid()
        b = helpers.generate_uuid()
        assert a != b


class TestNowIso:
    def test_format(self):
        result = helpers.now_iso()
        assert result.endswith("Z")
        assert "T" in result

    def test_length(self):
        result = helpers.now_iso()
        assert len(result) == 20  # YYYY-MM-DDTHH:MM:SSZ


class TestTodayDate:
    def test_format(self):
        result = helpers.today_date()
        assert len(result) == 10  # YYYY-MM-DD
        assert result.count("-") == 2


class TestUniqueFilepath:
    def test_no_collision(self, tmp_path):
        result = helpers.unique_filepath(tmp_path, "test")
        assert result == tmp_path / "test.md"

    def test_collision(self, tmp_path):
        (tmp_path / "test.md").touch()
        result = helpers.unique_filepath(tmp_path, "test")
        assert result == tmp_path / "test-2.md"

    def test_multiple_collisions(self, tmp_path):
        (tmp_path / "test.md").touch()
        (tmp_path / "test-2.md").touch()
        result = helpers.unique_filepath(tmp_path, "test")
        assert result == tmp_path / "test-3.md"

    def test_custom_extension(self, tmp_path):
        result = helpers.unique_filepath(tmp_path, "test", ext=".json")
        assert result == tmp_path / "test.json"


class TestParseFrontmatter:
    def test_valid(self, tmp_path):
        fpath = tmp_path / "test.md"
        fpath.write_text("---\ntitle: Hello\ntags:\n  - a\n  - b\n---\n\nBody content.", encoding="utf-8")
        fm, body = helpers.parse_frontmatter(fpath)
        assert fm["title"] == "Hello"
        assert fm["tags"] == ["a", "b"]
        assert body == "Body content."

    def test_no_frontmatter(self, tmp_path):
        fpath = tmp_path / "test.md"
        fpath.write_text("Just plain text.", encoding="utf-8")
        fm, body = helpers.parse_frontmatter(fpath)
        assert fm == {}
        assert body == "Just plain text."

    def test_empty_file(self, tmp_path):
        fpath = tmp_path / "test.md"
        fpath.write_text("", encoding="utf-8")
        fm, body = helpers.parse_frontmatter(fpath)
        assert fm == {}
        assert body == ""


class TestWriteFrontmatter:
    def test_roundtrip(self, tmp_path):
        fpath = tmp_path / "test.md"
        fm = {"title": "Test", "tags": ["a", "b"]}
        body = "Some body text."
        helpers.write_frontmatter(fpath, fm, body)
        parsed_fm, parsed_body = helpers.parse_frontmatter(fpath)
        assert parsed_fm["title"] == "Test"
        assert parsed_fm["tags"] == ["a", "b"]
        assert parsed_body == "Some body text."


class TestLoadAllRelationships:
    def test_multiple_files(self, tmp_path):
        r1 = [{"source_id": "a", "target_id": "b", "type": "derived-from"}]
        r2 = [{"source_id": "c", "target_id": "d", "type": "contradicts"}]
        (tmp_path / "s1.json").write_text(json.dumps(r1), encoding="utf-8")
        (tmp_path / "s2.json").write_text(json.dumps(r2), encoding="utf-8")
        result = helpers.load_all_relationships(tmp_path)
        assert len(result) == 2

    def test_malformed_json(self, tmp_path):
        (tmp_path / "bad.json").write_text("not json", encoding="utf-8")
        result = helpers.load_all_relationships(tmp_path)
        assert result == []

    def test_empty_dir(self, tmp_path):
        result = helpers.load_all_relationships(tmp_path)
        assert result == []

    def test_single_dict(self, tmp_path):
        (tmp_path / "s.json").write_text(json.dumps({"source_id": "a", "target_id": "b"}), encoding="utf-8")
        result = helpers.load_all_relationships(tmp_path)
        assert len(result) == 1


class TestSaveRelationships:
    def test_new_file(self, tmp_path):
        rels = [{"source_id": "a", "target_id": "b", "type": "derived-from"}]
        fpath = helpers.save_relationships(rels, "session-1", tmp_path)
        assert fpath.exists()
        data = json.loads(fpath.read_text(encoding="utf-8"))
        assert len(data) == 1

    def test_append(self, tmp_path):
        r1 = [{"source_id": "a", "target_id": "b"}]
        r2 = [{"source_id": "c", "target_id": "d"}]
        helpers.save_relationships(r1, "session-1", tmp_path)
        helpers.save_relationships(r2, "session-1", tmp_path)
        fpath = tmp_path / "session-1.json"
        data = json.loads(fpath.read_text(encoding="utf-8"))
        assert len(data) == 2
