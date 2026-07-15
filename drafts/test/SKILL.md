---
name: test
description: |
  Phase 5 of design thinking. Audit the implementation against the spec.
  Produces an audit document. Input: implementation from /prototype + spec
  from /define. Invoke after Prototype. NOT the same as /design-doc —
  this evaluates a specific implementation cycle, not the system's full
  architecture.
---

# Test — Phase 5 of Design Thinking

Using test to audit the implementation against the spec and produce an evaluation record.

## Goal

Produce `docs/dt/audit.md`.

## Primary Inputs

Read `docs/dt/spec.md` (the criteria) and examine the implementation from Prototype before doing anything else.

## What the Audit Contains

- **Summary verdict** — one of: PASS / PARTIAL / FAIL, with a one-line rationale.
- **Per-criterion evaluation** — for each success criterion from the spec:
  - Status: PASS / PARTIAL / FAIL
  - Evidence: what in the implementation satisfies or fails to satisfy this criterion
- **Per failure-criterion check** — for each failure criterion from the spec: confirm it was not triggered.
- **Findings by severity:**
  - **Critical** — blocks release; must be fixed before the artifact can be used.
  - **Important** — should be fixed; does not block release but represents meaningful risk or gap.
  - **Minor** — nice to fix; low impact.
- **What works well** — not just problems. Explicitly note what is solid so the next cycle preserves it.
- **Recommendation** — one of:
  - Proceed to release.
  - Fix specific issues and re-run `/test`.
  - Return to `/prototype` (implementation is wrong).
  - Return to `/define` (spec was wrong).

## What Does NOT Belong in the Audit

- Full design documentation — that is `/design-doc`'s job.
- Implementation details beyond what is needed to evaluate a criterion.
- New requirements or features — capture those as tasks, not audit findings.

## Procedure

1. **Read the spec.** Extract every success criterion and failure criterion.
2. **Read or examine the implementation.** For code: read the relevant files and run tests if available. For documents: read the artifact. For other: review against the plan's deliverables.
3. **Evaluate each criterion.** Be specific about evidence — cite line numbers, sections, or behavior. Do not hand-wave.
4. **Identify additional findings** not captured in the spec. Categorize by severity.
5. **Write the audit** to `docs/dt/audit.md`. Use the frontmatter:
   ```yaml
   ---
   date: YYYY-MM-DD
   phase: test
   status: complete
   verdict: PASS|PARTIAL|FAIL
   ---
   ```
6. **Commit.**
   ```
   docs(dt): complete test phase — <verdict>: <brief description>
   ```
7. **Hand off** using the appropriate template below.

## Handoff — PASS

```
Phase complete: Test — PASS
Artifact: docs/dt/audit.md

Cycle complete. Next options:
- Release or merge the implementation.
- Invoke /design-doc to update the architectural design document (recommended at release boundary).
- Start a new cycle with /understand or /design-thinking for the next problem.
```

## Handoff — PARTIAL or FAIL

```
Phase complete: Test — PARTIAL/FAIL
Artifact: docs/dt/audit.md

Critical findings require fixing. Next:
- Open a new agent session, invoke /prototype with docs/dt/audit.md as additional context alongside docs/dt/plan.md and docs/dt/spec.md.
- If the spec was wrong: invoke /define instead, using the audit's findings to correct the spec.
```

## Note on /design-doc

After a successful test, `/design-doc` is recommended but optional. Call it at a release boundary — when the implementation is stable and the architecture should be recorded for future contributors and agents. Do not call it mid-cycle.
