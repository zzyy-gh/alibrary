"""MCP stdio server exposing the Knowledge Library researcher as tools.

Provides library_search, library_trace, and library_graph tools via FastMCP.

Usage:
  python .claude/scripts/mcp_researcher.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import parse_frontmatter, get_project_root, load_all_relationships
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Knowledge Library")


@mcp.tool()
def library_search(query: str, tags: str = "", n: int = 10) -> str:
    """Search the Knowledge Library using semantic search with optional tag filters.

    Args:
        query: Natural language search query.
        tags: Comma-separated tags to filter by (optional).
        n: Maximum number of results to return (default 10).

    Returns:
        JSON string with search results including id, title, maturity, confidence, and file_path.
    """
    from researcher import search_semantic, search_tags

    root = get_project_root()
    nuggets_dir = root / "nuggets"
    inbox_dir = root / "inbox"

    if query:
        try:
            results = search_semantic(query, n=n)
            # Post-filter by tags if provided
            if tags:
                tag_set = set(t.strip().lower() for t in tags.split(","))
                results = [r for r in results if tag_set.intersection(
                    set(t.lower() for t in r.get("tags", []))
                )]
        except Exception as e:
            return json.dumps({"error": str(e)})
    elif tags:
        tag_list = [t.strip() for t in tags.split(",")]
        results = search_tags(tag_list, nuggets_dir, inbox_dir)
        results = results[:n]
    else:
        return json.dumps({"error": "Provide a query or tags"})

    return json.dumps(results, indent=2, ensure_ascii=False)


@mcp.tool()
def library_trace(nugget_id: str) -> str:
    """Trace the provenance of a nugget back to its source items.

    Args:
        nugget_id: Full or partial UUID of the nugget to trace.

    Returns:
        JSON string with the nugget info and its derived-from sources.
    """
    root = get_project_root()
    nuggets_dir = root / "nuggets"

    # Find the nugget
    nugget_file = None
    resolved_id = nugget_id
    for fpath in nuggets_dir.glob("*.md"):
        try:
            fm, _ = parse_frontmatter(fpath)
            if fm.get("id") == nugget_id or fm.get("id", "").startswith(nugget_id):
                nugget_file = fpath
                resolved_id = fm["id"]
                break
        except Exception:
            continue

    if not nugget_file:
        return json.dumps({"error": f"Nugget not found: {nugget_id}"})

    fm, _ = parse_frontmatter(nugget_file)
    result = {
        "nugget": {
            "id": resolved_id,
            "title": fm.get("title", ""),
            "maturity": fm.get("maturity", ""),
        },
        "sources": [],
    }

    # Load relationships
    relationships = load_all_relationships()
    derived = [r for r in relationships if r.get("source_id") == resolved_id and r.get("type") == "derived-from"]

    for rel in derived:
        target_id = rel.get("target_id", "")
        source_info = {"id": target_id, "note": rel.get("note", "")}

        # Try to find the source item
        for d in [root / "inbox", root / "nuggets"]:
            for fpath in d.glob("*.md"):
                try:
                    sfm, _ = parse_frontmatter(fpath)
                    if sfm.get("id") == target_id:
                        source_info["title"] = sfm.get("title", "")
                        source_info["file_path"] = str(fpath)
                        break
                except Exception:
                    continue

        result["sources"].append(source_info)

    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def library_graph(item_id: str, hops: int = 2) -> str:
    """Explore the relationship graph around an item.

    Args:
        item_id: UUID of the item to start from.
        hops: Number of relationship hops to traverse (default 2).

    Returns:
        JSON string with connected items and their relationships.
    """
    from graph_explore import build_graph, traverse
    relationships = load_all_relationships()
    graph = build_graph(relationships)
    result = traverse(graph, item_id, max_hops=hops)
    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
