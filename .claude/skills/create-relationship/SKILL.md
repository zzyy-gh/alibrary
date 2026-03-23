# Skill: create-relationship

Create typed relationship edges between library items.

## Input

- `source_id`: UUID of the source node (e.g. nugget)
- `target_id`: UUID of the target node (e.g. raw item)
- `type`: `derived-from` or `contradicts`
- `note`: optional string explaining the connection
- `created_by`: agent name (e.g. `indexer`)
- `session_id`: identifier for this agent run (for grouping relationships into one file)

## Process

1. Validate inputs:
   - `source_id` != `target_id` (no self-referential edges)
   - `type` is `derived-from` or `contradicts`
   - Both `source_id` and `target_id` must resolve to existing files in `/inbox/` or `/nuggets/` — use `resolve_id()` from `.claude/scripts/helpers.py` to verify. **Reject the relationship if either ID is unresolved.**
2. For `derived-from`: check acyclicity — load existing relationships via `load_all_relationships()` from helpers, verify no path from `target_id` back to `source_id`
3. For `contradicts`: check no duplicate edge already exists for this pair
4. Build the relationship tuple with `created_at` via `now_iso()`
5. Append to `/relationships/{session_id}.json` via `save_relationships()` from helpers

## Output

- Relationship written to `/relationships/{session_id}.json`
- Return the relationship dict

## Constraints

- No self-referential edges
- `derived-from` must be acyclic
- Only one `contradicts` edge per node pair
- Every nugget must have at least one `derived-from` relationship
- See `meta/schemas.md` for the full relationship schema
