---
id: d2bae234-ebf9-49e8-922a-6fc9334a1b61
title: Software Development Agent Catalog
maturity: summary
summary: A structured catalog of 28 custom agents covering the full software development lifecycle — testing, code review, documentation, DevOps, refactoring, and codebase research.
tags:
- agents
- software-development
- testing
- code-review
- documentation
- devops
- refactoring
- catalog
quality_score: 0.45
decay_rate: medium
review_by: 2026-04-22
created_at: 2026-03-23T04:49:15Z
updated_at: 2026-03-23T04:49:15Z
created_by: indexer
updated_by: indexer
changelog:
- timestamp: 2026-03-23T04:49:15Z
  agent: indexer
  action: created
  diff: null
  reason: "Initial synthesis from Useful Custom Agents for Claude Code"
---

Custom agents for software development fall into six categories that mirror the development lifecycle. Each agent automates a recurring, multi-step task that benefits from autonomous execution.

**Testing & Verification** agents catch problems before CI or humans do. They range from generating unit tests for untested code and running them, to creating regression tests from bug reports, analyzing coverage gaps by risk, and verifying that documentation examples still compile. Integration test agents exercise real cross-module interactions and flag flaky failures.

**Review & Security** agents enforce quality beyond what linters catch. A code review agent assesses diffs for logic errors, race conditions, and convention adherence. A security audit agent scans for hardcoded secrets, OWASP vulnerability patterns, and insecure configs. Performance review agents detect N+1 queries and algorithmic bottlenecks. Accessibility audit agents map findings to WCAG guidelines.

**Documentation & Knowledge** agents keep docs in sync with reality. They generate API docs from signatures, produce changelogs from git history, map architecture as diagrams, draft Architecture Decision Records, and create operational runbooks from deploy scripts.

**DevOps & Operations** agents assist with deployment preflight checks, incident diagnosis (correlating errors with recent changes), CI build debugging, and infrastructure-as-code review for security and cost implications.

**Refactoring & Maintenance** agents evolve code safely. Migration agents apply mechanical transforms for version upgrades. A dependency health agent audits risk and applies updates incrementally. Dead code eliminators verify removal safety before acting. Tech debt assessors rank debt by effort and risk. Optimization agents profile, improve, and benchmark.

**Research & Exploration** agents inform decisions. They generate onboarding guides for new contributors, detect undocumented knowledge gaps, and compare alternative libraries in structured decision matrices.
