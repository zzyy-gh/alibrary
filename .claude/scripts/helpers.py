"""Shared utilities for the Knowledge Library scripts.

Provides UUID generation, frontmatter parsing/writing,
and datetime helpers. Used by find_unprocessed, CLI, and agents.
"""

import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml


def get_project_root() -> Path:
    """Return the project root (alibrary/)."""
    return Path(__file__).resolve().parent.parent.parent


def generate_uuid() -> str:
    """Return a new UUID v4 string."""
    return str(uuid.uuid4())


def now_iso() -> str:
    """Return current UTC datetime as ISO 8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_date() -> str:
    """Return current date as YYYY-MM-DD string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def slugify(title: str) -> str:
    """Convert a title to a filename slug: lowercase, hyphens, no special chars."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "untitled"


def unique_filepath(directory: Path, slug: str, ext: str = ".md") -> Path:
    """Return a unique filepath in directory, appending -2, -3, etc. on collision."""
    fpath = directory / f"{slug}{ext}"
    if not fpath.exists():
        return fpath
    counter = 2
    while True:
        fpath = directory / f"{slug}-{counter}{ext}"
        if not fpath.exists():
            return fpath
        counter += 1


def parse_frontmatter(filepath: str | Path) -> tuple[dict, str]:
    """Read a Markdown file and return (frontmatter_dict, body_string).

    If no frontmatter is found, returns ({}, full_content).
    """
    filepath = Path(filepath)
    content = filepath.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return fm, body


def write_frontmatter(filepath: str | Path, frontmatter: dict, body: str) -> None:
    """Write a Markdown file with YAML frontmatter."""
    filepath = Path(filepath)
    fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    filepath.write_text(f"---\n{fm_str}---\n\n{body}", encoding="utf-8")


def resolve_id(query: str, project_root: Path | None = None) -> dict | None:
    """Find a library item by UUID (or prefix) or title substring.

    Searches inbox/ and nuggets/. Returns {id, title, item_type, file_path}
    or None if not found or ambiguous (multiple matches).
    """
    if project_root is None:
        project_root = get_project_root()

    matches = []
    for folder, item_type in [(project_root / "inbox", "raw"), (project_root / "nuggets", "nugget")]:
        if not folder.is_dir():
            continue
        for fpath in folder.glob("*.md"):
            if fpath.name == ".gitkeep":
                continue
            try:
                fm, _ = parse_frontmatter(fpath)
                item_id = str(fm.get("id", ""))
                item_title = fm.get("title", "")

                if item_id == query or item_id.startswith(query):
                    matches.append({
                        "id": item_id,
                        "title": item_title,
                        "item_type": item_type,
                        "file_path": str(fpath),
                    })
                elif query.lower() in item_title.lower():
                    matches.append({
                        "id": item_id,
                        "title": item_title,
                        "item_type": item_type,
                        "file_path": str(fpath),
                    })
            except Exception:
                continue

    if len(matches) == 1:
        return matches[0]
    return None


