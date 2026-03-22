import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import write_frontmatter, generate_uuid, now_iso
from init_db import init_db


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temp project structure with inbox/, nuggets/, relationships/."""
    (tmp_path / "inbox").mkdir()
    (tmp_path / "nuggets").mkdir()
    (tmp_path / "relationships").mkdir()
    return tmp_path


@pytest.fixture
def sample_raw_item(tmp_project):
    """Write a sample raw item and return (path, id)."""
    item_id = generate_uuid()
    fpath = tmp_project / "inbox" / "test-item.md"
    write_frontmatter(fpath, {
        "id": item_id,
        "title": "Test Item",
        "source_type": "manual",
        "tags": ["test", "sample"],
        "created_at": now_iso(),
        "created_by": "test",
    }, "This is test content.")
    return fpath, item_id


@pytest.fixture
def sample_nugget(tmp_project):
    """Write a sample nugget and return (path, id)."""
    item_id = generate_uuid()
    fpath = tmp_project / "nuggets" / "test-nugget.md"
    write_frontmatter(fpath, {
        "id": item_id,
        "title": "Test Nugget",
        "maturity": "summary",
        "summary": "A test nugget summary.",
        "tags": ["test", "nugget"],
        "quality_score": 0.7,
        "decay_rate": "medium",
        "created_at": now_iso(),
        "created_by": "test",
    }, "Synthesized test content.")
    return fpath, item_id


@pytest.fixture
def sample_relationships(tmp_project, sample_raw_item, sample_nugget):
    """Write a derived-from relationship and return the relationship list."""
    _, raw_id = sample_raw_item
    _, nugget_id = sample_nugget
    rels = [{
        "source_id": nugget_id,
        "target_id": raw_id,
        "type": "derived-from",
        "created_at": now_iso(),
        "created_by": "test",
    }]
    fpath = tmp_project / "relationships" / "test-session.json"
    fpath.write_text(json.dumps(rels), encoding="utf-8")
    return rels


@pytest.fixture
def db_path(tmp_path):
    """Create a temp SQLite DB with events table."""
    path = str(tmp_path / "test.db")
    init_db(path)
    return path
