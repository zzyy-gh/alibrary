import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, generate_uuid, now_iso
from retriever import _to_result, format_results, search_tags, search_keyword


class TestToResult:
    def test_basic(self):
        item = {
            "frontmatter": {"id": "abc", "title": "Test", "maturity": "summary", "summary": "A summary", "tags": ["t1"]},
            "body": "content",
            "path": "/test.md",
            "item_type": "nugget",
        }
        result = _to_result(item, relevance_score=0.8)
        assert result["id"] == "abc"
        assert result["title"] == "Test"
        assert result["maturity"] == "summary"
        assert result["relevance_score"] == 0.8
        assert result["tags"] == ["t1"]

class TestFormatResults:
    def test_json(self):
        results = [{"id": "a", "title": "T", "maturity": "stub",
                     "relevance_score": 0.5, "summary": "", "tags": ["x"], "file_path": "/f", "item_type": "nugget"}]
        output = format_results(results, "json")
        parsed = json.loads(output)
        assert len(parsed) == 1
        assert parsed[0]["id"] == "a"

    def test_text(self):
        results = [{"id": "abc12345", "title": "Test", "maturity": "stub",
                     "relevance_score": 0.5, "summary": "Sum", "tags": ["x"], "file_path": "/f", "item_type": "nugget"}]
        output = format_results(results, "text")
        assert "Test" in output
        assert "0.500" in output

    def test_empty(self):
        assert format_results([], "text") == "No results found."


class TestSearchTags:
    def test_match(self, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "N", "maturity": "stub", "tags": ["alpha", "beta"]}, "body")
        results = search_tags(["alpha"], tmp_project / "nuggets", tmp_project / "inbox")
        assert len(results) == 1
        assert results[0]["id"] == "n1"

    def test_no_match(self, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "N", "tags": ["alpha"]}, "body")
        results = search_tags(["gamma"], tmp_project / "nuggets", tmp_project / "inbox")
        assert len(results) == 0

    def test_partial_match_scored(self, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "N", "tags": ["alpha", "beta"]}, "body")
        results = search_tags(["alpha", "gamma"], tmp_project / "nuggets", tmp_project / "inbox")
        assert len(results) == 1
        assert results[0]["relevance_score"] == 0.5  # 1 of 2 tags matched


class TestSearchKeyword:
    def test_title_match(self, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "Agent Patterns", "maturity": "stub"}, "body content")
        results = search_keyword("agent", tmp_project / "nuggets", tmp_project / "inbox")
        assert len(results) == 1
        assert results[0]["relevance_score"] == 1.0

    def test_body_match(self, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "Other", "maturity": "stub"}, "body with agent keyword")
        results = search_keyword("agent", tmp_project / "nuggets", tmp_project / "inbox")
        assert len(results) == 1
        assert results[0]["relevance_score"] == 0.4

    def test_no_match(self, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "Other", "maturity": "stub"}, "nothing here")
        results = search_keyword("agent", tmp_project / "nuggets", tmp_project / "inbox")
        assert results == []


class TestSearchSemantic:
    @patch("embeddings.search_similar", return_value=[{"id": "n1", "relevance_score": 0.8}])
    def test_resolves_metadata(self, mock_search, tmp_project):
        write_frontmatter(tmp_project / "nuggets" / "n.md",
            {"id": "n1", "title": "Nugget", "maturity": "summary", "summary": "S", "tags": ["t"]}, "body")

        with patch("retriever.get_project_root", return_value=tmp_project):
            from retriever import search_semantic
            results = search_semantic("query", n=5)
            assert len(results) == 1
            assert results[0]["title"] == "Nugget"
            assert results[0]["maturity"] == "summary"

    @patch("embeddings.search_similar", return_value=[])
    def test_empty_results(self, mock_search):
        from retriever import search_semantic
        results = search_semantic("query")
        assert results == []
