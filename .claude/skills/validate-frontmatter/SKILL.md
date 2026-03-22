# Skill: validate-frontmatter

Validate and repair YAML frontmatter on a raw item in `/inbox/`.

## Input

- A file path to a Markdown file in `/inbox/`

## Process

1. Read the file using `parse_frontmatter()` from `.claude/scripts/helpers.py`
2. Check required fields against the Raw Item schema in `meta/schemas.md`:
   - `id`: valid UUID. If missing, generate one via `generate_uuid()`
   - `title`: non-empty string. If missing, infer from filename or first heading
   - `source_type`: one of `article`, `documentation`, `video`, `code`, `conversation`, `manual`, `snippet`. If missing, infer from content
   - `tags`: list of 2–5 lowercase strings. If missing, leave empty for assign-tags skill
   - `created_at`: ISO 8601 datetime. If missing, use current time via `now_iso()`
   - `created_by`: non-empty string. If missing, set to `"unknown"`
3. Validate optional fields if present: `source_url`, `artifact_path`, `summary`
4. Write repaired frontmatter back using `write_frontmatter()` from helpers

## Output

- The file is updated in-place with valid frontmatter
- Report what was repaired: list of `{field, old_value, new_value}`

## Constraints

- Never delete existing valid fields
- Never modify the Markdown body content
- Preserve field ordering where possible
