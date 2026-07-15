---
name: ideate
description: |
  Phase 3 of design thinking. Generate and select an approach, then produce a
  concrete implementation plan. Input: spec from /define. Invoke after Define,
  or when Prototype reveals a fundamental design issue requiring replanning.
---

# Ideate — Phase 3 of Design Thinking

Using ideate to generate approaches and produce a concrete implementation plan.

## Goal

Produce `docs/dt/plan.md`.

## Primary Input

Read `docs/dt/spec.md` before doing anything else.

## What the Plan Contains

- **Chosen approach** — the selected solution strategy, with 2-3 alternatives considered and explicit rationale for the choice.
- **Task breakdown** — an ordered list of tasks, each producing a testable increment. Tasks are sequential where there are dependencies; note which are independent.
  - For code tasks: each task lists the files to create or modify and a verify step (how to confirm the task is done).
  - For writing tasks: each task produces a section, draft, or revision pass.
  - For other tasks: each task produces a concrete deliverable.
- **Key design decisions** — choices made here that constrain Prototype. Explicitly document what was decided and why alternatives were not chosen.

## What Does NOT Belong in the Plan

- Implementation code itself.
- Test results or evaluation.
- Content that belongs in the spec (criteria, invariants).

The plan is the road, not the destination and not the vehicle.

## Procedure

1. **Read the spec.** Internalize all success criteria, failure criteria, invariants, and scope.
2. **Propose 2-3 approaches.** For each: name it, describe the core idea, and list the main tradeoffs relative to the spec's criteria.
3. **Select the best approach.** If the choice is genuinely ambiguous between approaches that serve the spec equally well, ask Alex. Otherwise, decide and document the reasoning.
4. **Break into tasks.** Each task should be small enough to complete in one sitting and produce something verifiable.
5. **Write the plan** to `docs/dt/plan.md`. Use the frontmatter:
   ```yaml
   ---
   date: YYYY-MM-DD
   phase: ideate
   status: complete
   ---
   ```
6. **Self-review against spec.** For each success criterion in the spec, trace it to at least one task in the plan. If a criterion is not covered, add a task.
7. **Commit.**
   ```
   docs(dt): complete ideate phase — <brief description>
   ```
8. **Hand off.**

## Handoff

```
Phase complete: Ideate
Artifact: docs/dt/plan.md

Next: open a new agent session, invoke /prototype, read docs/dt/plan.md and docs/dt/spec.md first.

Back-transitions: if plan reveals the spec has fundamental gaps → /define
Skip forward: if implementation is already started → /prototype
```
