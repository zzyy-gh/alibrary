import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from graph_explore import build_graph, traverse, format_text


class TestBuildGraph:
    def test_basic(self):
        rels = [
            {"source_id": "a", "target_id": "b", "type": "derived-from", "note": "test"},
        ]
        graph = build_graph(rels)
        assert "a" in graph
        assert "b" in graph
        # a should have outgoing to b
        a_neighbors = [n for n in graph["a"] if n["neighbor_id"] == "b"]
        assert len(a_neighbors) == 1
        assert a_neighbors[0]["direction"] == "outgoing"
        # b should have incoming from a
        b_neighbors = [n for n in graph["b"] if n["neighbor_id"] == "a"]
        assert len(b_neighbors) == 1
        assert b_neighbors[0]["direction"] == "incoming"

    def test_empty(self):
        graph = build_graph([])
        assert graph == {}

    def test_multiple_edges(self):
        rels = [
            {"source_id": "a", "target_id": "b", "type": "derived-from"},
            {"source_id": "a", "target_id": "c", "type": "contradicts"},
        ]
        graph = build_graph(rels)
        assert len(graph["a"]) == 2


class TestTraverse:
    def test_one_hop(self):
        rels = [
            {"source_id": "a", "target_id": "b", "type": "derived-from"},
            {"source_id": "b", "target_id": "c", "type": "derived-from"},
        ]
        graph = build_graph(rels)
        result = traverse(graph, "a", max_hops=1)
        node_ids = {n["id"] for n in result["nodes"]}
        assert "a" in node_ids
        assert "b" in node_ids
        assert "c" not in node_ids

    def test_two_hops(self):
        rels = [
            {"source_id": "a", "target_id": "b", "type": "derived-from"},
            {"source_id": "b", "target_id": "c", "type": "derived-from"},
        ]
        graph = build_graph(rels)
        result = traverse(graph, "a", max_hops=2)
        node_ids = {n["id"] for n in result["nodes"]}
        assert "c" in node_ids

    def test_not_in_graph(self):
        graph = build_graph([])
        result = traverse(graph, "nonexistent", max_hops=2)
        assert len(result["nodes"]) <= 1  # Just the start node or empty

    def test_returns_edges(self):
        rels = [{"source_id": "a", "target_id": "b", "type": "derived-from"}]
        graph = build_graph(rels)
        result = traverse(graph, "a", max_hops=1)
        assert len(result["edges"]) >= 1


class TestFormatText:
    def test_basic_output(self):
        result = {
            "nodes": [
                {"id": "abc123", "title": "Test Node", "maturity": "summary", "item_type": "nugget", "tags": ["test"]},
            ],
            "edges": [
                {"source": "abc123", "target": "def456", "type": "derived-from", "note": ""},
            ],
            "hops": 1,
        }
        text = format_text(result)
        assert "Test Node" in text

    def test_empty_graph(self):
        result = {"nodes": [], "edges": [], "hops": 0}
        text = format_text(result)
        assert isinstance(text, str)
