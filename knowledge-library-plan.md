# THE KNOWLEDGE LIBRARY

**Architecture, Design & Implementation Plan**

*A universal knowledge layer for autonomous agents*

**Version:** 1.4
**Date:** March 2026
**Status:** Draft

---

## Vision & Principles

The Knowledge Library is a persistent, structured, agent-accessible knowledge store. It serves as the single source of truth for procedural knowledge, reusable patterns, domain facts, references, and operational context. Any agent can query it at any time; a dedicated team of library agents maintains, enriches, and refines it continuously. Agent-specific configurations (skills, rules, instructions) are generated projections of the library's foundational knowledge, not the source of truth.

### Core Principles

- **Link-first, expand later.** Knowledge enters the library through `/inbox/` as lightweight stubs (a URL, a title, a few tags). The indexer picks up new items, classifies them, and places them in the appropriate folder. Over time, library agents enrich these stubs into full standalone entries. This keeps the ingest barrier low while building depth over time.
- **Folder-native, multi-indexed.** The primary representation is a human-readable folder tree. But the same content is also indexed by vector embeddings, tags, and explicit relationships — so agents can retrieve knowledge by browsing, searching semantically, filtering by category, or traversing connections.
- **Knowledge has types.** Knowledge entries (reusable patterns and domain facts) and references (pointers to external resources) are top-level knowledge categories. Procedural knowledge (how-to, skills) lives in `/meta/foundational/` as the generative source for agent-specific configurations. Within `/knowledge/`, individual entries vary in decay rate, trust level, and usage pattern — a stable architectural pattern ages slowly while a domain-specific regulatory fact needs frequent review. The schema encodes this per entry via `decay_rate` and `quality_score`.
- **Refinement over accumulation.** A library that only grows becomes a junkyard. The librarian agent continuously merges duplicates, validates links, discovers relationships, identifies gaps, and restructures folders. Quality compounds; clutter compounds too.
- **Auditability.** Every change is logged with a reason, a timestamp, and the agent that made it. Knowledge can be versioned, reverted, and traced.
- **Agent-agnostic at its core.** The library stores foundational knowledge — principles, workflows, constraints — that is true regardless of which agent runtime consumes it. Agent-specific configurations (Claude skills, Cursor rules, OpenAI instructions) are generated projections of this foundational knowledge, not the source of truth. The library is a platform, not an accessory to any single agent.
- **Inference-first content design.** Foundational entries in `/meta/foundational/` are optimised for agent consumption, not human readability. This means: high information density per token, explicit declarative statements rather than narrative prose, consistent terminology across entries, unambiguous taxonomic relationships, and every constraint and exception stated rather than implied. Human-readable versions are generated on demand through the projection layer. The library's markdown is structured knowledge that happens to be stored in markdown, not documentation.

---

## Architecture Overview

The library is composed of three layers and four agents. The layers handle storage, indexing, and presentation. The agents handle ingest, maintenance, retrieval, and institutional learning.

### Three Layers

#### Storage Layer

The canonical store. Each knowledge entry is a node with structured metadata stored in a database (SQLite for local, PostgreSQL for shared). The content itself may also be mirrored as Markdown files in the folder tree for human readability and Git-based version control.

#### Index Layer

Multiple indexes over the same data, each optimised for a different retrieval pattern:

- **Folder index:** a hierarchical tree for browsing and categorical retrieval.
- **Vector index:** embeddings of each entry for semantic similarity search.
- **Tag index:** flat labels for filtering (e.g. "python", "auth", "2024", "stale").
- **Graph index:** explicit typed relationships between entries (depends-on, related-to, supersedes, example-of).

#### View Layer

Projections of the underlying data for different consumers. A folder tree view, a mind-map view, a dependency graph, a dashboard of library health metrics. These are generated from queries, not manually maintained.

---

## The Four Agents

Each agent has a distinct role, a clear trigger model, and access to the shared library store. The first three agents — indexer, librarian, researcher — are operational workers with read-write access to the library. The fourth — the intern — is an observer with read-only access to everything, whose role is institutional learning.

All agents should read their own operating instructions from `/meta/foundational/` at the start of each run. This means the library contains the instructions for how to maintain itself. When agents improve through experience, those improvements are captured as updates to their foundational entries, creating a self-referential loop where the system's playbook evolves over time.

| Agent | Role | Trigger Model |
|-------|------|---------------|
| Indexer | Classifies incoming knowledge, assigns metadata, places it in the folder tree, generates initial embeddings. | Fires when new items appear in `/inbox/` — a submitted URL, a pasted snippet, a dropped file, or an API call. Must be fast and cheap. |
| Librarian | Enriches stubs, validates links, merges duplicates, restructures folders, discovers relationships, identifies gaps, manages staleness. | Runs on a schedule (daily/weekly). Also picks up tasks from the event queue: "entry:created", "entry:flagged", threshold alerts. |
| Researcher | Handles queries from other agents or humans. Determines the best retrieval strategy. Can also acquire new knowledge when gaps are found. | On-demand, invoked via tool call or API. Returns results and optionally logs gaps for the indexer. |
| Intern | Observes all system activity — user conversations, agent decisions, query patterns, refinement outcomes — and surfaces institutional learning. Read-only access to everything; write access to nothing. Outputs recommendations into a review queue. | Periodic (end of day/week) or event-batch driven. Processes activity logs in aggregate, looking for patterns rather than reacting to individual events. |

### Indexer (Cataloguer)

When new knowledge arrives in `/inbox/`, the indexer performs the following:

- **Classification:** What type is this? (knowledge / reference / foundational)
- **Metadata extraction:** Title, summary, source URL, language, relevant domain.
- **Folder placement:** Determine the best folder path in `/knowledge/`, `/references/`, or `/meta/`. Create new subfolders if no existing category fits. Move the processed item out of `/inbox/`.
- **Tagging:** Apply 2–5 tags based on content analysis.
- **Embedding:** Generate a vector embedding and store it in the vector index.
- **Maturity scoring:** Assign initial maturity level (typically "stub" or "summary" depending on input richness).
- **Event emission:** Post an "entry:created" event with the new entry ID.

The indexer should be optimised for speed. It can use a smaller, faster model for classification and a separate embedding model for vectors. It should process an ingest in under 5 seconds.

### Librarian (Curator)

The librarian is the refinement engine. It operates asynchronously on a schedule and through event-driven tasks.

#### Refinement Operations

- **Content enrichment:** Take a stub entry (just a URL) and expand it: fetch the page, extract key points, write a standalone summary, update the maturity score.
- **Inference optimisation:** When enriching entries, the goal is not "make this read better" but "make this more inferrable." Reduce ambiguity, increase density, standardise terminology, make relationships explicit, state every constraint and exception. Prefer "CONSTRAINT: X defaults to Y. Always set Z explicitly." over narrative prose like "One thing to watch out for is that X defaults to Y."
- **Link validation:** Check all reference URLs. Flag broken links, detect redirects, note if content has changed significantly since last check.
- **Deduplication:** Detect entries that cover substantially the same knowledge. Merge them into one richer entry, preserving the best content from each.
- **Relationship discovery:** After enriching an entry, scan for related entries. Create typed edges: "related-to", "depends-on", "supersedes", "example-of".
- **Folder hygiene:** Detect imbalanced folders (>50 entries or <3 entries), propose splits or merges, move miscategorised entries.
- **Gap analysis:** Examine the library's shape. Identify domains with thin coverage relative to their importance or usage frequency. Flag gaps for human review or autonomous acquisition.
- **Staleness management:** Apply decay models by knowledge type. Tech-specific entries decay fast (6–12 months), conceptual entries decay slowly (2–5 years). Re-check entries past their review-by date.
- **Quality scoring:** Maintain an overall quality score per entry (completeness, accuracy, recency, link health). Surface the lowest-quality entries for priority attention.

#### Refinement Audit Log

Every librarian action produces a log entry: what changed, why, what the entry looked like before, and a confidence level. This enables rollback and builds trust in automated curation.

### Researcher (Reference Desk)

The researcher is the query interface. Other agents and humans talk to the researcher when they need knowledge.

- **Query routing:** Determine the best retrieval strategy for each query. Exact match → folder lookup. Vague question → vector search. Exploratory → graph traversal. Filtered → tag query.
- **Multi-strategy fusion:** For complex queries, combine results from multiple indexes and rank by relevance.
- **Maturity-aware responses:** When returning a stub entry, flag it as low-confidence. When returning a fully enriched entry, flag it as high-confidence. Let the consuming agent decide how to weight it.
- **Gap detection:** When a query returns no results or only stubs, log a "knowledge:gap" event. The indexer or librarian can then prioritise acquiring or enriching that area.
- **Context assembly:** For agents with limited context windows, the researcher should return concise, pre-digested knowledge — not raw documents. Summarise, extract the relevant section, or provide a structured snippet.
- **Human-readable generation:** When a human queries the library directly, the researcher generates a readable response with narrative, examples, and context — produced on the fly from the inference-optimised foundational entry. For shareable documents, the researcher invokes the human-readable spawn template to produce a formatted artefact.

### Intern (Institutional Learner)

The intern is the library's capacity for self-awareness at the system level. It has read-only access to everything — all library entries, all agent activity logs, all event queues, all user conversations — but cannot write to the library directly. It outputs recommendations into a review queue that humans or senior agents approve or reject.

#### Access Model

**Read:** everything. The intern can see all library content, all agent logs, all event history, all user conversations that flow through the system. This all-access visibility is what enables cross-cutting pattern recognition that no single operational agent could achieve.

**Write:** nothing. The intern cannot modify library entries, cannot change folder structures, cannot update metadata. It can only append to a dedicated recommendations queue. This constraint is permanent by design — it is what keeps the intern fresh and unburdened by operational responsibility.

#### What the Intern Observes

- **Query patterns:** Which topics get asked about repeatedly? Which phrasings fail to return results even though relevant entries exist? Are there synonyms or framings the embeddings aren't capturing?
- **Agent disagreements:** The indexer places entries in one folder; the librarian moves them to another. This signals a taxonomy boundary that's unclear and needs better guidance in `/meta/foundational/`.
- **Refinement outcomes:** Which librarian actions get reverted? Which merges were wrong? Which enrichments degraded quality? These are signals that the librarian's operating policies need tuning.
- **User conversation signals:** New concepts, emerging terminology, recurring frustrations, knowledge that surfaces in conversation but never gets formally indexed. The intern catches what falls through the cracks.
- **System-level gaps:** Not just content gaps (the researcher handles those), but structural gaps — missing relationship types, inadequate tag taxonomies, folder categories that no longer match how knowledge is actually used.

#### What the Intern Outputs

All intern output goes into a recommendations queue with a type, a rationale, and a suggested action. Recommendations are never auto-applied. Examples:

- **Policy update:** "Update `/meta/foundational/librarian/deduplication-policy` — the 0.92 cosine threshold is too aggressive based on 7 false merges this month. Suggest lowering to 0.88."
- **Taxonomy clarification:** "Clarify the boundary between `/knowledge/architecture/` and `/knowledge/infrastructure/` for DevOps topics. The indexer and librarian disagree on placement 40% of the time for entries tagged 'devops'."
- **Missing knowledge:** "Users have asked about 'edge computing deployment patterns' in 12 conversations this month. The library has zero entries. Recommend acquisition."
- **Embedding improvement:** "The query 'how to handle auth' returns no results, but entries about 'authentication patterns' and 'OAuth implementation' exist. Suggest adding synonyms to tags or recomputing embeddings."
- **Agent self-improvement:** "The indexer's classification accuracy for 'foundational' vs 'knowledge' type is 68%. Suggest adding distinguishing criteria to `/meta/foundational/indexing/classification-strategy`."

#### Why It Stays an Intern Forever

The read-only constraint is not a temporary limitation — it is the design. The intern's value comes from its permanent outsider perspective. It never becomes invested in defending past decisions because it never made any. It never accumulates operational stress or bias. It observes with fresh eyes every time, unburdened by the responsibility of execution. Giving it write access would turn it into another librarian. Keeping it read-only keeps it what the system needs: a tireless, curious observer with no agenda except noticing things.

### Self-Referential Design

All four agents read their operating instructions from `/meta/foundational/` at the start of each run. The indexer reads its classification strategy, the librarian reads its refinement policies, the researcher reads its retrieval rules, and the intern reads its observation criteria. When any of these need updating — based on experience, intern recommendations, or human feedback — the foundational entry is updated, and the agent's behavior changes on its next run.

This means the library's operational behaviour is itself library content, subject to the same versioning, auditing, and maturity model as any other entry. The system's playbook is not hardcoded; it evolves.

---

## Knowledge Node Schema

Every entry in the library, regardless of type or folder location, conforms to the following schema.

| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID. Immutable primary key. |
| title | string | Human-readable title. Should be concise and descriptive. |
| type | enum | One of: `knowledge`, `reference`, `foundational`, `governance`, `template`. |
| folder_path | string | Location in the folder tree, e.g. `/meta/foundational/python/testing` or `/knowledge/frontend/accessibility`. |
| maturity | enum | `stub` → `summary` → `detailed` → `complete`. Tracks enrichment level. |
| content | text | The knowledge content itself. May be a URL only (stub) or full standalone prose (complete). |
| source_url | string? | Original source link if applicable. |
| source_type | enum? | article, documentation, video, code, conversation, manual. |
| summary | string? | 1–3 sentence summary. Generated by indexer, refined by librarian. |
| tags | string[] | Flat labels for filtering. 2–10 per entry. |
| relationships | edge[] | Typed links: `{target_id, type, note}`. Types: related-to, depends-on, supersedes, example-of. |
| embedding | float[] | Vector embedding for semantic search. Generated on creation, refreshed on enrichment. |
| quality_score | float | 0–1. Composite of completeness, recency, link health, usage frequency. |
| decay_rate | enum | fast (6mo), medium (1yr), slow (3yr). Determines re-check frequency. |
| review_by | date | Next scheduled review date. Set by librarian based on decay_rate. |
| created_at | datetime | When the entry was first indexed. |
| updated_at | datetime | Last modification timestamp. |
| created_by | string | Agent or user that created the entry. |
| updated_by | string | Agent or user that last modified the entry. |
| changelog | log[] | Array of `{timestamp, agent, action, diff, reason}`. Full audit trail. |

---

## Default Folder Taxonomy

The top-level split separates the ingest surface (`/inbox/`), general knowledge, references, and meta/operational content. Procedural knowledge ("how to do things") does not have its own top-level folder — it lives in `/meta/foundational/` because it is the generative source for agent-specific skills and instructions, not a directly consumable artefact. New knowledge enters through `/inbox/` and is classified into the appropriate folder by the indexer. The top-level folders contain knowledge that agents reference or adapt; `/meta/` contains knowledge that the library and its projection system use to generate agent configurations.

| Folder | Purpose & Examples |
|--------|--------------------|
| `/inbox/` | Ingest drop zone. New knowledge — files, URLs, snippets — lands here in any format. The indexer watches this folder, classifies each item, creates a database entry, and moves the item to its destination folder. Processed items are moved to `/inbox/processed/` for auditability before eventual cleanup. Nothing stays in `/inbox/` long-term. |
| `/knowledge/` | Reusable design patterns, architectural approaches, and factual domain knowledge. Encompasses both structural patterns and evolving domain facts. Examples: `/knowledge/architecture/event-driven`, `/knowledge/api/pagination`, `/knowledge/finance/tax-regulations`, `/knowledge/frontend/accessibility`. |
| `/references/` | Pointers to external resources, APIs, documentation, tools. High proportion of stub/link entries. Examples: `/references/apis/stripe`, `/references/docs/aws-lambda`, `/references/tools/observability`. |
| `/meta/governance/` | Library self-management. Schema definitions, taxonomy rules, refinement policies, decision logs. How the library operates. |
| `/meta/foundational/` | Agent-agnostic procedural knowledge — the generative source for all agent skills and instructions. Describes principles, constraints, workflows, and gotchas for how to do things, without targeting any specific agent format. Subcategorised by topic. Examples: `/meta/foundational/python/testing`, `/meta/foundational/devops/docker`, `/meta/foundational/writing/technical-docs`. |
| `/meta/templates/` | Spawn templates that define how to transform foundational entries into consumer-specific formats. One template per target format, including both agent runtimes and human consumption. Examples: `/meta/templates/claude-skill`, `/meta/templates/cursor-rule`, `/meta/templates/openai-instruction`, `/meta/templates/human-readable`. |

The librarian agent is responsible for evolving this taxonomy. When a subfolder exceeds 50 entries, it should be split. When a subfolder has fewer than 3 entries for more than 30 days, it should be merged upward or reclassified. New top-level folders can be proposed but require human approval.

---

## Agent-Agnostic Design & Projection Model

The library is the source of truth. Agent runtimes are consumers. This section describes how foundational knowledge in the library gets projected into runtime-specific configurations, and why this separation matters.

### The Core Principle

The library does not store Claude skills, Cursor rules, or OpenAI custom instructions. It stores the underlying knowledge those artefacts are derived from. A foundational entry about "how to produce high-quality docx files" contains the principles, constraints, gotchas, and workflow steps that are true regardless of which agent executes them. From that single entry, you can generate a Claude skill, a Cursor rule, a human-readable runbook, or any other format a new agent runtime requires.

This means onboarding a new agent framework does not require rewriting all your skills. You write one new spawn template and generate the full set from what the library already knows.

### The Three-Layer Separation

#### Foundational Logic (lives in the library)

Agent-agnostic knowledge entries in `/knowledge/` and critically `/meta/foundational/`. The foundational folder is where procedural knowledge lives — how to do things, expressed as principles, constraints, and workflows rather than agent-formatted instructions. The librarian maintains, enriches, and refines these entries using the standard maturity model.

#### Spawn Templates (live in `/meta/templates/`)

Patterns for transforming foundational entries into consumer-specific formats. Each template defines: the target format, the extraction logic (which fields to include, how to structure them), and any format-specific conventions. Templates exist for agent runtimes (e.g. Claude SKILL.md, Cursor .cursorrules, OpenAI custom instructions) and also for human consumption (e.g. human-readable documentation with narrative, examples, and progressive disclosure).

#### Agent Projections (live in each project)

The generated output. These are runtime-specific files that agents load at execution time. They are cached copies of library knowledge, formatted for a specific consumer. They should be regenerated whenever their source entries are updated.

### Project-Level Agent Folders

Each agent runtime gets its own folder at the project level. All agent-specific configuration lives inside that folder, keeping the project root clean and making it clear what belongs to which runtime.

| Folder | Contents & Purpose |
|--------|--------------------|
| `.claude/` | All Claude-specific configuration. Contains: CLAUDE.md (operational instructions for Claude Code), skills/ (generated Claude-formatted skill files), settings.json (MCP config, permissions, custom commands). |
| `.cursor/` | All Cursor-specific configuration. Contains: rules/ (generated Cursor rule files), settings.json (workspace config). |
| `.openai/` | All OpenAI-specific configuration. Contains: instructions.md (generated custom instructions), tools/ (function definitions). |
| `.<agent>/` | The pattern generalises. Any new agent runtime follows the same convention: a dot-folder containing generated projections and runtime config. |

### The Generation Flow

When foundational knowledge changes, downstream projections are regenerated:

1. **Librarian updates a foundational entry.** For example, enriches `/meta/foundational/docx/document-creation` from a stub to a detailed entry with new constraints and best practices.
2. **Event emitted: "entry:enriched".** The event payload includes the entry ID and which fields changed.
3. **Projection generator checks dependencies.** A mapping table tracks which foundational entries feed into which agent projections. If `.claude/skills/docx.md` was generated from this entry, it is flagged for regeneration.
4. **Regeneration runs.** The spawn template for Claude skills is applied to the updated foundational entry. The new `.claude/skills/docx.md` is written.
5. **Optional: commit to version control.** If the project uses Git, the regenerated projection is committed with a message referencing the source change.

### Key Design Implications

- **CLAUDE.md lives inside `.claude/`.** It is Claude-specific operational context, not project-level configuration. Placing it inside the `.claude/` folder keeps the project root clean and makes the ownership explicit. Note: Claude Code currently expects CLAUDE.md at the project root; a symlink may be needed as a temporary workaround.
- **Skills are foundational entries, not agent config.** The canonical procedural knowledge lives in the library's `/meta/foundational/` folder as agent-agnostic entries. The `.claude/skills/` files are generated projections. If a skill is found lacking during execution, the feedback flows back to the foundational entry, not to the projection.
- **The library is the platform.** Switching from Claude to another agent runtime, or running both in parallel, requires only: (1) a spawn template for the new format, and (2) a new dot-folder in the project. All the knowledge transfers automatically.
- **/meta/ is the generative source.** The `/meta/` folder is the most critical folder in the library. `/meta/governance/` holds the operating rules, `/meta/foundational/` holds the procedural knowledge that generates all agent skills, and `/meta/templates/` holds the spawn templates that make the projection system work. Everything flows from `/meta/`.

### Human-Readable Projections

Since foundational entries are optimised for inference rather than human readability, the library needs a mechanism for producing human-consumable knowledge. This is handled as another projection type, not as a change to the foundational content.

#### Ephemeral (On-the-fly)

When a human queries the researcher directly — "explain our OAuth patterns to me" — the researcher assembles context from the foundational entry, its relationships, and related domain knowledge, then generates a readable response with narrative, examples, and context. This response is not stored; it is produced fresh each time.

#### Generated Artefact (On Request)

When someone asks "give me a document I can share with the team about our OAuth patterns," the system produces a formatted artefact (markdown, docx, or other format) from the foundational entry via the human-readable spawn template. This document is disposable: if the foundational entry changes, the document is regenerated rather than manually updated.

#### One-Way Discipline

Human-readable projections are strictly one-way. They are never edited and pushed back upstream. If a human reads the generated document and spots something wrong, the correction goes to the foundational entry in `/meta/foundational/`, not to the generated document. The librarian then updates the entry using inference-optimised formatting, and any downstream projections — including the human-readable version — can be regenerated.

---

## Agent Communication & Coordination

The agents coordinate through the library data itself plus a lightweight event/task queue. No agent needs direct access to another agent's working memory or filesystem.

### Event Queue

A simple table (or message queue) where agents post events and consume tasks. Events are typed and carry a payload:

| Event | Emitted By | Description & Payload |
|-------|------------|----------------------|
| ingest:received | Inbox watcher | New item detected in `/inbox/`. Payload: file path, file type, timestamp. Triggers the indexer. |
| entry:created | Indexer | New entry has been indexed and placed in its destination folder. Payload: entry ID, type, folder path. |
| entry:enriched | Librarian | Entry maturity upgraded. Payload: entry ID, old/new maturity. |
| entry:merged | Librarian | Duplicate entries consolidated. Payload: surviving ID, merged IDs. |
| entry:stale | Librarian | Entry flagged as potentially outdated. Payload: entry ID, reason. |
| link:broken | Librarian | Source URL no longer accessible. Payload: entry ID, URL, HTTP status. |
| knowledge:gap | Researcher | Query could not be satisfied. Payload: original query, domain, attempted strategies. |
| folder:rebalance | Librarian | Folder structure changed. Payload: affected paths, reason. |
| review:needed | Librarian | Entry past its review-by date. Payload: entry ID, days overdue. |
| projection:stale | Projection Gen. | An agent projection is out of date with its source entry. Payload: projection path, source entry ID, agent runtime. |
| intern:recommendation | Intern | A new recommendation has been posted to the review queue. Payload: recommendation type, target entry/policy, rationale, suggested action. |

### Coordination Pattern

The agents follow a task-queue-plus-shared-database pattern. The database is the library itself. Each operational agent reads from the database, performs its work, writes results back, and emits events. The intern reads everything but writes only to the recommendations queue. No agent calls another directly. This decouples them completely — they can run on different machines, different schedules, or different LLM providers.

**Example flow:** A user drops a URL into `/inbox/`. The indexer picks it up, creates a stub entry with metadata, moves it out of `/inbox/`, and emits "entry:created". The librarian, on its next scheduled run, sees the new stub, fetches the URL content, writes an enriched summary, discovers two related entries, creates relationship edges, and emits "entry:enriched". Later, an agent building a feature asks the researcher "what do we know about event-driven architecture?" The researcher runs a vector search, finds the enriched entry among the results, and returns a concise summary with a confidence score. Meanwhile, the intern observes across all of this: query patterns, classification decisions, enrichment quality — and periodically posts recommendations for how the system can improve.

---

## Quality Assurance & Feedback Loop

The library's knowledge quality cannot be judged by inspecting documents. It is measured through outcomes: do agents get useful answers, do projections work correctly, do humans encounter wrong knowledge? This section defines who checks what, when, and how corrections flow back to the foundational entries.

### Continuous Passive Checks (Intern)

The intern's observation is itself the primary quality check. It runs continuously or on a daily/weekly batch, accumulating signals from all system activity:

- **Retrieval misses:** Researcher queries that return no results or only low-maturity stubs. Indicates content gaps or poor embedding coverage.
- **Projection errors:** Agent-specific skills or configs that lead to incorrect behaviour. Traces back to ambiguity or incompleteness in the foundational entry.
- **Agent disagreements:** Indexer and librarian disagree on classification, or researcher returns results the consuming agent ignores. Signals structural misalignment.
- **Repeated query patterns:** Multiple agents or users asking the same question in different phrasings, suggesting the entry exists but isn't discoverable (tag gaps, embedding blind spots, synonym gaps).
- **Correction frequency:** Entries that receive frequent human corrections are likely still suboptimal and need deeper review.

Weekly, the intern produces a health report: a short digest surfacing the top 5–10 entries or domains most likely to need human attention, with evidence for each. Target: 15–30 minutes of human review time per report. If it takes longer, the intern's sensitivity needs tuning.

### Scheduled Mechanical Checks (Librarian)

The librarian runs structural and mechanical checks on a fixed cadence. These do not require human judgment:

- **Daily:** Link validation. Hit all source URLs, flag broken or redirected links.
- **Weekly:** Structural balance (folder sizes), maturity distribution (percentage of stubs vs enriched entries), embedding freshness.
- **Monthly:** Deep taxonomy review. Detect miscategorised entries, propose folder splits or merges, flag unused categories.

The librarian self-corrects where confident (e.g. flagging a broken link) and queues for human review where confidence is low (e.g. proposing a folder restructure).

### Human Review (Reactive, Not Proactive)

Humans are domain experts, not library janitors. They should never browse the library looking for problems, rewrite entries for formatting, check links, or reorganise folders. All of that is agent work. Instead, humans engage through three triggers:

#### Trigger 1: Intern Health Reports

The weekly digest surfaces entries needing attention. The human scans it, confirms or corrects the flagged entries, and moves on. Corrections are semantic: "this is wrong," "this is missing a crucial caveat," "these two entries are actually about different things." The librarian translates the correction into properly structured, inference-optimised updates to the foundational entry.

#### Trigger 2: Natural Work Corrections

During normal work, an agent uses a projection and it gives bad advice. The human notices and flags the error. This feedback enters the event queue as a correction event, the librarian updates the foundational entry, and affected projections regenerate. The system should make this feedback path frictionless — one command, one message, one annotation. No context-switching required.

#### Trigger 3: Threshold Alerts

Automated tripwires that escalate to human attention only when something is measurably off:

- **Researcher hit rate:** Drops below 80%. Indicates widespread content gaps or retrieval degradation.
- **Intern acceptance rate:** Falls outside the 20–90% band. Below 20% means intern recommendations aren't useful; above 90% means it's being too conservative.
- **Unresolved gaps:** More than 5 knowledge:gap events in a single domain within 14 days.
- **Projection failure rate:** Agents using projected skills report errors above a baseline threshold.

### A/B Experimentation

To empirically discover what "optimised for inference" means for the library's specific agents and domains, the librarian can produce variant versions of a foundational entry — one denser, one more verbose, one restructured differently — and measure which produces better researcher answers or projection quality. The intern tracks outcomes over time and learns which refinement patterns tend to improve performance. This builds an evidence base for content design decisions rather than relying on intuition.

### What Humans Contribute

The irreplaceable human inputs are: domain expertise (is this actually correct?), completeness judgments (is this missing something critical?), strategic direction (we're migrating to a new auth system, the library needs to reflect that), and ground truth corrections. Humans do not need to understand how agents process content. They just need to answer: "is what the library believes actually correct and complete?"

---

## Technology Stack

The library is designed to start simple (local, file-based) and scale up as needed. The following are recommended starting points.

| Component | Recommended | Notes |
|-----------|-------------|-------|
| Node store | SQLite (local) / PostgreSQL (shared) | Stores node schema. Simple, reliable, supports JSON fields for flexible metadata. |
| Folder tree | Filesystem + Git | Markdown files mirroring the database. Git provides versioning, diffing, and rollback. |
| Vector index | SQLite-vec / Chroma / Qdrant | Start with SQLite-vec for local. Move to Chroma or Qdrant when dataset exceeds ~50k entries. |
| Embeddings | Voyage / OpenAI / local model | Generate embeddings via API or local model. Store alongside node data. |
| Event queue | SQLite table / Redis pub-sub | Start with a simple "events" table polled by agents. Upgrade to Redis when latency matters. |
| Agent runtime | Any LLM agent (Claude Code, Cursor, etc.) | The library is agent-agnostic. Each runtime consumes projections from its dot-folder. |
| Projection generator | Script + spawn templates | Reads foundational entries + templates from `/meta/`, writes agent-specific configs to project dot-folders. Triggered by entry:enriched events. |
| API layer | FastAPI / Express | Optional. Exposes library CRUD + search as an HTTP API for remote agents. |

---

## Implementation Phases

The build is structured in four phases. Each phase produces a working system; later phases add sophistication. The goal is to have a usable library from Phase 1, not to wait until everything is built.

### Phase 1 — Foundation (Week 1–2)

Get the storage layer and the indexer working. The library can accept knowledge and store it.

- **Database setup:** Create the SQLite database with the node schema. Define tables for nodes, tags, relationships, events, and changelog.
- **Folder tree initialisation:** Create the default top-level folders (`/inbox/`, `/knowledge/`, `/references/`) and the `/meta/` subfolders (`/meta/governance/`, `/meta/foundational/`, `/meta/templates/`). Populate `/meta/governance/` with schema docs and taxonomy rules.
- **Foundational `/meta/` entries:** Write the first foundational logic entries in `/meta/foundational/` — agent-agnostic procedural knowledge on core topics. These should be rich enough that a spawn template could generate a Claude skill or equivalent from them.
- **Indexer agent v1:** Build a minimal indexer that watches `/inbox/`, classifies each item (type + folder), generates basic metadata (title, summary, tags), writes it to the database as a stub, and moves the processed item out of `/inbox/`.
- **CLI interface:** A simple command-line tool for ingesting knowledge (writes to `/inbox/` or calls the indexer directly) and browsing the folder tree. This is the initial human interface.
- **Deliverable:** You can add knowledge entries via CLI, browse them by folder, and see them in the database. `/meta/governance/` contains the library's self-documentation, `/meta/foundational/` contains the first procedural knowledge entries.

### Phase 2 — Retrieval (Week 3–4)

Get the researcher working. The library can answer questions.

- **Vector index:** Integrate an embedding model. Generate embeddings for all existing entries. Store in SQLite-vec or Chroma.
- **Researcher agent v1:** Build the query interface. Supports folder browsing, tag filtering, and semantic search. Returns results ranked by relevance with maturity/confidence indicators.
- **Tool interface:** Expose the researcher as a callable tool that any agent runtime can invoke — not just Claude Code. This is the agent-agnostic query API.
- **Gap logging:** When a query returns no results, log a "knowledge:gap" event with the original query.
- **Deliverable:** Any agent can query the library and get useful results. Gaps are tracked.

### Phase 3 — Refinement (Week 5–7)

Get the librarian working. The library improves itself over time.

- **Librarian agent v1:** Build the scheduled refinement loop. On each run, the librarian processes a queue of tasks: enrich stubs, validate links, check for duplicates.
- **Content enrichment pipeline:** For stub entries, fetch the source URL, extract content, generate a standalone summary, update the maturity score. All enrichment follows the inference-first principle: dense, declarative, explicit structure over narrative prose.
- **Relationship discovery:** After enriching an entry, compare it against nearby entries in the vector space. Propose and create relationship edges.
- **Link checker:** Scheduled job that hits all source URLs and flags broken or redirected links.
- **Deduplication:** Detect entries with >0.92 cosine similarity. Present candidates for merge with a proposed consolidated entry.
- **Audit logging:** Every librarian action writes to the changelog with before/after state and reasoning.
- **Deliverable:** The library self-heals. Stubs get enriched, links get checked, duplicates get merged, relationships emerge.

### Phase 4 — Intelligence (Week 8–10)

Advanced features that make the library proactively useful, including the agent projection system.

- **Projection generator:** Build the system that takes foundational entries + spawn templates and produces agent-specific configurations. Start with Claude (`.claude/CLAUDE.md`, `.claude/skills/`). Track which projections depend on which source entries so updates cascade automatically.
- **Spawn template authoring:** Create the first spawn templates in `/meta/templates/` for Claude skill format and the human-readable format. Document the template format so new agent runtimes or output formats can be onboarded by writing a single template.
- **Gap analysis engine:** The librarian analyses coverage patterns. Identifies domains with high query frequency but low entry count. Generates acquisition recommendations.
- **Staleness decay model:** Apply per-type decay rates. Auto-schedule reviews. Flag entries whose source content has changed since last check.
- **Folder rebalancing:** Automated detection of oversized or undersized folders. Propose restructurings with human approval for top-level changes.
- **Quality dashboard:** A view layer that shows library health: entry count by type/maturity, stale entries, broken links, coverage heatmap by domain, recent refinement activity, projection freshness.
- **Graph exploration:** An interface for traversing the relationship graph. "Show me everything connected to entry X within 2 hops."
- **Intern agent v1:** Build the observation loop. The intern reads all agent activity logs, event history, and query patterns. On each run, it produces a batch of typed recommendations into a review queue. Start with query-pattern analysis (identifying embedding gaps and missing synonyms) and agent-disagreement detection (indexer vs librarian placement conflicts).
- **Recommendations queue & review UI:** A simple interface where humans can approve, reject, or defer intern recommendations. Includes the weekly health report digest. Accepted recommendations become tasks for the librarian or updates to `/meta/foundational/` entries. Threshold alerts notify humans when metrics breach targets.
- **Deliverable:** The library is a self-improving, self-aware knowledge system with proactive gap filling, quality management, automated projection generation (including human-readable documents), and a complete feedback loop from outcomes back to foundational entries via the intern.

---

## Knowledge Maturity Model

Every entry progresses through a maturity lifecycle. The maturity level determines how the researcher presents it to consuming agents (confidence level) and how the librarian prioritises it (enrichment urgency).

| Level | Definition | Transition Rule |
|-------|-----------|-----------------|
| Stub | A URL or one-line description with basic metadata. No standalone content. Typical for link-first ingest. | Indexer sets this on creation. Librarian prioritises enrichment within 7 days. |
| Summary | Has a 1–3 sentence summary and full tag set. Source has been fetched and read. Not yet standalone. | Librarian upgrades from stub after initial enrichment pass. |
| Detailed | Full standalone prose. Can be understood without visiting the source. Relationships mapped. Tags refined. | Librarian upgrades after deep enrichment. Entry is now high-confidence for retrieval. |
| Complete | Authoritative entry. Reviewed by human or validated against multiple sources. Regularly maintained. | Requires human review or multi-source validation. Highest confidence tier. |

---

## Risks & Mitigations

| Risk | Mitigation | Likelihood |
|------|-----------|------------|
| Librarian makes bad merges or reclassifications | All changes are logged with before/after state. Implement a "confidence threshold" — low-confidence changes are queued for human review rather than auto-applied. | Medium |
| Library grows large, vector search becomes slow | Start with SQLite-vec. Migrate to Qdrant or Chroma at ~50k entries. Implement hierarchical search: folder filter first, then vector search within. | Low (long-term) |
| Agents over-query the library, high API/token costs | Cache frequent queries. Implement a TTL-based result cache. The researcher can return cached results for identical or near-identical queries within a window. | Medium |
| Knowledge conflicts: two entries say different things | The librarian flags conflicts. Human resolves. Entries can carry a "disputed" tag that lowers their confidence score until resolved. | Medium |
| Folder taxonomy becomes stale or misaligned | The librarian runs quarterly taxonomy reviews. Unused folders are flagged. The `/meta/` folder documents all taxonomy decisions and rationale. | Low |
| Projection drift: agent configs diverge from library source | Track projection-to-source mappings. Regenerate projections on source update. Add a staleness check that flags projections older than their source entry. | Medium |
| Agent-specific feedback lost: fix applied to projection, not library | Establish convention that all skill/knowledge fixes flow back to the foundational entry. Projections are treated as read-only generated artefacts, never edited directly. | High |
| Intern recommendation noise: too many low-value suggestions | Start with a narrow observation scope (query patterns and agent disagreements only). Expand as the review queue proves its value. Track accept/reject ratios to calibrate the intern's sensitivity. | Medium |

---

## Success Metrics

The following metrics indicate whether the library is healthy and providing value:

- **Retrieval hit rate:** Percentage of researcher queries that return at least one relevant result. Target: >80% by end of Phase 2.
- **Maturity distribution:** Percentage of entries at each maturity level. Target: <30% stubs after 3 months of librarian operation.
- **Staleness rate:** Percentage of entries past their review-by date. Target: <10%.
- **Link health:** Percentage of source URLs that resolve successfully. Target: >95%.
- **Duplicate rate:** Number of entries merged per month. Should trend downward as the indexer learns from past merges.
- **Gap fill rate:** Percentage of "knowledge:gap" events that result in a new entry within 14 days. Target: >50%.
- **Agent adoption:** Number of distinct agents querying the library per week. Indicates whether the library is actually useful in practice.
- **Projection freshness:** Percentage of agent projections that are up to date with their source entries. Target: 100% within 24 hours of a source update.
- **Intern acceptance rate:** Percentage of intern recommendations that are approved. If too low (<20%), the intern's observation scope or sensitivity needs tuning. If too high (>90%), it may be too conservative. Target: 40–70%.

---

## Next Steps

To begin implementation:

1. **Validate the schema:** Review the knowledge node schema with your team. Adjust fields based on your specific domain needs.
2. **Decide on storage backend:** SQLite for solo/local use, PostgreSQL for team/shared. This affects how agents connect.
3. **Seed the library:** Start with 20–30 entries you already know are valuable. This gives the librarian something to work with and tests the indexer's classification.
4. **Build Phase 1:** Database, folder tree, indexer, CLI. Target: 1–2 weeks of focused effort.
5. **Integrate early:** As soon as the researcher is functional (Phase 2), start connecting it to your working agents. Real usage reveals what the schema and retrieval need next.
6. **Write the first spawn template:** Define the Claude skill format template and the human-readable format template early. Even before the projection generator is automated (Phase 4), manually generating a few projections from foundational entries validates the separation model and the inference-first content approach.
