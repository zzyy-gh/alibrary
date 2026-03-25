import sys
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, parse_frontmatter


class TestCmdIngest:
    def test_ingest_text(self, tmp_project):
        with patch("cli.get_project_root", return_value=tmp_project):
            from cli import cmd_ingest
            args = SimpleNamespace(url=None, file=None, text="Hello world", title="Test", type=None)
            cmd_ingest(args)

        files = list((tmp_project / "inbox").glob("*.md"))
        assert len(files) == 1
        fm, body = parse_frontmatter(files[0])
        assert fm["title"] == "Test"
        assert fm["id"] is not None
        assert body == "Hello world"

    def test_ingest_url(self, tmp_project):
        with patch("cli.get_project_root", return_value=tmp_project):
            from cli import cmd_ingest
            args = SimpleNamespace(url="https://example.com", file=None, text=None, title=None, type=None)
            cmd_ingest(args)

        files = list((tmp_project / "inbox").glob("*.md"))
        assert len(files) == 1
        fm, _ = parse_frontmatter(files[0])
        assert fm["source_url"] == "https://example.com"
