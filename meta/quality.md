# Quality Assurance & Feedback Loop

The library's knowledge quality cannot be judged by inspecting documents. It is measured through outcomes: do agents get useful answers, do humans encounter wrong knowledge? This document defines who checks what, when, and how corrections flow back to the source nuggets.

## Continuous Passive Checks (Intern)

The intern's observation loop is the primary quality check. Weekly, it produces a health report: a short digest surfacing the top 5–10 entries or domains most likely to need human attention, with evidence for each. Target: 15–30 minutes of human review time per report.

## Scheduled Mechanical Checks (Librarian)

The librarian runs structural and mechanical checks on a fixed cadence. These do not require human judgment:

- **Daily:** Link validation. Hit source URLs on raw items, flag broken or redirected links.
- **Weekly:** Maturity distribution (percentage of stubs vs enriched nuggets), embedding freshness, orphaned raw items (no `derived-from` edges).
- **Monthly:** Tag vocabulary review. Detect inconsistent or redundant tags, propose consolidations.

The librarian self-corrects where confident (e.g. flagging a broken link) and queues for human review where confidence is low (e.g. proposing tag consolidation).

## Human Review (Reactive, Not Proactive)

Humans are domain experts, not library janitors. They should never browse the library looking for problems, rewrite entries for formatting, check links, or reorganise folders. All of that is agent work. Instead, humans engage through three triggers:

### Trigger 1: Intern Health Reports

The weekly digest surfaces entries needing attention. The human scans it, confirms or corrects the flagged entries, and moves on. Corrections are semantic: "this is wrong," "this is missing a crucial caveat," "these two entries are actually about different things." The librarian translates the correction into properly structured, inference-optimised updates to the source nugget.

### Trigger 2: Natural Work Corrections

During normal work, an agent uses library knowledge and it gives bad advice. The human notices and flags the error. This feedback enters the event queue as a correction event, and the librarian updates the source nugget. The system should make this feedback path frictionless — one command, one message, one annotation. No context-switching required.

### Trigger 3: Threshold Alerts

Automated tripwires that escalate to human attention only when something is measurably off:

- **Researcher hit rate:** Drops below 80%. Indicates widespread content gaps or retrieval degradation.
- **Intern acceptance rate:** Falls outside the 20–90% band. Below 20% means intern recommendations aren't useful; above 90% means it's being too conservative.
- **Unresolved gaps:** More than 5 knowledge:gap events in a single domain within 14 days.

## A/B Experimentation

To empirically discover what "optimised for inference" means for the library's specific agents and domains, the librarian can produce variant versions of a nugget — one denser, one more verbose, one restructured differently — and measure which produces better researcher answers. The intern tracks outcomes over time and learns which refinement patterns tend to improve performance. This builds an evidence base for content design decisions rather than relying on intuition.

## What Humans Contribute

The irreplaceable human inputs are: domain expertise (is this actually correct?), completeness judgments (is this missing something critical?), strategic direction (we're migrating to a new auth system, the library needs to reflect that), and ground truth corrections. Humans do not need to understand how agents process content. They just need to answer: "is what the library believes actually correct and complete?"

## Success Metrics

The following metrics indicate whether the library is healthy and providing value:

- **Retrieval hit rate:** Percentage of researcher queries that return at least one relevant result. Target: >80%.
- **Maturity distribution:** Percentage of nuggets at each maturity level. Target: <30% stubs after 3 months of librarian operation.
- **Staleness rate:** Percentage of entries past their review-by date. Target: <10%.
- **Link health:** Percentage of source URLs on raw items that resolve successfully. Target: >95%.
- **Duplicate rate:** Number of entries merged per month. Should trend downward as the indexer learns from past merges.
- **Gap fill rate:** Percentage of "knowledge:gap" events that result in a new entry within 14 days. Target: >50%.
- **Agent adoption:** Number of distinct agents querying the library per week. Indicates whether the library is actually useful in practice.
- **Intern acceptance rate:** Percentage of intern recommendations that are approved. If too low (<20%), the intern's observation scope or sensitivity needs tuning. If too high (>90%), it may be too conservative. Target: 40–70%.
