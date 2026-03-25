# Skill: validate-frontmatter

Validate and repair YAML frontmatter on a raw item in `/inbox/`.

## Input

- A file path to a Markdown file in `/inbox/`

## Process

1. Read the file using `parse_frontmatter()` from `.claude/scripts/helpers.py`
2. Check required fields against the Raw Item schema in `meta/schemas.md`
3. Repair missing fields:
   - `id`: generate via `generate_uuid()`
   - `title`: infer from filename or first heading
   - `source_type`: infer from content
   - `tags`: leave empty for assign-tags skill
   - `created_at`: use current time via `now_iso()`
   - `created_by`: set to `"unknown"`
   - `maturity`: default to `stub`
4. Validate optional fields if present: `source_url`, `artifact_path`, `summary`
5. Write repaired frontmatter back using `write_frontmatter()` from helpers

## Output

- The file is updated in-place with valid frontmatter
- Report what was repaired: list of `{field, old_value, new_value}`

## Constraints

- Never delete existing valid fields
- Never modify the Markdown body content
- Preserve field ordering where possible
