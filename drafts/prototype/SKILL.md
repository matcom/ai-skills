---
name: prototype
description: |
  Phase 4 of design thinking. Execute the plan to produce a working artifact.
  Input: plan from /ideate and spec from /define. For code: uses superpowers
  execution skills. For writing/creative: produces the draft artifact.
  Invoke after Ideate.
---

# Prototype — Phase 4 of Design Thinking

Using prototype to execute the plan and produce a working artifact.

## Goal

Implement the plan and produce a working artifact: code committed, document written, or other concrete deliverable.

## Primary Inputs

Read `docs/dt/plan.md` (primary) and `docs/dt/spec.md` (success criteria reference) before doing anything else.

## Execution by Task Type

### Code tasks

Invoke `superpowers:subagent-driven-development` or `superpowers:executing-plans` — do not reinvent execution. The plan's task breakdown is the input. The spec's success criteria are the acceptance bar.

### Writing tasks

Follow the plan's task breakdown. Produce each section or draft in order. Use the spec to verify you are producing what was asked for, not what seems interesting.

### Creative or other tasks

Follow plan tasks in order. Produce each deliverable before moving to the next. Do not batch-produce — one task at a time allows early course correction.

## Note on Artifact Location

Prototype does NOT write to `docs/dt/`. It writes to wherever the artifact lives:

- Code: `src/`, `lib/`, wherever the repo puts it.
- Documents: `vault/Efforts/Projects/<name>/`, or wherever the project lives.
- Other: follow the plan's specified output locations.

The `docs/dt/` directory is for design-thinking process artifacts only.

## Self-Review Before Handoff

Before declaring Prototype complete, do a quick pass against the spec:

- Does each success criterion have something in the implementation that addresses it?
- Are there any criteria that were not touched at all?

This is a gap check, not a full evaluation — that is Test's job. Do not attempt to evaluate quality or correctness in detail here. If there are obvious omissions, fill them. If the gap is fundamental (wrong approach, spec was wrong), back-transition rather than pushing through.

## Back-Transitions

- Fundamental design issue discovered mid-implementation → back to **Ideate** (update `plan.md` with what changed and why).
- Implementation reveals spec was wrong or contradictory → back to **Define** (update `spec.md`).

Do not back-transition silently. Update the relevant artifact before reopening that phase.

## Handoff

```
Phase complete: Prototype
Artifact: [describe what was built and where — commit hash for code, file path for docs]

Next: open a new agent session, invoke /test, read docs/dt/spec.md and review the implementation.

Back-transitions: if fundamental design issue discovered → /ideate (or /define if spec was wrong)
```
