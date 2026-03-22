"""Shared utilities for the Knowledge Library scripts.

Provides UUID generation, frontmatter parsing/writing, relationship I/O,
and datetime helpers. Used by event queue scripts, find_unprocessed, and agents.
"""

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml


def get_project_root() -> Path:
    """Return the project root (alibrary/)."""
    return Path(__file__).resolve().parent.parent.parent


def get_db_path() -> Path:
    """Return the default path to the SQLite database."""
    return get_project_root() / ".claude" / "scripts" / "library.db"


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


def load_all_relationships(rel_dir: str | Path | None = None) -> list[dict]:
    """Read all JSON files from /relationships/ and return a flat list of relationship dicts."""
    if rel_dir is None:
        rel_dir = get_project_root() / "relationships"
    rel_dir = Path(rel_dir)

    relationships = []
    if not rel_dir.is_dir():
        return relationships

    for fpath in rel_dir.glob("*.json"):
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            if isinstance(data, list):
                relationships.extend(data)
            elif isinstance(data, dict):
                relationships.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    return relationships


def save_relationships(relationships: list[dict], session_id: str, rel_dir: str | Path | None = None) -> Path:
    """Write a list of relationship dicts to /relationships/{session_id}.json."""
    if rel_dir is None:
        rel_dir = get_project_root() / "relationships"
    rel_dir = Path(rel_dir)
    rel_dir.mkdir(parents=True, exist_ok=True)

    fpath = rel_dir / f"{session_id}.json"

    # If file exists, load and extend
    existing = []
    if fpath.exists():
        try:
            existing = json.loads(fpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = []

    existing.extend(relationships)
    fpath.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    return fpath
