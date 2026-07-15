---
name: understand
description: |
  Phase 1 of design thinking. Map the problem space thoroughly before defining
  or solving. Produces a context brief. Invoke at the start of any non-trivial
  problem, or when a later phase reveals the problem was not well understood.
---

# Understand — Phase 1 of Design Thinking

Using understand to map the problem space before any definition or solution work.

## Goal

Produce `docs/dt/context-brief.md`.

## What the Context Brief Contains

- **Problem statement** — what is broken, missing, or desired; why it matters now.
- **Current state** — what exists today and its limitations or pain points.
- **Stakeholders and needs** — who is affected and what each party needs from a solution.
- **Hard constraints** — things that cannot change (technical, organizational, time-bound).
- **Adjacent systems and dependencies** — what this problem touches that is outside its boundary.
- **Open questions** — things that must be resolved before the problem can be properly defined.
- **Explicitly out of scope** — what will not be addressed in this cycle.

## What Does NOT Belong in the Context Brief

- Proposed solutions.
- Success criteria or acceptance conditions.
- Implementation details or task breakdowns.
- Design decisions.

The context brief is a map, not a plan.

## Procedure

1. **Gather existing context.** Read `AGENTS.md`, `know-how/`, any notes or background Alex provided, and the existing `context-brief.md` if this is an update pass.
2. **Ask clarifying questions.** Surface gaps ONE AT A TIME. Do not ask multiple questions in a single message — each answer may eliminate subsequent questions. Continue until you can write the brief without leaving blanks.
3. **Write the context brief** to `docs/dt/context-brief.md`. Use the frontmatter:
   ```yaml
   ---
   date: YYYY-MM-DD
   phase: understand
   status: complete
   ---
   ```
4. **Commit.**
   ```
   docs(dt): complete understand phase — <brief description>
   ```
5. **Hand off.**

## Handoff

```
Phase complete: Understand
Artifact: docs/dt/context-brief.md

Next: open a new agent session, invoke /define, read docs/dt/context-brief.md first.

Back-transitions: if Define reveals the problem is still unclear → return to /understand
Skip forward: if problem and constraints are already well-known → start at /define
```
