# Skill: assign-tags

Generate descriptive tags for a raw item or nugget based on its content.

## Input

- A file path to a Markdown file (raw item in `/inbox/` or nugget in `/nuggets/`)
- The current tags from frontmatter (if any)

## Process

1. Read the file content (frontmatter + body)
2. Analyze content to identify:
   - Primary domain/topic (e.g. `python`, `authentication`, `architecture`)
   - Content type indicators (e.g. `tutorial`, `reference`, `pattern`)
3. Generate tags following conventions:
   - All lowercase, no spaces (use hyphens: `event-driven`)
   - 2–5 tags for raw items, 2–10 for nuggets
   - Prefer reusing existing tags in the library for consistency
4. Update the file frontmatter with the new tags using `write_frontmatter()` from helpers

## Output

- The file is updated in-place with assigned tags
- Return the list of assigned tags

## Constraints

- Tags must be lowercase
- No duplicate tags
- Minimum 2 tags per item
