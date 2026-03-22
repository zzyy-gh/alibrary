"""Graph exploration for the Knowledge Library.

Traverse relationships, resolve node metadata, and visualize the knowledge graph.

Usage:
  python graph_explore.py --id UUID --hops N [--format json|text]   # traverse from a node
  python graph_explore.py --all [--format json|text]                 # dump entire graph
  python graph_explore.py --viz [--output PATH]                      # generate HTML visualization
"""

import argparse
import json
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import get_project_root, load_all_relationships, parse_frontmatter


def build_graph(relationships: list[dict]) -> dict:
    """Build an adjacency list from a list of relationship dicts.

    Each node maps to a list of {neighbor_id, relationship_type, note, direction}
    where direction is "outgoing" or "incoming".
    """
    graph: dict[str, list[dict]] = {}

    for rel in relationships:
        src = rel.get("source_id")
        tgt = rel.get("target_id")
        rel_type = rel.get("type", "unknown")
        note = rel.get("note", "")

        if not src or not tgt:
            continue

        # Ensure both nodes exist in the graph
        if src not in graph:
            graph[src] = []
        if tgt not in graph:
            graph[tgt] = []

        # Outgoing edge from source
        graph[src].append({
            "neighbor_id": tgt,
            "relationship_type": rel_type,
            "note": note,
            "direction": "outgoing",
        })

        # Incoming edge to target
        graph[tgt].append({
            "neighbor_id": src,
            "relationship_type": rel_type,
            "note": note,
            "direction": "incoming",
        })

    return graph


def resolve_node(node_id: str) -> dict | None:
    """Scan inbox/ and nuggets/ for a file with matching id in frontmatter.

    Returns {id, title, maturity, tags, item_type, file_path} or None.
    """
    root = get_project_root()

    for folder, item_type in [(root / "inbox", "raw"), (root / "nuggets", "nugget")]:
        if not folder.is_dir():
            continue
        for fpath in folder.glob("*.md"):
            if fpath.name == ".gitkeep":
                continue
            try:
                fm, _ = parse_frontmatter(fpath)
                if fm.get("id") == node_id:
                    return {
                        "id": node_id,
                        "title": fm.get("title", "Untitled"),
                        "maturity": fm.get("maturity", ""),
                        "tags": fm.get("tags", []),
                        "item_type": item_type,
                        "file_path": str(fpath),
                    }
            except Exception:
                continue

    return None


def traverse(graph: dict, start_id: str, max_hops: int = 2) -> dict:
    """BFS from start_id up to max_hops.

    Returns {"nodes": [...], "edges": [...], "hops": max_hops}.
    Nodes include resolved metadata. Edges include type and note.
    """
    visited: set[str] = set()
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_edges: set[tuple] = set()

    queue: deque[tuple[str, int]] = deque()
    queue.append((start_id, 0))
    visited.add(start_id)

    while queue:
        current_id, depth = queue.popleft()

        # Resolve node metadata
        meta = resolve_node(current_id)
        if meta:
            nodes.append(meta)
        else:
            nodes.append({
                "id": current_id,
                "title": current_id[:8] + "..",
                "maturity": "",
                "tags": [],
                "item_type": "unresolved",
                "file_path": "",
            })

        if depth >= max_hops:
            continue

        # Explore neighbors
        for edge in graph.get(current_id, []):
            neighbor = edge["neighbor_id"]

            # Record edge (deduplicate by source-target-type)
            if edge["direction"] == "outgoing":
                edge_key = (current_id, neighbor, edge["relationship_type"])
            else:
                edge_key = (neighbor, current_id, edge["relationship_type"])

            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({
                    "source": edge_key[0],
                    "target": edge_key[1],
                    "type": edge["relationship_type"],
                    "note": edge["note"],
                })

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    return {"nodes": nodes, "edges": edges, "hops": max_hops}


def get_full_graph(relationships: list[dict]) -> dict:
    """Return the entire graph with all nodes resolved."""
    # Collect all unique node IDs
    all_ids: set[str] = set()
    for rel in relationships:
        if rel.get("source_id"):
            all_ids.add(rel["source_id"])
        if rel.get("target_id"):
            all_ids.add(rel["target_id"])

    nodes = []
    for node_id in sorted(all_ids):
        meta = resolve_node(node_id)
        if meta:
            nodes.append(meta)
        else:
            nodes.append({
                "id": node_id,
                "title": node_id[:8] + "..",
                "maturity": "",
                "tags": [],
                "item_type": "unresolved",
                "file_path": "",
            })

    edges = []
    seen_edges: set[tuple] = set()
    for rel in relationships:
        src = rel.get("source_id")
        tgt = rel.get("target_id")
        rel_type = rel.get("type", "unknown")
        if not src or not tgt:
            continue
        edge_key = (src, tgt, rel_type)
        if edge_key not in seen_edges:
            seen_edges.add(edge_key)
            edges.append({
                "source": src,
                "target": tgt,
                "type": rel_type,
                "note": rel.get("note", ""),
            })

    return {"nodes": nodes, "edges": edges, "hops": -1}


def format_text(result: dict) -> str:
    """Format a graph result as human-readable text."""
    lines = []

    # Build a lookup for quick access
    node_map = {n["id"]: n for n in result["nodes"]}

    for node in result["nodes"]:
        type_label = f"[{node['item_type']}]" if node["item_type"] else ""
        lines.append(f"Node: {node['title']} ({node['id'][:8]}..) {type_label}")

        # Find edges involving this node
        for edge in result["edges"]:
            if edge["source"] == node["id"]:
                target = node_map.get(edge["target"], {})
                target_title = target.get("title", edge["target"][:8] + "..")
                target_short = edge["target"][:8] + ".."
                lines.append(f"  [{edge['type']} ->] {target_title} ({target_short})")
            elif edge["target"] == node["id"]:
                source = node_map.get(edge["source"], {})
                source_title = source.get("title", edge["source"][:8] + "..")
                source_short = edge["source"][:8] + ".."
                lines.append(f"  [{edge['type']} <-] {source_title} ({source_short})")

        lines.append("")

    return "\n".join(lines)


def generate_viz(result: dict, output_path: str) -> None:
    """Generate an HTML visualization from a graph result."""
    template_path = Path(__file__).parent / "graph_viz_template.html"
    if not template_path.exists():
        print(f"Error: template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    template = template_path.read_text(encoding="utf-8")
    graph_json = json.dumps(result, indent=2, ensure_ascii=False)
    html = template.replace("__GRAPH_DATA__", graph_json)

    out = Path(output_path)
    out.write_text(html, encoding="utf-8")
    print(f"Visualization written to: {out}")


def main():
    parser = argparse.ArgumentParser(description="Knowledge Library Graph Explorer")

    parser.add_argument("--id", help="Start node UUID (full or prefix)")
    parser.add_argument("--hops", type=int, default=2, help="Max hops for traversal (default: 2)")
    parser.add_argument("--all", action="store_true", help="Dump the entire graph")
    parser.add_argument("--viz", action="store_true", help="Generate HTML visualization")
    parser.add_argument("--output", default=None, help="Output path for visualization")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")

    args = parser.parse_args()

    if not args.id and not args.all and not args.viz:
        parser.print_help()
        sys.exit(1)

    relationships = load_all_relationships()

    if args.viz:
        result = get_full_graph(relationships)
        output = args.output or str(get_project_root() / "graph.html")
        generate_viz(result, output)
        return

    if args.all:
        result = get_full_graph(relationships)
    else:
        # Resolve partial ID
        start_id = args.id
        all_ids = set()
        for rel in relationships:
            if rel.get("source_id"):
                all_ids.add(rel["source_id"])
            if rel.get("target_id"):
                all_ids.add(rel["target_id"])

        matches = [uid for uid in all_ids if uid.startswith(start_id)]
        if len(matches) == 1:
            start_id = matches[0]
        elif len(matches) > 1:
            print(f"Ambiguous ID prefix '{start_id}', matches:", file=sys.stderr)
            for m in sorted(matches):
                print(f"  {m}", file=sys.stderr)
            sys.exit(1)

        graph = build_graph(relationships)
        if start_id not in graph:
            # Check if node exists in inbox/nuggets even without relationships
            meta = resolve_node(start_id)
            if meta:
                result = {"nodes": [meta], "edges": [], "hops": args.hops}
            else:
                print(f"Node not found in graph: {start_id}", file=sys.stderr)
                sys.exit(1)
        else:
            result = traverse(graph, start_id, args.hops)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
