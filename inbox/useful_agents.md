---
id: f36943bd-bd3d-4a7d-a188-4b9e8421b33e
title: Useful Custom Agents for Claude Code
source_type: manual
tags:
- agents
- catalog
- reference
- automation
- multi-agent
created_at: 2026-03-23 00:00:00+00:00
created_by: human
---

# Useful Custom Agents for Claude Code

A catalog of custom agents worth building for Claude Code. Each entry describes what the agent does and why it's valuable — not how to write the AGENT.md file. Covers software development, professional services, commerce, healthcare, research, and education.

**Entry format:** agent name, one-line purpose, 3-4 concrete behaviors. The behaviors listed are starting points — swap in your own frameworks, methods, or tools as needed.

---

## 1. Testing & Verification

Catch problems before humans or CI do.

### Unit Test Generator
Write tests for untested code, run them, and report what changed.
- Scan source files to find functions/classes with no corresponding tests
- Generate test files following the project's existing framework and conventions
- Run the generated tests and fix failures before reporting
- Report coverage delta (before/after) so you know what improved

### Integration Test Agent
Verify that modules work together, not just in isolation.
- Identify module boundaries and public APIs that cross them
- Generate tests exercising real interactions (database, API calls, filesystem)
- Set up and tear down test fixtures and environments
- Run tests multiple times to flag flaky failures

### Doc Coherence Checker
Verify that documentation matches the actual codebase.
- Cross-reference README, API docs, and inline comments against real function signatures and file paths
- Detect stale references: deleted files, renamed functions, changed parameters
- Check that code examples in docs actually compile or run
- Report discrepancies with suggested fixes

### Coverage Analyst
Parse coverage results and prioritize what to test next.
- Run coverage tooling and parse the output
- Identify high-risk uncovered code: complex functions, error paths, recently changed files
- Rank gaps by risk (complexity x change frequency)
- Produce a prioritized list of test targets

### Regression Test Agent
Create tests from bug reports that reproduce the original bug.
- Read a bug report or the git diff of a fix
- Write a test that fails without the fix and passes with it
- Add the test to the correct suite
- Verify no existing tests break

---

## 2. Review & Security

Enforce quality standards beyond what linters catch.

### Code Review Agent
Perform thorough code review on staged changes or PRs.
- Read the diff and assess logic correctness, edge cases, and error handling
- Check adherence to project conventions that linters don't cover
- Identify potential bugs, race conditions, or resource leaks
- Produce structured review comments: file, line, severity, suggestion

### Security Audit Agent
Scan code for vulnerabilities and bad security practices.
- Check for hardcoded secrets, credentials, and API keys in source
- Identify common vulnerability patterns: SQL injection, XSS, path traversal, insecure deserialization
- Review dependency versions against known CVEs
- Flag insecure configurations: permissive CORS, debug mode in production

### Performance Review Agent
Identify performance bottlenecks and anti-patterns in code.
- Detect N+1 queries, unnecessary allocations, missing database indexes
- Flag O(n^2) or worse algorithms in hot paths
- Check for missing caching opportunities
- Review bundle sizes and lazy-loading patterns in frontend code

### Accessibility Audit Agent
Check frontend code for accessibility compliance.
- Scan templates and JSX for missing ARIA attributes, alt text, semantic HTML
- Verify keyboard navigation paths exist for all interactive elements
- Check color contrast ratios in style definitions
- Map findings to WCAG guidelines with severity levels

---

## 3. Documentation & Knowledge

Keep docs accurate and capture institutional knowledge.

### API Doc Generator
Generate or update API documentation from source code.
- Parse function/method signatures, types, and docstrings
- Generate markdown documentation following project conventions
- Include usage examples derived from test files
- Flag undocumented public APIs

### Changelog Generator
Produce changelogs from git history between releases.
- Parse commit messages between two tags or refs
- Categorize changes: features, fixes, breaking changes, internal
- Link to relevant PRs and issues
- Output in Keep a Changelog or similar format

### Architecture Doc Agent
Generate architecture documentation that reflects the actual codebase.
- Map module dependencies and produce component diagrams (mermaid or text)
- Document data flow between major components
- Identify the project's layer structure from imports and directory layout
- Detect drift between documented architecture and current reality

### Decision Record Agent
Draft Architecture Decision Records from context and code.
- Accept a decision topic and relevant context
- Research the codebase for prior decisions and constraints
- Draft an ADR: status, context, decision, consequences
- Link to related ADRs and code locations

### Runbook Generator
Create operational runbooks from deployment scripts and infrastructure config.
- Analyze deploy scripts, monitoring configs, and error handling code
- Document common procedures: deploy, rollback, scale, debug
- Include specific commands, expected outputs, and decision trees
- Verify steps against actual infrastructure

---

## 4. DevOps & Operations

Assist with deployment, CI, and incident response.

### Deployment Preflight Agent
Run pre-deployment checks to catch issues before they reach production.
- Verify all tests pass and coverage meets threshold
- Check environment variable requirements against deployment configs
- Validate database migrations are sequential and reversible
- Confirm no debug or dev-only code is present in production paths

### Incident Response Agent
Assist with diagnosing and responding to production incidents.
- Parse error logs and stack traces, locate relevant source code
- Identify recent changes that could have introduced the issue via git log
- Suggest a fix or rollback strategy
- Draft an incident report: timeline, root cause, remediation

### CI Debugger
Diagnose failing CI builds quickly.
- Read CI logs and identify the failure point
- Distinguish between flaky tests, environment issues, and real code failures
- Suggest fixes for common CI problems: cache invalidation, version mismatches, timeouts
- Attempt to reproduce the failure locally

### IaC Reviewer
Review infrastructure-as-code changes for correctness and security.
- Check for overly permissive IAM policies or security group rules
- Verify resource naming conventions and tagging
- Detect configuration drift between environments (dev/staging/prod)
- Flag cost implications of resource changes

---

## 5. Refactoring & Maintenance

Evolve code safely through systematic changes.

### Migration Agent
Assist with framework, library, or language version migrations.
- Scan for deprecated API usage based on migration guides
- Apply mechanical transformations: import paths, API signatures, config formats
- Flag cases that require manual review and cannot be auto-migrated
- Run tests after each transformation step to catch breakage early

### Dependency Health Agent
Audit dependency risk and apply updates safely.
- Check each dependency's maintenance status, known vulnerabilities, and available updates
- Assess breaking changes in major version bumps by reading changelogs
- Update one dependency at a time and run tests between each
- Produce a risk matrix and summary of what changed, flagging heavy deps with lighter alternatives

### Dead Code Eliminator
Find and remove unused code safely.
- Identify unreachable functions, unused imports, dead branches
- Verify removal safety by tracing all call sites and references
- Remove dead code in small, testable increments
- Report what was removed and lines saved

### Tech Debt Assessor
Quantify and prioritize technical debt across the project.
- Scan for TODO, FIXME, and HACK comments; categorize them
- Identify code duplication across the project
- Find overly complex functions: deep nesting, high cyclomatic complexity
- Produce a ranked debt backlog with estimated effort

### Optimization Agent
Profile and optimize existing code for speed, memory, or resource usage.
- Run profiling or benchmarking tools and identify the slowest code paths
- Apply targeted optimizations: algorithm improvements, caching, batch operations, lazy loading
- Benchmark before and after each change to verify measurable improvement
- Ensure no behavioral regressions by running the test suite between changes

---

## 6. Research & Exploration

Analyze codebases and inform decisions.

### Onboarding Agent
Generate an orientation guide for new contributors.
- Map the project structure and explain each top-level directory
- Identify entry points, key abstractions, and critical code paths
- List development setup steps by reading configs (package.json, Makefile, etc.)
- Produce a "start here" guide: the top 5 files to read first

### Knowledge Gap Detector
Identify undocumented areas of the project that represent risk.
- Compare code modules against existing documentation coverage
- Find complex logic with no explanatory docs or comments
- Identify tribal knowledge: code only one contributor has touched
- Produce a prioritized list of documentation needs

### Competitive Analysis Agent
Research and compare alternative tools, libraries, or approaches.
- Given a problem domain, search for relevant libraries and tools
- Compare features, performance, community size, and license
- Summarize trade-offs in a decision matrix
- Recommend a choice with reasoning

---

# Industry-Specific Agents

---

## 7. Legal & Compliance

Automate document-heavy legal workflows and track regulatory changes.

### Contract Risk Analyzer
Scan contracts for liability, compliance, and financial risks.
- Parse contract documents and extract key clauses: payment terms, liability caps, IP ownership, termination conditions
- Compare against safe templates and flag non-standard or high-risk language
- Cross-reference regulatory requirements for the relevant jurisdiction
- Generate a structured risk report with section-by-section annotations and recommended modifications

### Precedent Research Agent
Build comprehensive precedent summaries for legal arguments.
- Accept case type and jurisdiction constraints
- Search legal databases and knowledge bases for relevant case law, statutes, and treatises
- Synthesize into a precedent graph: holdings, tests applied, distinguishing facts
- Organize by precedential weight (binding, persuasive, distinguishable)

### Compliance Drift Monitor
Track regulatory changes and flag impacts on operational policies.
- Ingest regulatory feeds (SEC releases, FINRA notices, state guidance) on a schedule
- Compare new rules against existing company policies
- Map affected processes and personnel
- Emit alerts with impact assessment: which policy needs updating, by when, due to which regulation

### Document Metadata Extractor
Standardize metadata across heterogeneous legal documents for discovery.
- Scan document folders (contracts, emails, memos) and extract parties, dates, claims, amounts, signatories
- Create normalized data records linked to source documents
- Build searchable index by party, amount, date, and claim type
- Identify document gaps: missing signature pages, incomplete chains of custody

---

## 8. Finance & Accounting

Correlate transactions, validate positions, and automate reconciliation.

### Audit Trail Synthesizer
Build audit narratives by correlating transactions with supporting documents.
- Ingest transaction records and categorize by GL account and business process
- Match each transaction to supporting docs: invoices, POs, approvals
- Trace cash flow from source to use to reconciliation, flagging breaks in the chain
- Generate audit narrative with control flow and evidence for each material assertion

### Financial Reconciliation Agent
Automate high-variance reconciliation and variance investigation.
- Ingest trial balances and financial statements; identify line items with variance above threshold
- Search for root-cause explanations from prior periods (acquisitions, one-time charges)
- Generate variance explanation templates; prompt for investigation where no prior explanation exists
- Aggregate explanations into footnote and MD&A boilerplate

### Debt Covenant Monitor
Continuously assess loan covenant compliance and flag early warning signs.
- Ingest covenant definitions and monthly financial data
- Calculate covenant metrics: leverage ratio, interest coverage, working capital
- Alert 60/30/14 days before test dates with compliance forecast and variance drivers
- Propose corrective actions based on historical precedents

### Tax Position Validator
Ensure tax positions align with current guidance and case law.
- Index company tax positions: deductions, credits, restructuring, IP transfers
- Monitor IRS and court guidance; flag positions that are now vulnerable
- Cross-reference against industry guidance and peer benchmarks
- Alert tax team when positions have adverse rulings and recommend remediation

---

## 9. Human Resources

Reduce bias, identify gaps, and measure what matters in people operations.

### Skill Gap Mapper
Identify skills needed for succession and create targeted development plans.
- Ingest org chart, role definitions, and employee skill inventories
- Calculate gaps: which competencies does each role require vs. what the team currently has
- Identify high-potential internal candidates and generate development plans
- Track completion and readiness; recommend promotion timing or external hire

### Compensation Equity Auditor
Detect unexplained compensation disparities by role, tenure, and demographics.
- Ingest anonymized employee records: role, tenure, education, performance rating, compensation
- Run regression to identify what explains variance; flag unexplained gaps
- Stratify by demographics and identify statistically anomalous groups
- Generate audit report with confidence intervals and recommended adjustments

### Hiring Panel Calibration Agent
Reduce interview bias and ensure consistent scoring across panels.
- Ingest competency frameworks and interview rubrics for each role
- Compare panelists' past scores on same candidates; identify scoring variance
- Before interviews, surface key competencies, sample questions, and common interviewer errors
- After interviews, flag outlier scores and suggest recalibration discussion

### Training ROI Tracker
Measure whether training investments translate to behavior change and business impact.
- Link training programs to employee records; track enrollment, completion, test scores
- Post-training, measure engagement, manager feedback, promotion rates, attrition
- Calculate ROI by cohort; identify programs that drive behavior change vs. those that don't
- Recommend doubling down on high-impact programs and phasing out low-impact ones

---

## 10. Executive & Strategy

Synthesize cross-functional data into strategic decisions, reporting, and oversight.

### Strategic Intelligence Agent
Synthesize market data, competitor moves, and internal metrics into strategic briefs.
- Monitor competitor announcements, funding rounds, product launches, and hiring patterns
- Aggregate internal KPIs across departments into a unified executive dashboard
- Identify trends, threats, and opportunities; produce weekly strategic briefs
- Flag when competitors enter your market segments or when market conditions shift

### Situational Analysis Agent
Assess the company's current strategic position using structured frameworks.
- Run SWOT analysis: aggregate internal strengths/weaknesses from department data and external opportunities/threats from market intelligence
- Apply PESTEL framework: scan political, economic, social, technological, environmental, and legal factors relevant to the business
- Map competitive positioning: where the company sits vs. competitors on key dimensions (price, quality, speed, breadth)
- Produce a structured assessment with evidence from internal metrics and external sources

### Scenario Planning Agent
Model alternative futures and build contingency plans for key strategic decisions.
- Accept a strategic question (e.g., "what if our main competitor cuts prices 30%?" or "what if regulation X passes?")
- Model 3-4 scenarios: best case, worst case, most likely, and wildcard
- For each scenario, estimate impact on revenue, market share, talent, and operations using available data
- Produce a contingency playbook: trigger conditions, recommended actions, resource requirements, and decision deadlines

### Board & Investor Reporting Agent
Assemble board decks and investor updates from cross-functional data.
- Pull financial summaries, growth metrics, product milestones, and risk items from department reports
- Generate board-ready narrative: what happened, why it matters, what's next
- Track action items from prior board meetings and flag overdue commitments
- Produce investor update drafts with consistent formatting and tone

### OKR & Performance Tracker
Track company-wide objectives, surface what's off-track, and recommend course corrections.
- Ingest OKRs across all departments and track progress against key results
- Flag objectives falling behind schedule with root-cause context from department data
- Identify cross-team dependencies that are blocking progress
- Generate quarterly review summaries with achievement rates and recommended adjustments

### M&A Due Diligence Agent
Research acquisition targets and assess strategic fit, risks, and integration complexity.
- Compile target company profile: financials, product, team, market position, tech stack
- Assess strategic fit against company priorities and identify overlap or gaps
- Flag risks: regulatory, cultural, technical debt, customer concentration, key-person dependencies
- Produce due diligence summary with go/no-go recommendation and integration considerations

---

## 11. Sales & Marketing

Connect touchpoints to revenue and keep pipeline data clean.

### Prospect Research Agent
Identify high-value prospects, research their context, and score fit before outreach.
- Search company databases, industry reports, and news for companies matching ideal customer profile
- Enrich prospect data: company size, revenue, tech stack, recent funding, organizational changes
- Analyze buying signals: relevant job postings, tech announcements, acquisitions
- Score each prospect by fit and timing; prioritize for outreach

### Campaign Attribution Engine
Connect marketing touchpoints to revenue outcomes across channels.
- Ingest campaign spend, customer interactions (email, web, social), and revenue data
- Build customer journey graph: first touch through conversion with all intermediate interactions
- Apply multi-touch attribution; calculate channel contribution and tactic effectiveness
- Generate recommendations: increase budget here, reduce there, test this sequence

### Content Calendar Optimizer
Plan and sequence content across channels for maximum engagement and brand consistency.
- Ingest brand messaging pillars, product roadmap, event calendar, and audience interests
- Generate 90-day editorial calendar mixing content types and channels
- Check consistency: every piece should reinforce at least one brand pillar
- Flag gaps: topics with audience interest but no planned content

### Pipeline Hygiene Agent
Maintain CRM data quality and surface stalled deals.
- Validate pipeline data: flag missing close dates, inconsistent deal stages, opportunities lacking activity
- Analyze deal velocity and predict which deals are at risk of slipping
- Calculate revenue forecast with confidence intervals
- Surface stalled deals and suggest re-engagement tactics

---

## 12. Commerce & Supply Chain

Optimize listings and pricing; forecast demand and monitor suppliers.

### Catalog Optimizer
Enrich product listings with optimized descriptions and metadata.
- Extract attribute patterns from competitor listings and product databases
- Generate description variants targeting different buyer personas and SEO keywords
- Flag products missing critical attributes and auto-populate from supplier data
- A/B test listing elements and recommend updates based on performance

### Dynamic Pricing Agent
Adjust pricing and promotional strategy based on demand, competition, and inventory.
- Monitor competitor pricing, demand trends, and seasonal patterns
- Simulate price elasticity scenarios and calculate revenue-optimal pricing per SKU
- Recommend flash sales, bundles, and clearance for slow-moving inventory
- Alert when price changes trigger compliance issues (MAP violations, regional restrictions)

### Demand Forecasting Agent
Predict demand and recommend replenishment orders to minimize stockouts and overstock.
- Ingest point-of-sale data, seasonal trends, promotional calendar, and external signals (weather, economic indicators)
- Calculate optimal order quantities, safety stock, and reorder points
- Generate purchase orders for routine items; flag high-touch decisions for human review
- Monitor forecast accuracy post-shipment and adjust when demand patterns shift

### Supplier Performance Monitor
Track supplier quality, delivery, and compliance; flag risks and recommend actions.
- Track on-time delivery rates, defect rates, lead time variability, and invoice accuracy per supplier
- Monitor supplier certifications and alert when renewals are due or compliance flags appear
- Analyze root causes of delays or quality issues from supplier communications and shipping data
- Recommend diversification, contract renegotiation, or escalation based on risk thresholds

### Inventory Exception Agent
Track inventory across locations and surface discrepancies.
- Aggregate inventory counts from multiple systems (WMS, ERP, 3PLs) and reconcile
- Flag shrinkage, misplaced stock, and obsolete inventory requiring writeoff
- Detect in-transit shipments at risk of delay and recommend corrective actions
- Recommend inventory rebalancing across locations to meet demand

---

## 13. Customer Success & Support

Triage faster, prevent escalation, and retain at-risk customers.

### Ticket Triage Agent
Automatically categorize, prioritize, and route support tickets.
- Parse ticket content to extract issue category, urgency, and customer impact
- Score priority using urgency, customer segment, and issue type
- Route to appropriate queue: critical outages to senior engineers, billing to finance, feature requests to product
- Suggest matching knowledge base articles and generate canned responses for routine issues

### Knowledge Base Curator
Build and maintain a searchable knowledge base from resolved support tickets.
- Analyze resolved tickets to identify recurring issues and extract resolution steps
- Draft knowledge base articles from ticket solutions with troubleshooting steps
- Tag articles by keywords, customer segments, and product versions
- Monitor article usage and suggest updates when tickets reveal gaps

### Customer Risk & Retention Agent
Identify at-risk tickets and accounts, intervene before satisfaction declines.
- Monitor ticket-level signals (response time, sentiment, backlog age) and account-level signals (feature adoption, utilization, renewal date)
- Predict escalation and churn risk; prioritize by severity and customer value
- Recommend intervention: reassign tickets, schedule health checks, offer training or compensation
- Track NPS/CSAT trends and surface cohorts with declining satisfaction

---

## 14. Healthcare & Medical

Match patients, monitor protocols, and track outcomes.

### Clinical Trial Matcher
Match patients to clinical trials based on eligibility criteria.
- Ingest anonymized patient records: diagnoses, prior treatments, comorbidities, labs, demographics
- Index clinical trials by eligibility criteria, phase, enrollment status, and location
- Identify trials each patient qualifies for; check contraindications and enrollment caps
- Generate a ranked report: best fit, secondary options, and marginal matches

### Treatment Protocol Monitor
Flag when treatment deviates from evidence-based protocols.
- Ingest treatment protocols indexed by condition and risk factors
- For each patient, check whether prescribed treatment aligns with protocol
- Flag undocumented deviations and outdated protocols (guideline updated but practice unchanged)
- Alert clinical team with deviation details and request justification

### Medication Interaction Checker
Identify drug-drug, drug-supplement, and drug-food interactions before prescribing.
- Index medication interaction database: severity, mechanism, and recommendation
- When a prescriber inputs patient medications, check the full interaction matrix
- Alert on significant interactions and suggest alternatives for high-risk combinations
- Flag genetic polymorphisms that affect drug metabolism when data is available

### Outcomes Quality Tracker
Monitor treatment outcomes by provider and protocol to identify outliers.
- Ingest treatment records and follow-up outcomes: readmission, mortality, complications
- Calculate risk-adjusted outcome metrics by provider, hospital, and protocol
- Identify providers or protocols with better or worse outcomes than expected
- Alert when outcomes fall below targets and recommend practice review

---

## 15. Research & Academia

Synthesize literature, build proposals, and target the right venues.

### Literature Review Synthesizer
Systematically search and synthesize literature on a research topic.
- Accept research question and inclusion/exclusion criteria
- Search databases (PubMed, arXiv, Google Scholar) and apply inclusion criteria
- Extract from each paper: study design, sample size, key findings, limitations
- Synthesize into a narrative summary with evidence table, quality assessment, and gap identification

### Grant Proposal Builder
Assemble preliminary data, literature, and budget into grant proposal structure.
- Ingest researcher's prior publications, funding history, and preliminary data
- Query for citation trends, successful themes in funder's past awards, and budget benchmarks
- Generate proposal skeleton: significance, innovation, and approach sections populated with data
- Flag missing preliminary data, needed citations, and budget red flags

### Journal Targeting Assistant
Help researchers identify the best venue for their work.
- Accept manuscript abstract and keywords
- Query journal database: scope fit, impact factor, acceptance rate, review timeline
- Estimate acceptance probability based on similarity to published papers and author profile
- Generate ranked list with fit reasoning and backup options

### Peer Review Assignment Optimizer
Recommend reviewers for submitted manuscripts based on expertise and conflict of interest.
- Extract paper topics and methods; query reviewer database for expertise match
- Check for conflicts: co-authorship, competing work, institutional overlap
- Predict review quality from historical track record (thorough vs. superficial feedback)
- Recommend 4-5 reviewer options ranked by expertise and quality fit

---

## 16. Education & Training

Personalize learning, scale feedback, and detect at-risk students early.

### Learning Path Generator
Build customized learning plans based on student assessment data.
- Administer diagnostic assessments to determine baseline knowledge and gaps
- Map results to curriculum learning objectives; identify prerequisite gaps
- Generate learning path: recommended resources, sequencing, and checkpoint assessments
- Adjust path dynamically based on ongoing assessment results

### Assessment Feedback Agent
Grade assignments and provide detailed feedback at scale.
- Accept student submissions (essays, code, problem sets) and analyze against rubric criteria
- Generate detailed feedback: strengths, gaps, specific areas for improvement, misconceptions
- Compare against exemplars and peer work to provide contextualized feedback
- Flag patterns (common misconceptions, struggling learners) for instructor intervention

### Curriculum Content Generator
Rapidly generate curriculum materials adapted for different learning modalities.
- Accept learning objectives and generate outlines, modules, practice problems, and assessments
- Create content variants: visual (infographics), kinesthetic (simulations), auditory (lecture notes)
- Adapt for different competency levels: remedial, grade-level, advanced
- Cross-reference existing content to minimize duplication

### Student Early Alert Agent
Identify at-risk students and recommend interventions before failure.
- Monitor performance data: assignment completion, test scores, attendance, engagement signals
- Build predictive models of student success risk; flag early warning signs
- Recommend interventions: tutoring, study groups, office hours, curriculum adjustments
- Track intervention uptake and outcomes; refine predictions based on effectiveness data

---

## How to Use This Catalog

**Extensibility.** Every agent here defines a role, not a rigid recipe. The Situational Analysis Agent lists SWOT and PESTEL as examples — but you could just as easily plug in Porter's Five Forces, Jobs-to-be-Done, or a custom framework that fits your context. The same applies throughout: swap methods, add steps, combine approaches. The value is in what the agent is responsible for, not the specific technique it uses.

**Composability.** Agents work well together — within and across domains. A deployment preflight agent can invoke a test agent and a security audit agent before clearing a release. A strategic intelligence agent can pull from the OKR tracker, financial reconciliation agent, and pipeline hygiene agent to assemble a complete executive brief. A compliance drift monitor can trigger a contract risk analyzer when regulations change.

**Getting started.** Pick one agent that addresses your biggest pain point, build it, iterate on it, and compose from there.
