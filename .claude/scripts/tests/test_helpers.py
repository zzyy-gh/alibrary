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


class TestResolveId:
    def _create_item(self, directory, item_id, title):
        """Helper: write a minimal MD file with frontmatter."""
        fpath = directory / f"{title.lower().replace(' ', '-')}.md"
        fpath.write_text(
            f"---\nid: {item_id}\ntitle: {title}\n---\n\nBody.",
            encoding="utf-8",
        )
        return fpath

    def test_by_full_uuid(self, tmp_path):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        self._create_item(inbox, "aaaa-bbbb-cccc", "Test Item")
        result = helpers.resolve_id("aaaa-bbbb-cccc", project_root=tmp_path)
        assert result is not None
        assert result["id"] == "aaaa-bbbb-cccc"
        assert result["title"] == "Test Item"
        assert result["item_type"] == "raw"

    def test_by_uuid_prefix(self, tmp_path):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        self._create_item(inbox, "aaaa-bbbb-cccc", "Test Item")
        result = helpers.resolve_id("aaaa", project_root=tmp_path)
        assert result is not None
        assert result["id"] == "aaaa-bbbb-cccc"

    def test_by_title(self, tmp_path):
        nuggets = tmp_path / "nuggets"
        nuggets.mkdir()
        self._create_item(nuggets, "xxxx-yyyy", "Agent Composition Rules")
        result = helpers.resolve_id("Composition Rules", project_root=tmp_path)
        assert result is not None
        assert result["title"] == "Agent Composition Rules"
        assert result["item_type"] == "nugget"

    def test_nonexistent(self, tmp_path):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        result = helpers.resolve_id("nonexistent", project_root=tmp_path)
        assert result is None

    def test_ambiguous(self, tmp_path):
        nuggets = tmp_path / "nuggets"
        nuggets.mkdir()
        self._create_item(nuggets, "aaaa-1111", "Agent Alpha")
        self._create_item(nuggets, "aaaa-2222", "Agent Beta")
        # Both UUIDs start with "aaaa" — ambiguous
        result = helpers.resolve_id("aaaa", project_root=tmp_path)
        assert result is None


