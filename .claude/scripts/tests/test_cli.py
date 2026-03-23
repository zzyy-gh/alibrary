import sys
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, parse_frontmatter


class TestCmdIngest:
    def test_ingest_text(self, tmp_project, db_path):
        with patch("cli.get_project_root", return_value=tmp_project), \
             patch("cli.init_db"), \
             patch("cli.emit_event", return_value=1):
            from cli import cmd_ingest
            args = SimpleNamespace(url=None, file=None, text="Hello world", title="Test", type=None)
            cmd_ingest(args)

        files = list((tmp_project / "inbox").glob("*.md"))
        assert len(files) == 1
        fm, body = parse_frontmatter(files[0])
        assert fm["title"] == "Test"
        assert fm["id"] is not None
        assert body == "Hello world"

    def test_ingest_url(self, tmp_project, db_path):
        with patch("cli.get_project_root", return_value=tmp_project), \
             patch("cli.init_db"), \
             patch("cli.emit_event", return_value=1):
            from cli import cmd_ingest
            args = SimpleNamespace(url="https://example.com", file=None, text=None, title=None, type=None)
            cmd_ingest(args)

        files = list((tmp_project / "inbox").glob("*.md"))
        assert len(files) == 1
        fm, _ = parse_frontmatter(files[0])
        assert fm["source_url"] == "https://example.com"


class TestCmdQuery:
    def test_list_all(self, tmp_project, capsys):
        write_frontmatter(tmp_project / "nuggets" / "n1.md",
            {"id": "n1", "title": "Nugget One", "maturity": "summary", "tags": ["test"]}, "body")

        with patch("cli.get_project_root", return_value=tmp_project):
            from cli import cmd_query
            args = SimpleNamespace(tag=None, keyword=None, list=True)
            cmd_query(args)

        output = capsys.readouterr().out
        assert "Nugget One" in output

    def test_filter_by_tag(self, tmp_project, capsys):
        write_frontmatter(tmp_project / "nuggets" / "n1.md",
            {"id": "n1", "title": "Alpha", "maturity": "stub", "tags": ["keep"]}, "body")
        write_frontmatter(tmp_project / "nuggets" / "n2.md",
            {"id": "n2", "title": "Beta", "maturity": "stub", "tags": ["skip"]}, "body")

        with patch("cli.get_project_root", return_value=tmp_project):
            from cli import cmd_query
            args = SimpleNamespace(tag=["keep"], keyword=None, list=False)
            cmd_query(args)

        output = capsys.readouterr().out
        assert "Alpha" in output
        assert "Beta" not in output

    def test_filter_by_keyword(self, tmp_project, capsys):
        write_frontmatter(tmp_project / "nuggets" / "n1.md",
            {"id": "n1", "title": "Agent Patterns", "maturity": "stub"}, "body")
        write_frontmatter(tmp_project / "nuggets" / "n2.md",
            {"id": "n2", "title": "Other", "maturity": "stub"}, "body")

        with patch("cli.get_project_root", return_value=tmp_project):
            from cli import cmd_query
            args = SimpleNamespace(tag=None, keyword="agent", list=False)
            cmd_query(args)

        output = capsys.readouterr().out
        assert "Agent Patterns" in output
        assert "Other" not in output


