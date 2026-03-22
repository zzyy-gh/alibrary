# Skill: synthesize-nugget

Synthesize one or more knowledge nuggets from a raw item.

## Input

- A file path to a raw item in `/inbox/`
- The raw item's parsed frontmatter and body content

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
   - `created_by`, `updated_by`: `indexer`
   - `changelog`: initial entry `{timestamp, agent: "indexer", action: "created", diff: null, reason: "Initial synthesis from [raw item title]"}`
4. Write each nugget as `/nuggets/{uuid}.md` with YAML frontmatter using helpers
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
