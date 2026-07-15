---
name: define
description: |
  Phase 2 of design thinking. Synthesize understanding into a precise problem
  definition and spec. Produces a spec with explicit success/failure criteria.
  Input: context brief from /understand. Invoke after Understand, or when
  Ideate reveals the spec is too vague.
---

# Define — Phase 2 of Design Thinking

Using define to synthesize understanding into a precise spec with verifiable criteria.

## Goal

Produce `docs/dt/spec.md`.

## Primary Input

Read `docs/dt/context-brief.md` before doing anything else.

## What the Spec Contains

- **Problem statement** — refined from the context brief; the one-sentence core of what must be solved.
- **Success criteria** — explicit, verifiable conditions that indicate the solution works. Each criterion must be checkable by the Test phase without ambiguity.
- **Failure criteria** — conditions that indicate the solution is wrong, even if it appears to work. What would make a "passing" solution actually unacceptable.
- **Invariants** — things that must always remain true regardless of what approach is chosen.
- **Scope** — what is in this cycle and what is explicitly out.
- **Open decisions** — explicit choices deferred to Ideate, listed with the known tradeoffs.

## What Does NOT Belong in the Spec

- How to solve it.
- Implementation approaches or technology choices.
- Task breakdowns.
- Code or pseudocode.

The spec defines the target, not the path.

## Procedure

1. **Read the context brief.** Internalize the problem statement, constraints, and open questions.
2. **Identify gaps.** Are there open questions from the context brief that block writing verifiable criteria? Ask Alex to resolve them, ONE question at a time.
3. **Write the spec** to `docs/dt/spec.md`. Use the frontmatter:
   ```yaml
   ---
   date: YYYY-MM-DD
   phase: define
   status: complete
   ---
   ```
4. **Self-review.** Check: Is any success criterion not verifiable? Does any criterion contradict another? Are all constraints from the context brief reflected? Fix before committing.
5. **Commit.**
   ```
   docs(dt): complete define phase — <brief description>
   ```
6. **Hand off.**

## Handoff

```
Phase complete: Define
Artifact: docs/dt/spec.md

Next: open a new agent session, invoke /ideate, read docs/dt/spec.md first.

Back-transitions: if spec reveals the problem was not understood → /understand
Skip forward: if you already have a clear plan → /ideate
```
