# Skill: synthesize-nugget

Synthesize knowledge nuggets from multiple related sources. Invoked by the librarian when cross-source patterns are discovered — not for 1:1 summaries of single items.

## Input

- File paths to two or more related items (raw items in `/inbox/` and/or nuggets in `/nuggets/`)
- Each item's parsed frontmatter and body content

## Process

1. Read and understand the source material
2. Identify distinct topics — a single raw item may yield multiple nuggets
3. For each nugget, produce:
   - `id`: new UUID via `generate_uuid()`
   - `title`: concise, descriptive (not the same as the raw item title)
   - `summary`: 1–3 sentences capturing the core insight
   - `maturity`: `stub` if minimal, `summary` if a reasonable standalone summary
   - `tags`: 2–10 lowercase tags
   - `quality_score`: initial estimate (`stub` ~0.2, `summary` ~0.4)
   - `decay_rate`: `fast` for tech-specific, `medium` for general, `slow` for conceptual
   - `review_by`: today + 7 days for stubs, + 30 days for summaries
   - `created_at`, `updated_at`: current time
   - `created_by`, `updated_by`: `librarian`
   - `changelog`: initial entry `{timestamp, agent: "librarian", action: "created", diff: null, reason: "Cross-source synthesis from [source titles]"}`
4. Write each nugget as `/nuggets/{slug}.md` (slugified title, see `meta/schemas.md` § Filename Convention) using `slugify()` and `unique_filepath()` from helpers
5. The body is AI-synthesized knowledge — standalone prose, not a copy of the source

## Output

- One or more nugget files written to `/nuggets/`
- Return list of `{id, title, maturity, file_path}`

## Constraints

- Every nugget must be readable without visiting its source
- Never copy source text verbatim — always synthesize
- Initial maturity is `stub` or `summary` only
- Quality score reflects actual synthesis depth
- See `meta/schemas.md` for the full nugget schema
