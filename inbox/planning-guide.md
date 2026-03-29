---
id: 448a4258-b9c7-4632-b50d-c8a848773b79
title: Planning Guide
source_type: manual
tags:
- planning
- project-management
- framework
- execution
- mental-models
created_at: '2026-03-29T00:00:00Z'
created_by: unknown
maturity: summary
summary: A thinking framework for planning any kind of work — development, research,
  operations, and personal projects. Organises planning into three lenses (Purpose,
  Structure, Motion) and documents common failure modes.
---

# Planning Guide

A thinking framework for planning any kind of work — development, research, operations, personal projects. Not a process to follow step-by-step, but a set of perspectives to rotate through depending on where you are and what you're uncertain about.

## How to use this

Pick the perspective that matches your current uncertainty. Starting something new? Start with Purpose. Stuck mid-project? Try Structure or Motion. Rotate as needed — these aren't phases, they're lenses.

Match the weight of your planning to the weight of the problem. A weekend project doesn't need a pre-mortem. A two-year initiative probably does. Not every section here applies to every project — use what fits, skip what doesn't. The goal is to think well, not to think exhaustively.

---

## Simplify relentlessly

This applies everywhere — purpose, structure, motion. The natural tendency in planning is to add: more steps, more layers, more distinctions, more process. Fight it. Every separation, every intermediate stage, every abstraction is a cost. It must solve a real problem to justify its existence.

In **purpose**: don't solve problems you don't have. Don't add goals "while we're at it." Every goal you add multiplies the work non-linearly — it's not one more thing, it's one more thing that interacts with everything else.

In **structure**: prefer flat over nested. If two things can be one thing without confusion, they should be one thing. Don't create layers to "stay organized" — create them only when a real boundary exists. A three-step process that could be two steps has a wasted step, even if each step is well-defined.

In **motion**: don't create process overhead that doesn't directly help you move. Status meetings, elaborate tracking, detailed documentation of intermediate work — each one is a drag on forward motion unless it's earning its keep.

The method: dump everything out first, *then* simplify. Get all the ideas, goals, tasks, and concerns out of your head. Then look at the pile and ask: what can I throw away? What can I merge? What's actually one thing pretending to be three? The first pass is expansive. The second pass is reductive. Most people skip the second pass.

---

## 1. Purpose — Why, what, and what not

Everything here is about understanding the problem before solving it.

### What's the actual need?

Strip to first principles. "We need a database" — no, you need to persist and query data. Maybe a file is enough. Work backward from the need, not forward from a tool or solution. Question inherited constraints: "we've always done it this way" isn't a constraint, it's a habit. Distinguish real constraints (budget, physics, deadlines) from assumed ones.

### What does done look like?

If you can't describe the end state, you're not ready to plan. This doesn't need to be detailed — "users can search the library by concept" is enough. But if you can't say even that, you need to explore before you plan.

### What assumptions are we making?

List them. The ones you don't examine are the ones that kill the project. Pay special attention to assumptions about what the user/audience needs, what's technically feasible, and how long things take.

Be aware that your mental model shapes what you even notice. A developer sees technical risk first. A PM sees scope risk first. A designer sees usability risk first. None are wrong — but each has blind spots. Actively seek perspectives you wouldn't naturally take.

### Has this been solved before?

Before building, search. Before searching, articulate what you're looking for precisely enough that you'd recognize a match. Most problems have been solved — the skill is finding and adapting, not reinventing. Even partial solutions or analogous work in other domains can save significant effort. In research contexts, this becomes literature review — a discipline in itself. Don't just search; systematically map prior art, related work, and adjacent fields.

### What's the minimum version?

What's the smallest thing that tests whether this is worth doing at all? This isn't about shipping something bad — it's about learning whether you're solving the right problem before investing fully. Cut scope to the core question. For a product or business, this includes validating demand — the minimum version isn't just "does this work?" but "does anyone want this?"

### Pre-mortem

Imagine the project has failed. Why? Work backward from the failure. This is more effective than risk lists because it leverages narrative thinking — you'll surface risks your optimistic brain skips when planning forward.

---

## 2. Structure — How it breaks apart and connects

Everything here is about seeing the shape of the work.

### Decomposition

Break the work into parts. The goal is pieces that are independently understandable and (ideally) independently executable. If a piece is still vague, it's either too big or it's an unknown that needs exploration, not decomposition.

### Dependencies

What blocks what? What must happen in sequence? What can run in parallel? The critical path — the longest chain of dependencies — determines the minimum time to completion. Everything else is flexible. Identify the critical path early; that's where delays compound.

### Overlaps

Do any tasks share inputs, outputs, or intermediate work? Can one effort serve multiple needs? Look for tasks that produce artifacts useful to other tasks. When you spot overlap, consider whether doing one thing well replaces doing two things separately. This is where reuse emerges naturally — not as an abstract goal but as a structural observation.

### Known vs. unknown

Separate them and treat them differently. Known work gets task lists and deadlines. Unknown work gets experiments with defined learning goals. Mixing them is how you end up with detailed plans for things you don't understand and vague hand-waving about things that are actually straightforward.

Not all unknowns are the same. Some are *solvable with analysis* — you don't know the answer yet, but the right expertise or research will get you there. Others are *emergent* — the outcome depends on how things interact, and you can only learn by trying. The first kind rewards upfront investigation. The second rewards small, safe-to-fail experiments where you learn by doing.

### Boundaries

Where are the clean seams? Good boundaries make delegation possible, parallel work safe, and scope changes contained. If changing one part always ripples into others, the boundaries are wrong. Look for natural interfaces — points where you can define "this part takes X and produces Y" without caring about internals.

---

## 3. Motion — How to move and stay on track

Everything here is about making effective progress. Urgent work plans itself — you react to it. The important-but-not-urgent work is where planning matters most, because it's what gets neglected and where the highest-leverage investments hide.

### What unblocks the most?

Do that first. Dependencies are the bottleneck, not individual task duration. A task that unblocks three others is more valuable than a task that's easy to finish but blocks nothing.

### Fail fast on unknowns

Build the part you're least sure about first. If it doesn't work, you've lost days, not months. The riskiest assumption should be validated before you invest in everything that depends on it.

### Prefer reusable work

When two tasks are roughly equal priority, do the one whose output is useful beyond this immediate project. Build the library function before the one-off script. This compounds over time.

### Optimize the workflow, not just the work

Friction in the process compounds. If you're doing something repeatedly and it's annoying — slow builds, manual steps, unclear handoffs — fix the process before grinding through more iterations. A small improvement to something you do 50 times matters more than a large improvement to something you do once.

### Externalize state

Plan on paper, in files, on boards — not in your head. You can't inspect what's only in memory. You can't share it, you can't diff it, and you'll lose it when context switches. The medium doesn't matter; the externalization does.

### Verify and replan

Three things to check as you go. *Internal consistency:* do the parts of the plan contradict each other? Are you doing redundant work, or following steps that made sense three decisions ago but no longer do? *External signal:* how will you know you're on track? Define the signal before you start — tests, reviews, metrics, user reactions. Without a feedback loop, you can drift a long time before noticing. *Direction:* is this plan still the right plan? Not just "am I on track" but "is the track still right." Plans decay. A plan that doesn't evolve with reality becomes a trap.

---

## Failure modes

A short reference for common ways planning goes wrong.

- **Planning the wrong thing.** Solving a problem that doesn't need solving, or solving the right problem for the wrong audience.
- **Wrong granularity.** Detailed plans for uncertain work (wasted effort when reality diverges). Vague plans for known work (confusion during execution).
- **Not replanning.** The plan is stale but you keep following it because changing feels like failure.
- **Confusing the plan with the goal.** The plan is a tool, not a commitment. Completing every task on the plan is worthless if it doesn't achieve the goal.
- **Local optimization.** Each step is efficient but the sequence is wrong. Doing the right things in the wrong order.
- **Planning as procrastination.** Planning feels productive. At some point you have to start. If you've answered the Purpose questions, you know enough to move. Timebox your planning — if you're still planning after the timebox, that's a signal the problem is too big (decompose it) or you're avoiding starting.

---

## Acknowledgements

Ideas in this framework draw from: OODA loop (John Boyd), Eisenhower matrix, Getting Things Done (David Allen), pre-mortem technique (Gary Klein), Cynefin framework (Dave Snowden), and agile/iterative development practices.
