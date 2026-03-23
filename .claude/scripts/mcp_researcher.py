"""MCP stdio server exposing the Knowledge Library researcher as tools.

Provides library_search tool via FastMCP.

Usage:
  python .claude/scripts/mcp_researcher.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from helpers import get_project_root
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


if __name__ == "__main__":
    mcp.run(transport="stdio")
