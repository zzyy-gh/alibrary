---
id: 96ec1ccb-3750-48dd-88b7-aca6a7dab15f
title: Agent Extensibility and Composability
maturity: summary
summary: Agents define roles, not rigid recipes — methods and frameworks are interchangeable. Agents compose across domains, with one agent invoking others to build complex workflows.
tags:
- agents
- composability
- extensibility
- patterns
- design-principles
quality_score: 0.45
decay_rate: slow
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

Two principles govern how agents should be designed and deployed: extensibility and composability.

**Extensibility** means every agent defines a role, not a rigid recipe. The specific methods, frameworks, and tools an agent uses are interchangeable. A situational analysis agent might use SWOT and PESTEL as defaults, but Porter's Five Forces, Jobs-to-be-Done, or a custom industry framework can be swapped in without changing the agent's fundamental responsibility. The value lies in what the agent is accountable for — assessing strategic position — not the particular technique it employs. This applies broadly: a security audit agent can use OWASP top 10 or a company-specific threat model; a literature review agent can use PubMed or domain-specific databases.

**Composability** means agents chain together within and across domains. A deployment preflight agent invokes a test agent and a security audit agent before clearing a release. A strategic intelligence agent pulls from the OKR tracker, financial reconciliation agent, and pipeline hygiene agent to assemble a complete executive brief. A compliance drift monitor triggers a contract risk analyzer when regulations change. This composition pattern means individual agents stay focused on a single responsibility while complex workflows emerge from their combination.

The practical implication: start with one agent that addresses the biggest pain point, build it, iterate, and then compose outward. An agent that works well alone becomes more valuable when it can be invoked by other agents as part of a larger workflow.
