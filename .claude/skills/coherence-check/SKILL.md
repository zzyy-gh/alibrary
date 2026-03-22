# Skill: coherence-check

Run a coherence check on `meta/` and `.claude/` folders when there are uncommitted changes.

## Trigger

Invoke manually: `/coherence-check`

## Process

1. Run `git diff --name-only` and `git diff --name-only --cached` to find changed files
2. Filter for files in `meta/` or `.claude/`
3. If no changes in either folder, report "No changes to check" and stop
4. For each changed folder, read all files in that folder and check for:
   - **Syntax** — valid markdown, valid JSON, valid YAML frontmatter
   - **Structure** — consistent heading hierarchy and format
   - **Logic** — no contradictions, coherent design decisions, workflows make sense
   - **Cross-references** — referenced files exist, skill/agent/script names align
5. Report findings: list issues or confirm all checks pass
